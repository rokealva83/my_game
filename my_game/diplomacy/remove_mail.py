# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity, Warehouse
from my_game import function
from my_game.models import Mail


def remove_mail(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        function.check_all_queues(session_user)
        full_request = request
        mail_dict = full_request.POST
        mail_dict = mail_dict.items()
        mail_tuple = mail_dict[2]
        element_remove = mail_tuple[0]
        remove_mail_id = mail_tuple[1]
        if element_remove == 'remove':
            Mail.objects.filter(id=remove_mail_id).delete()
        elif element_remove == 'remove_all':
            Mail.objects.filter(user=session_user, category=remove_mail_id).delete()
        mails = Mail.objects.filter(user=session_user).order_by('category', '-time')
        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('resource_id')
        user_citys = UserCity.objects.filter(user=session_user)
        request.session['user'] = session_user.id
        request.session['user_city'] = session_user_city.id
        request.session['live'] = True
        output = {'user': session_user, 'warehouses': warehouses, 'user_city': session_user_city,
                  'user_citys': user_citys, 'mails': mails}
        return render(request, "diplomacy.html", output)
