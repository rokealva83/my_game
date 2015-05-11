# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, User_city, Warehouse
from my_game.models import Factory_installed
from my_game.models import Manufacturing_complex
from my_game import function


def factory(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        factory_installeds = Factory_installed.objects.filter(user=session_user, user_city=session_user_city,
                                                              complex_status=0).order_by(
            'production_class', 'production_id')
        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('id_resource')
        manufacturing_complexs = Manufacturing_complex.objects.filter(user=session_user, user_city=session_user_city)
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = User_city.objects.filter(user=int(session_user))
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouses': warehouses, 'user_city': user_city, 'user_citys': user_citys,
                  'manufacturing_complexs': manufacturing_complexs, 'factory_installeds': factory_installeds}
        return render(request, "factory.html", output)