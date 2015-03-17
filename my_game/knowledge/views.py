# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, User_city, Warehouse, User_scientic
from my_game.models import Turn_scientic
from my_game import function
from my_game.knowledge import scientic_work


def knowledge(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        warehouses = Warehouse.objects.filter(user=session_user, user_city = session_user_city).order_by('id_resource')
        user_city = User_city.objects.filter(user=session_user).first()
        scientic = User_scientic.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        turn_scientics = Turn_scientic.objects.filter(user=session_user)
        user_citys = User_city.objects.filter(user=int(session_user))
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'scientic': scientic, 'warehouses': warehouses, 'user_city': user_city,
                  'turn_scientics': turn_scientics, 'user_citys': user_citys}
        return render(request, "scientic.html", output)


def study(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        if request.method == "POST":
            level_up = int(request.POST.get("scient"))
            scientic = int(request.POST.get("name_scient"))
            scientic_work.scien_up(session_user, level_up, scientic, session_user_city)
        warehouses = Warehouse.objects.filter(user=session_user, user_city = session_user_city).order_by('id_resource')
        user = MyUser.objects.filter(user_id=session_user).first()
        user_city = User_city.objects.filter(user=session_user).first()
        scientic = User_scientic.objects.filter(user=session_user).first()
        turn_scientics = Turn_scientic.objects.filter(user=session_user)
        user_citys = User_city.objects.filter(user=int(session_user))
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'scientic': scientic, 'warehouses': warehouses, 'user_city': user_city,
                  'turn_scientics': turn_scientics, 'user_citys': user_citys}
        return render(request, "scientic.html", output)