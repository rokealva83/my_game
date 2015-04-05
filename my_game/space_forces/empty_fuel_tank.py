# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, User_city
from my_game.models import Warehouse, Warehouse_element, Warehouse_factory, Warehouse_ship, Basic_resource
from my_game import function
from my_game.models import Project_ship, Ship, Fleet, Hold
from my_game.models import Flightplan, Flightplan_flight
from my_game.models import Factory_pattern, Hull_pattern, Armor_pattern, Shell_pattern, Shield_pattern, \
    Generator_pattern, Weapon_pattern, Engine_pattern, Module_pattern

def empty_fuel_tank(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)