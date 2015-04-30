
from my_game.models import Chat_private, User_chat_online, MyUser
import function
from django.http import JsonResponse
from django.utils import timezone



def send_private_message(request):
    session_user = int(request.session['userid'])
    user = MyUser.objects.filter(user_id=session_user).first().user_name
    recipient_id = int(request.POST.get('user'))
    text = request.POST.get('text')
    recipient_name = User_chat_online.objects.filter(id=recipient_id).first().user
    recipient_id = MyUser.objects.filter(user_name = recipient_name).first().user_id

    message = Chat_private(
        user_id=session_user,
        user=user,
        recipient = recipient_id,
        recipient_name = recipient_name,
        text=text,
    )
    message.save()


def update_private_message(request):
    session_user = int(request.session['userid'])
    message = Chat_private.objects.filter(recipient = session_user).first()
    response = []
    if message:
        response.append({
            'user_id': message.user_id,
            'user': message.user,
            'text': message.text,
        })
    message_delete = Chat_private.objects.filter(id = message.id).delete()
    return JsonResponse({
        'result': response
    })