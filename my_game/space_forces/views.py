# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity, Warehouse
from my_game import function
from my_game.models import Ship, Fleet


def space_forces(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('resource_id')
        user_city = UserCity.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = UserCity.objects.filter(user=int(session_user))
        user_fleets = Fleet.objects.filter(user=session_user)
        ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city)
        ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1)
        command = 0
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouses': warehouses, 'user_city': user_city, 'user_citys': user_citys,
                  'user_fleets': user_fleets, 'ships': ships, 'ship_fleets': ship_fleets, 'command': command}
        return render(request, "space_forces.html", output)