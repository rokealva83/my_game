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
from  models import Flightplan, Flightplan_flight, Flightplan_hold, Flightplan_production, Flightplan_refill, \
    Flightplan_repair, Flightplan_scan, Flightplan_fight


def fleet_manage(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        add_ships = {}
        flightplans = {}
        flightplan_flights = {}
        fleet_id = 0
        command = 0
        ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1)
        if request.POST.get('create_fleet'):
            name = request.POST.get('fleet_name')
            user_city = User_city.objects.filter(id=session_user_city).first()
            new_fleet = Fleet(
                user=session_user,
                name=name,
                x=user_city.x,
                y=user_city.y,
                z=user_city.z,
                system=user_city.system_id,
                planet=user_city.planet_id
            )
            new_fleet.save()

        if request.POST.get('navy_ships'):
            add_ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city)
            fleet_id = int(request.POST.get('hidden_fleet'))
            command = 1

        if request.POST.get('add_ship'):
            amount_ship = int(request.POST.get('amount_ship'))
            fleet_id = int(request.POST.get('hidden_fleet'))
            ship_id = int(request.POST.get('hidden_ship'))
            ship = Ship.objects.filter(id=ship_id, user=session_user, fleet_status=0,
                                       place_id=session_user_city).first()
            if amount_ship > 0:
                if int(ship.amount_ship) >= int(amount_ship):
                    ship_fleet = Ship.objects.filter(id_project_ship=ship.id_project_ship, user=session_user,
                                                     fleet_status=1, place_id=fleet_id).first()
                    if ship_fleet:
                        if int(ship.amount_ship) == int(amount_ship):
                            new_amount = int(ship_fleet.amount_ship) + int(amount_ship)
                            ship_fleet = Ship.objects.filter(id_project_ship=ship.id_project_ship, user=session_user,
                                                             fleet_status=1, place_id=fleet_id).update(
                                amount_ship=new_amount)
                            delete_ship = Ship.objects.filter(id=ship_id, user=session_user, fleet_status=0,
                                                              place_id=session_user_city).delete()
                            ship = Ship.objects.filter(place_id=fleet_id, fleet_status=1, user=session_user).first()
                            project_ship = Project_ship.objects.filter(id=ship.id_project_ship).first()
                            fleet = Fleet.objects.filter(id=fleet_id).first()

                            system_power = int(project_ship.system_power) * amount_ship + int(fleet.system_power)
                            intersystem_power = int(
                                project_ship.intersystem_power) * amount_ship + int(fleet.intersystem_power)
                            giper_power = int(project_ship.giper_power) * amount_ship + int(fleet.giper_power)
                            giper_accuracy = int(project_ship.giper_accuracy) * amount_ship + int(fleet.giper_accuracy)
                            null_power = int(project_ship.null_power) * amount_ship + int(fleet.null_power)
                            null_accuracy = int(project_ship.null_accuracy) * amount_ship + int(fleet.null_accuracy)
                            ship_empty_mass = int(project_ship.mass) * amount_ship + int(fleet.ship_empty_mass)
                            fleet = Fleet.objects.filter(user=session_user, id=fleet_id).update(
                                system_power=system_power,
                                intersystem_power=intersystem_power,
                                giper_power=giper_power,
                                giper_accuracy=giper_accuracy,
                                null_power=null_power,
                                null_accuracy=null_accuracy,
                                ship_empty_mass=ship_empty_mass
                            )
                        else:
                            new_amount = int(ship_fleet.amount_ship) + int(amount_ship)
                            ship_fleet = Ship.objects.filter(id_project_ship=ship.id_project_ship, user=session_user,
                                                             fleet_status=1, place_id=fleet_id).update(
                                amount_ship=new_amount)
                            ship = Ship.objects.filter(id=ship_id, user=session_user, fleet_status=0,
                                                       place_id=session_user_city).first()
                            new_amount = int(ship.amount_ship) - int(amount_ship)
                            update_ship = Ship.objects.filter(id=ship_id, user=session_user, fleet_status=0,
                                                              place_id=session_user_city).update(amount_ship=new_amount)

                            ship = Ship.objects.filter(place_id=fleet_id, fleet_status=1, user=session_user).first()
                            project_ship = Project_ship.objects.filter(id=ship.id_project_ship).first()
                            fleet = Fleet.objects.filter(id=fleet_id).first()

                            system_power = int(project_ship.system_power) * amount_ship + int(fleet.system_power)
                            intersystem_power = int(
                                project_ship.intersystem_power) * amount_ship + int(fleet.intersystem_power)
                            giper_power = int(project_ship.giper_power) * amount_ship + int(fleet.giper_power)
                            giper_accuracy = int(project_ship.giper_accuracy) * amount_ship + int(fleet.giper_accuracy)
                            null_power = int(project_ship.null_power) * amount_ship + int(fleet.null_power)
                            null_accuracy = int(project_ship.null_accuracy) * amount_ship + int(fleet.null_accuracy)
                            ship_empty_mass = int(project_ship.mass) * amount_ship + int(fleet.ship_empty_mass)
                            fleet = Fleet.objects.filter(user=session_user, id=fleet_id).update(
                                system_power=system_power,
                                intersystem_power=intersystem_power,
                                giper_power=giper_power,
                                giper_accuracy=giper_accuracy,
                                null_power=null_power,
                                null_accuracy=null_accuracy,
                                ship_empty_mass=ship_empty_mass
                            )
                    else:
                        if int(ship.amount_ship) == int(amount_ship):
                            ship = Ship.objects.filter(id=ship_id, user=session_user, fleet_status=0,
                                                       place_id=session_user_city).update(fleet_status=1,
                                                                                          place_id=fleet_id)
                            ship = Ship.objects.filter(id=ship_id, ).first()
                            project_ship = Project_ship.objects.filter(id=ship.id_project_ship).first()
                            fleet = Fleet.objects.filter(user=session_user, id=fleet_id).update(
                                system_power=int(project_ship.system_power) * amount_ship,
                                intersystem_power=int(project_ship.intersystem_power) * amount_ship,
                                giper_power=int(project_ship.giper_power) * amount_ship,
                                giper_accuracy=int(project_ship.giper_accuracy) * amount_ship,
                                null_power=int(project_ship.null_power) * amount_ship,
                                null_accuracy=int(project_ship.null_accuracy) * amount_ship,
                                ship_empty_mass=int(project_ship.mass) * amount_ship
                            )
                        else:
                            ship = Ship(
                                user=session_user,
                                id_project_ship=ship.id_project_ship,
                                amount_ship=amount_ship,
                                fleet_status=1,
                                place_id=fleet_id,
                                name=ship.name
                            )
                            ship.save()
                            ship = Ship.objects.filter(id=ship_id, user=session_user, fleet_status=0,
                                                       place_id=session_user_city).first()
                            new_amount = int(ship.amount_ship) - int(amount_ship)
                            ship = Ship.objects.filter(id=ship_id, user=session_user, fleet_status=0,
                                                       place_id=session_user_city).update(amount_ship=new_amount)
                            ship = Ship.objects.filter(id=ship_id, user=session_user, fleet_status=0,
                                                       place_id=session_user_city).first()
                            project_ship = Project_ship.objects.filter(id=ship.id_project_ship).first()
                            fleet = Fleet.objects.filter(user=session_user, id=fleet_id).update(
                                system_power=int(project_ship.system_power) * amount_ship,
                                intersystem_power=int(project_ship.intersystem_power) * amount_ship,
                                giper_power=int(project_ship.giper_power) * amount_ship,
                                giper_accuracy=int(project_ship.giper_accuracy) * amount_ship,
                                null_power=int(project_ship.null_power) * amount_ship,
                                null_accuracy=int(project_ship.null_accuracy) * amount_ship,
                                ship_empty_mass=int(project_ship.mass) * amount_ship)
                else:
                    'Недостаточно корблей'
            else:
                message = 'Неверное количество кораблей'
            ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1)

        if request.POST.get('del_ship'):
            amount_ship = int(request.POST.get('amount_ship'))
            fleet_id = int(request.POST.get('hidden_fleet'))
            ship_id = int(request.POST.get('hidden_del_ship'))
            fleet = Fleet.objects.filter(id=fleet_id).first()
            user_city = User_city.objects.filter(user=session_user, x=fleet.x, y=fleet.y, z=fleet.z).first()
            if user_city:
                ship = Ship.objects.filter(user=session_user, id_project_ship=ship_id, place_id=user_city.id,
                                           fleet_status=0).first()
                if ship:
                    new_amount = int(ship.amount_ship) + int(amount_ship)
                    ship = Ship.objects.filter(user=session_user, id_project_ship=ship_id, place_id=user_city.id,
                                               fleet_status=0).update(amount_ship=new_amount)
                    ship = Ship.objects.filter(user=session_user, id_project_ship=ship_id, place_id=fleet_id,
                                               fleet_status=1).first()
                    new_amount = int(ship.amount_ship) - int(amount_ship)
                    if new_amount == 0:
                        ship = Ship.objects.filter(user=session_user, id_project_ship=ship_id, place_id=fleet_id,
                                                   fleet_status=1).delete()
                    else:
                        ship = Ship.objects.filter(user=session_user, id_project_ship=ship_id, place_id=fleet_id,
                                                   fleet_status=1).update(amount_ship=new_amount)

                    fleet = Fleet.objects.filter(user=session_user, id=fleet_id).first()
                    project_ship = Project_ship.objects.filter(id=ship_id).first()

                    system_power = int(fleet.system_power) - int(project_ship.system_power) * amount_ship
                    intersystem_power = int(fleet.intersystem_power) - int(project_ship.intersystem_power) * amount_ship
                    giper_power = int(fleet.giper_power) - int(project_ship.giper_power) * amount_ship
                    giper_accuracy = int(fleet.giper_accuracy) - int(project_ship.giper_accuracy) * amount_ship
                    null_power = int(fleet.null_power) - int(project_ship.null_power) * amount_ship
                    null_accuracy = + int(fleet.null_accuracy) - int(project_ship.null_accuracy) * amount_ship
                    ship_empty_mass = int(fleet.ship_empty_mass) - int(project_ship.mass) * amount_ship
                    fleet = Fleet.objects.filter(user=session_user, id=fleet_id).update(
                        system_power=system_power,
                        intersystem_power=intersystem_power,
                        giper_power=giper_power,
                        giper_accuracy=giper_accuracy,
                        null_power=null_power,
                        null_accuracy=null_accuracy,
                        ship_empty_mass=ship_empty_mass
                    )
                else:
                    project_ship = Project_ship.objects.filter(id=ship_id).first()

                    ship = Ship(
                        user=session_user,
                        id_project_ship=ship_id,
                        amount_ship=amount_ship,
                        fleet_status=0,
                        place_id=user_city.id,
                        name=project_ship.name
                    )
                    ship.save()
                    ship = Ship.objects.filter(user=session_user, id_project_ship=ship_id, place_id=fleet_id,
                                               fleet_status=1).first()
                    new_amount = int(ship.amount_ship) - int(amount_ship)
                    if new_amount == 0:
                        ship = Ship.objects.filter(user=session_user, id_project_ship=ship_id, place_id=fleet_id,
                                                   fleet_status=1).delete()
                    else:
                        ship = Ship.objects.filter(user=session_user, id_project_ship=ship_id, place_id=fleet_id,
                                                   fleet_status=1).update(amount_ship=new_amount)

                    fleet = Fleet.objects.filter(user=session_user, id=fleet_id).first()
                    project_ship = Project_ship.objects.filter(id=ship_id).first()

                    system_power = int(fleet.system_power) - int(project_ship.system_power) * amount_ship
                    intersystem_power = int(fleet.intersystem_power) - int(project_ship.intersystem_power) * amount_ship
                    giper_power = int(fleet.giper_power) - int(project_ship.giper_power) * amount_ship
                    giper_accuracy = int(fleet.giper_accuracy) - int(project_ship.giper_accuracy) * amount_ship
                    null_power = int(fleet.null_power) - int(project_ship.null_power) * amount_ship
                    null_accuracy = + int(fleet.null_accuracy) - int(project_ship.null_accuracy) * amount_ship
                    ship_empty_mass = int(fleet.ship_empty_mass) - int(project_ship.mass) * amount_ship
                    fleet = Fleet.objects.filter(user=session_user, id=fleet_id).update(
                        system_power=system_power,
                        intersystem_power=intersystem_power,
                        giper_power=giper_power,
                        giper_accuracy=giper_accuracy,
                        null_power=null_power,
                        null_accuracy=null_accuracy,
                        ship_empty_mass=ship_empty_mass
                    )
            else:
                message = 'Флот не над планетой'

        if request.POST.get('flight_plan'):
            fleet_id = int(request.POST.get('hidden_fleet'))
            flightplans = Flightplan.objects.filter(user=session_user, id_fleet=fleet_id)
            flightplan_flights = Flightplan_flight.objects.filter(user=session_user, id_fleet=fleet_id)
            command = 3

        warehouse = Warehouse.objects.filter(user=session_user).first()
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = User_city.objects.filter(user=int(session_user))
        user_fleets = Fleet.objects.filter(user=session_user)
        ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1)
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouse': warehouse, 'user_city': user_city, 'user_citys': user_citys,
                  'user_fleets': user_fleets, 'add_ships': add_ships, 'fleet_id': fleet_id, 'ship_fleets': ship_fleets,
                  'command': command, 'flightplans': flightplans, 'flightplan_flights': flightplan_flights}
        return render(request, "space_forces.html", output)


