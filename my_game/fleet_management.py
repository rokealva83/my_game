# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.template import Context
import math
import random
import sys
import string
from datetime import datetime, timedelta, date, time as dt_time
import time
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.contrib.sessions.models import Session
from django.utils import timezone
from models import Galaxy, System, Planet
from models import MyUser, User_city, Race, User_scientic
from models import Warehouse
from models import Basic_scientic, Turn_scientic, Basic_armor, Basic_engine, Basic_factory, Basic_generator, \
    Basic_hull, Basic_module, Basic_shell, Basic_shield, Basic_weapon, Turn_building, Turn_assembly_pieces, \
    Turn_production
from models import Hull_pattern, Shell_pattern, Shield_pattern, Generator_pattern, Engine_pattern, \
    Armor_pattern, Module_pattern, Factory_pattern, Weapon_pattern, Factory_installed
from models import Warehouse_factory, Warehouse_element, Warehouse_ship, Warehouse
import function
import scientic_func
import verification_func
from models import User_variables
from models import Project_ship, Element_ship, Turn_ship_build, Ship, Fleet


def fleet_manage(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        add_ships = {}
        fleet_id = 0
        ship_fleets = Ship.objects.filter(user= session_user, fleet_status = 1)
        if request.POST.get('create_fleet'):
            name = request.POST.get('fleet_name')
            user_city = User_city.objects.filter(id = session_user_city).first()
            new_fleet = Fleet(
                user = session_user,
                name = name,
                x = user_city.x,
                y = user_city.y,
                z = user_city.z
            )
            new_fleet.save()

        if request.POST.get('navy_ships'):
            add_ships = Ship.objects.filter(user = session_user, fleet_status = 0, place_id = session_user_city)
            fleet_id = request.POST.get('hidden_fleet')


        if request.POST.get('add_ship'):
            amount_ship = request.POST.get('amount_ship')
            fleet_id = request.POST.get('hidden_fleet')
            ship_id = request.POST.get('hidden_ship')
            ship = Ship.objects.filter(id = ship_id, user= session_user, fleet_status = 0, place_id = session_user_city).first()
            if int(ship.amount_ship) >= int(amount_ship):
                ship_fleet = Ship.objects.filter(id_project_ship = ship.id_project_ship, user= session_user, fleet_status = 1, place_id = fleet_id).first()
                if ship_fleet:
                    if int(ship.amount_ship) == int(amount_ship):
                        new_amount = int(ship_fleet.amount_ship) + int(amount_ship)
                        ship_fleet = Ship.objects.filter(id_project_ship = ship.id_project_ship, user= session_user, fleet_status = 1, place_id = fleet_id).update(amount_ship = new_amount)
                        ship = Ship.objects.filter(id = ship_id, user= session_user, fleet_status = 0, place_id = session_user_city).delete()
                    else:
                        new_amount = int(ship_fleet.amount_ship) + int(amount_ship)
                        ship_fleet = Ship.objects.filter(id_project_ship = ship.id_project_ship, user= session_user, fleet_status = 1, place_id = fleet_id).update(amount_ship = new_amount)
                        ship = Ship.objects.filter(id = ship_id, user= session_user, fleet_status = 0, place_id = session_user_city).first()
                        new_amount = int(ship.amount_ship) - int(amount_ship)
                        ship = Ship.objects.filter(id = ship_id, user= session_user, fleet_status = 0, place_id = session_user_city).update(amount_ship = new_amount)

                else:
                    if int(ship.amount_ship) == int(amount_ship):
                        ship = Ship.objects.filter(id = ship_id, user= session_user, fleet_status = 0, place_id = session_user_city).update(fleet_status = 1, place_id = fleet_id)
                    else:
                        ship = Ship(
                            user = session_user,
                            id_project_ship = ship.id_project_ship,
                            amount_ship = amount_ship,
                            fleet_status = 1,
                            place_id = fleet_id,
                            name = ship.name
                        )
                        ship.save()
                        ship = Ship.objects.filter(id = ship_id, user= session_user, fleet_status = 0, place_id = session_user_city).first()
                        new_amount = int(ship.amount_ship) - int(amount_ship)
                        ship = Ship.objects.filter(id = ship_id, user= session_user, fleet_status = 0, place_id = session_user_city).update(amount_ship = new_amount)
            ship_fleets = Ship.objects.filter(user= session_user, fleet_status = 1)

        warehouse = Warehouse.objects.filter(user=session_user).first()
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = User_city.objects.filter(user=int(session_user))
        user_fleets = Fleet.objects.filter(user=session_user)
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouse': warehouse, 'user_city': user_city, 'user_citys': user_citys,
                  'user_fleets': user_fleets, 'add_ships': add_ships, 'fleet_id': fleet_id, 'ship_fleets':ship_fleets}
        return render(request, "space_forces.html", output)
