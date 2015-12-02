# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity, Warehouse, UserScientic
from my_game.models import TurnScientic
from my_game import function
from my_game.knowledge.scien_up import scien_up


def knowledge(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        function.check_all_queues(session_user)
        scientic = UserScientic.objects.filter(user=session_user).first()
        turn_scientics = TurnScientic.objects.filter(user=session_user)
        user_citys = UserCity.objects.filter(user=session_user)
        request.session['user'] = session_user.id
        request.session['user_city'] = session_user_city.id
        request.session['live'] = True
        output = {'user': session_user, 'scientic': scientic, 'warehouse': session_user_city.warehouse,
                  'user_city': session_user_city, 'turn_scientics': turn_scientics, 'user_citys': user_citys}
        return render(request, "scientic.html", output)


def study(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        function.check_all_queues(session_user)
        if request.method == "POST":
            level_up = int(request.POST.get("scient"))
            scientic = int(request.POST.get("name_scient"))
            scien_up(session_user, level_up, scientic, session_user_city)
        scientic = UserScientic.objects.filter(user=session_user).first()
        turn_scientics = TurnScientic.objects.filter(user=session_user)
        user_citys = UserCity.objects.filter(user=session_user)
        request.session['userid'] = session_user.id
        request.session['user_city'] = session_user_city.id
        request.session['live'] = True
        output = {'user': session_user, 'scientic': scientic, 'warehouse': session_user_city.warehouse,
                  'user_city': session_user_city, 'turn_scientics': turn_scientics, 'user_citys': user_citys}
        return render(request, "scientic.html", output)
