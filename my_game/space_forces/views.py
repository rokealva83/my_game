# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity
from my_game import function
from my_game.models import Ship, Fleet


def space_forces(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        function.check_all_queues(session_user)
        user_citys = UserCity.objects.filter(user=session_user).all()
        user_fleets = Fleet.objects.filter(user=session_user).all()
        ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city.id).all()
        ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1).all()
        command = 0
        request.session['user'] = session_user.id
        request.session['user_city'] = session_user_city.id
        request.session['live'] = True
        output = {'user': session_user, 'warehouse': session_user_city.warehouse, 'user_city': session_user_city,
                  'user_citys': user_citys, 'user_fleets': user_fleets, 'ships': ships, 'ship_fleets': ship_fleets,
                  'command': command}
        return render(request, "space_forces.html", output)