def fleet_fly(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)

        if request.POST.get('add_command'):
            command = 3
            fleet_id = int(request.POST.get('hidden_fleet'))
            city = request.POST.get('city')
            if city:
                planet_system = int(request.POST.get('planet_system'))
                planet_planet = int(request.POST.get('planet_planet'))
                planet_giper = request.POST.get('planet_giper')
                planet_null = request.POST.get('planet_null')
                target_system = System.objects.filter(id=planet_system).first()
                target_planet = Planet.objects.filter(system_id=planet_system, planet_num=planet_planet).first()
                fleet = Fleet.objects.filter(id=fleet_id).first()
                system = System.objects.filter(id=fleet.system).first()
                # XYZ - координаты звезд  xyz - соординаты планет  XxYyZz - межзвездные координаты планет
                if fleet.planet_status == 1:
                    Xx1 = system.x * 1000 + fleet.x
                    Yy1 = system.y * 1000 + fleet.y
                    Zz1 = system.z * 1000 + fleet.z
                else:
                    Xx1 = fleet.x
                    Yy1 = fleet.y
                    Zz1 = fleet.z

                if target_planet:
                    Xx2 = target_system.x * 1000 + target_planet.x
                    Yy2 = target_system.y * 1000 + target_planet.y
                    Zz2 = target_system.z * 1000 + target_planet.z
                else:
                    distance = math.sqrt((Xx1 - target_system.x*1000) ** 2 + (Yy1 - target_system.y*1000) ** 2 + (Zz1 - target_system.z*1000) ** 2)
                    Xx2 = Xx1 + (target_system.x*1000 - Xx1)*(distance-target_system.system_size*1000)/distance
                    Yy2 = Yy1 + (target_system.y*1000 - Yy1)*(distance-target_system.system_size*1000)/distance
                    Zz2 = Zz1 + (target_system.z*1000 - Zz1)*(distance-target_system.system_size*1000)/distance

                distance = math.sqrt((Xx1 - Xx2) ** 2 + (Yy1 - Yy2) ** 2 + (Zz1 - Zz2) ** 2)
                if int(system.id) == planet_system:
                    flight_time = math.sqrt(distance*(fleet.ship_empty_mass + fleet.hold)/fleet.system_power)
                else:
                    if planet_giper:
                        fleet_ships = Ship.objects.filter(place_id = fleet_id, fleet_status = 1)
                        check = 0
                        for fleet_ship in fleet_ships:
                            project_ship = Project_ship.objects.filter(id = fleet_ship.id_project_ship).first()
                            if project_ship.giper_power == 0:
                                check = 1
                        if check == 0:
                            flight_time = math.sqrt(distance*(fleet.ship_empty_mass + fleet.hold)/fleet.giper_power)
                        else:
                            flight_time = math.sqrt(distance*(fleet.ship_empty_mass + fleet.hold)/fleet.intersystem_power)
                    elif planet_null:
                        fleet_ships = Ship.objects.filter(place_id = fleet_id, fleet_status = 1)
                        check = 0
                        for fleet_ship in fleet_ships:
                            project_ship = Project_ship.objects.filter(id = fleet_ship.id_project_ship).first()
                            if project_ship.giper_power == 0:
                                check = 1
                        if check == 0:
                            flight_time = math.sqrt(distance*(fleet.ship_empty_mass + fleet.hold)/fleet.giper_power)
                        else:
                            flight_time = math.sqrt(distance*(fleet.ship_empty_mass + fleet.hold)/fleet.intersystem_power)
                    else:
                        flight_time = math.sqrt(distance*(fleet.ship_empty_mass + fleet.hold)/fleet.intersystem_power)



            coordinate = request.POST.get('coordinate')
            if coordinate:
                coordinate_x = request.POST.get('coordinate_x')
                coordinate_y = request.POST.get('coordinate_y')
                coordinate_z = request.POST.get('coordinate_z')
                coordinate_giper = request.POST.get('coordinate_giper')
                coordinate_null = request.POST.get('coordinate_null')
                coordinate_system = request.POST.get('')
                coordinate_intersystem = request.POST.get('coordinate_intersystem')
                fleet = Fleet.objects.filter(id=fleet_id).first()

        warehouse = Warehouse.objects.filter(user=session_user).first()
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = User_city.objects.filter(user=int(session_user))
        user_fleets = Fleet.objects.filter(user=session_user)
        ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1)
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouse': warehouse, 'user_city': user_city, 'user_citys': user_citys,
                  'user_fleets': user_fleets, 'fleet_id': fleet_id, 'ship_fleets': ship_fleets,
                  'command': command}
        return render(request, "space_forces.html", output)