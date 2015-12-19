# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity, Warehouse, Chat, UserChatOnline
from django.http import JsonResponse
from django.utils import timezone


def chat(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        user_online = UserChatOnline.objects.filter(user_id=session_user.id).first()
        if user_online is None:
            user_online = UserChatOnline(
                user_id=session_user.id,
                user=session_user.user_name,
                last_time_update=timezone.now()
            )
            user_online.save()
            message = Chat(
                user_id=1,
                user='System',
                text='Hello, ' + str(session_user.user_name)
            )
            message.save()
        else:
            user_online = UserChatOnline.objects.filter(user_id=session_user.id).update(last_time_update=timezone.now())

        last_id = Chat.objects.last().pk
        need_id = int(last_id) - 38
        messages = Chat.objects.filter(id__gte=need_id).all()

        online_users = UserChatOnline.objects.all()

        user_name = session_user.user_name
        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('resource_id')
        user_city = UserCity.objects.filter(user=session_user).first()
        user_citys = UserCity.objects.filter(user=session_user)

        request.session['user'] = session_user.id
        request.session['user_city'] = session_user_city.id
        request.session['live'] = True
        output = {'user': session_user, 'warehouses': warehouses, 'user_city': user_city, 'user_citys': user_citys,
                  'user_name': user_name, 'messages': messages, 'online_users': online_users}

        return render(request, "chat.html", output)


def send_message(request):
    session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
    name = request.POST.get('user')
    text = request.POST.get('text')
    time = timezone.now()
    message = Chat(
        user_id=session_user.id,
        user=name,
        text=text,
        time=time
    )
    message.save()
    user_online = UserChatOnline.objects.filter(user_id=session_user.id).first()
    if user_online is None:
        user_online = UserChatOnline(
            user_id=session_user.id,
            user=session_user.user_name,
            last_time_update=timezone.now()
        )
        user_online.save()
    else:
        UserChatOnline.objects.filter(user_id=session_user.id).update(last_time_update=timezone.now())


def update_message(request):
    post_id = int(request.POST.get('id'))
    messages = Chat.objects.filter(id__gte=post_id).all()
    response = []
    for msg in messages:
        response.append({
            'id': msg.pk,
            'text': msg.text,
            'user': msg.user,
            'time': msg.time,
        })
    return JsonResponse({
        'result': response
    })


def user_delete(request):
    online_users = UserChatOnline.objects.all()
    for online_user in online_users:
        last_time_update = online_user.last_time_update
        delta_time = timezone.now() - last_time_update
        delta_time = delta_time.total_seconds()
        if delta_time > 300:
            UserChatOnline.objects.filter(id=online_user.id).delete()


def delete_user_update(request):
    id = int(request.POST.get('id'))
    response = 0
    online_user = UserChatOnline.objects.filter(id=id)
    if online_user:
        response = 1
    return JsonResponse({
        'result': response
    })


def update_user(request):
    id = int(request.POST.get('id'))
    user_onlines = UserChatOnline.objects.filter(id__gt=id).all()
    response = []
    for usr in user_onlines:
        response.append({
            'id': usr.pk,
            'user': usr.user,
        })
    return JsonResponse({
        'result': response
    })