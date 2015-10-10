# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity, Warehouse
from my_game import function
from my_game.models import Mail


def remove_mail(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        full_request = request
        mail_dict = full_request.POST
        mail_dict = mail_dict.items()
        mail_tuple = mail_dict[2]
        element_remove = mail_tuple[0]
        id_remove = mail_tuple[1]
        if element_remove == 'remove':
            mail = Mail.objects.filter(id=id_remove).delete()
        elif element_remove == 'remove_all':
            mail = Mail.objects.filter(user=session_user, category=id_remove).delete()

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