from django.shortcuts import render
from my_game.models import MyUser, User_city, Warehouse, Chat, User_chat_online
import function
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime


def chat(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        user = MyUser.objects.filter(user_id=session_user).first()

        user_online = User_chat_online.objects.filter(user_id=session_user).first()
        if user_online is None:
            user_online = User_chat_online(
                user_id=session_user,
                user=user.user_name,
                last_time_update = timezone.now()
            )
            user_online.save()
            message = Chat(
                user_id=1,
                user='System',
                text= 'Hello, ' + str(user.user_name)
            )
            message.save()
        else:
            user_online = User_chat_online.objects.filter(user_id=session_user).update(last_time_update = timezone.now())

        last_id = Chat.objects.last().pk
        need_id = int(last_id) - 38
        messages = Chat.objects.filter(id__gte=need_id).all()

        online_users = User_chat_online.objects.all()

        user_name = MyUser.objects.filter(user_id=session_user).first().user_name
        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('id_resource')
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = User_city.objects.filter(user=int(session_user))

        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouses': warehouses, 'user_city': user_city, 'user_citys': user_citys,
                  'user_name': user_name, 'messages': messages, 'online_users':online_users}

        return render(request, "chat.html", output)


def send_message(request):
    session_user = int(request.session['userid'])
    user = MyUser.objects.filter(user_id=session_user).first()
    name = request.POST.get('user')
    text = request.POST.get('text')
    time = timezone.now()
    message = Chat(
        user_id=session_user,
        user=name,
        text=text,
        time=time
    )
    message.save()
    user_online = User_chat_online.objects.filter(user_id=session_user).first()
    if user_online is None:
        user_online = User_chat_online(
            user_id=session_user,
            user=user.user_name,
            last_time_update = timezone.now()
        )
        user_online.save()
    else:
        user_online = User_chat_online.objects.filter(user_id=session_user).update(last_time_update = timezone.now())



def update_message(request):
    session_user = int(request.session['userid'])
    id = int(request.POST.get('id'))
    messages = Chat.objects.filter(id__gte=id).all()
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
    online_users = User_chat_online.objects.all()
    for online_user in online_users:
        last_time_update = online_user.last_time_update
        delta_time = timezone.now()-last_time_update
        delta_time = delta_time.seconds
        if delta_time > 30:
            online_user_delete = User_chat_online.objects.filter(id = online_user.id).delete()



def update_user_delete(request):
    id = int(request.POST.get('id'))
    response = 0
    online_user = User_chat_online.objects.filter(id = id)
    if online_user:
        response = 1
    return JsonResponse({
        'result': response
    })

def update_user(request):
    id = int(request.POST.get('id'))
    user_onlines = User_chat_online.objects.filter(id__gt=id).all()
    response = []
    for usr in user_onlines:
        response.append({
            'id': usr.pk,
            'user': usr.user,
        })
    return JsonResponse({
        'result': response
    })