# -*- coding: utf-8 -*-

from my_game.models import ChatPrivate, UserChatOnline, MyUser
from django.http import JsonResponse


def send_private_message(request):
    session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
    user = session_user.user_name
    recipient_id = int(request.POST.get('user'))
    text = request.POST.get('text')
    recipient_name = UserChatOnline.objects.filter(id=recipient_id).first().user
    recipient_id = MyUser.objects.filter(user_name=recipient_name).first().id

    message = ChatPrivate(
        user_id=session_user.id,
        user=user,
        recipient=recipient_id,
        recipient_name=recipient_name,
        text=text,
    )
    message.save()


def update_private_message(request):
    session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
    message = ChatPrivate.objects.filter(recipient=session_user.id).first()
    response = []
    if message:
        response.append({
            'user_id': message.user_id,
            'user': message.user,
            'text': message.text,
        })
    message_delete = ChatPrivate.objects.filter(id=message.id).delete()
    return JsonResponse({
        'result': response
    })