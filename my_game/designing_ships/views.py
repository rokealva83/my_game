# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from django.shortcuts import render
from my_game.models import MyUser, User_city, Warehouse
from my_game.models import Hull_pattern, Shield_pattern, Generator_pattern, Engine_pattern, \
    Armor_pattern, Module_pattern, Weapon_pattern
from my_game.models import Warehouse_element
from my_game import function
from my_game.models import Project_ship, Element_ship, Turn_ship_build


def designingships(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        warehouse = Warehouse.objects.filter(user=session_user).first()
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = User_city.objects.filter(user=int(session_user))
        hulls = Hull_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')
        project_ships = Project_ship.objects.filter(user=session_user).order_by('id')
        turn_ship_builds = Turn_ship_build.objects.filter(user=session_user, user_city=session_user_city)
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouse': warehouse, 'user_city': user_city, 'user_citys': user_citys,
                  'hulls': hulls, 'project_ships': project_ships, 'turn_ship_builds': turn_ship_builds}
        return render(request, "designingships.html", output)
