# -*- coding: utf-8 -*-

from datetime import datetime
from django.shortcuts import render
from my_game.models import MyUser, UserCity, Warehouse
from my_game import function
from my_game.models import Mail


def send_mail(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)

        target = request.POST.get('message_target')
        target_name = MyUser.objects.filter(user_name=target).first()
        if target_name is None:
            message = 'GGGGGGGGGGGGGGGGGGGGgg'
        else:
            title = request.POST.get('title')
            mail = request.POST.get('message')
            user = MyUser.objects.filter(user_id=session_user).first()
            user_name = user.user_name

            new_mail = Mail(
                user=target_name.user_id,
                recipient=session_user,
                time=datetime.now(),
                status=1,
                category=1,
                login_recipient=user_name,
                title=title,
                message=mail
            )
            new_mail.save()

        mails = Mail.objects.filter(user=session_user).order_by('category', '-time')
        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('id_resource')
        user = MyUser.objects.filter(user_id=session_user).first()
        user_city = UserCity.objects.filter(user=int(session_user)).first()
        user_citys = UserCity.objects.filter(user=int(session_user))
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouses': warehouses, 'user_city': user_city, 'user_citys': user_citys,
                  'mails': mails}
        return render(request, "diplomacy.html", output)