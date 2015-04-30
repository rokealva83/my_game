from django.shortcuts import render
from my_game.models import MyUser, User_city, Warehouse, Chat
import function
from django.http import JsonResponse
from django.utils import timezone



def chat(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        message = Chat.objects.all()
        if message:
            last_id = Chat.objects.last().pk
            need_id = int(last_id) - 38
            messages = Chat.objects.filter(id__gte=need_id).all()
        else:
            message = Chat(
                user='System',
                text='Hello, user'
            )
            message.save()
            messages = Chat.objects.all()



        user_name = MyUser.objects.filter(user_id = session_user).first().user_name

        function.check_all_queues(session_user)
        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('id_resource')
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = User_city.objects.filter(user=int(session_user))

        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output={'user': user, 'warehouses': warehouses, 'user_city': user_city, 'user_citys': user_citys, 'user_name':user_name, 'messages':messages}

        return render(request, "chat.html", output)


def send_message(request):
    user = request.POST.get('user')
    text = request.POST.get('text')
    time = timezone.now()
    message = Chat(
        user = user,
        text = text,
        time = time
    )
    message.save()


def update_message(request):
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