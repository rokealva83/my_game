# -*- coding: utf-8 -*-

import math
from datetime import datetime, timedelta
from django.shortcuts import render
from my_game.models import System, Planet, Asteroid_field
from my_game.models import MyUser, User_city
from my_game.models import Warehouse
from my_game import function
from my_game.models import Project_ship, Ship, Fleet, Fleet_parametr_scan, Fleet_energy_power, Fleet_engine
from  my_game.models import Flightplan, Flightplan_flight, Flightplan_scan, Flightplan_hold


def fleet_flightplan(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        fleet_id = int(request.POST.get('hidden_fleet'))
        command = 0
        if request.POST.get('add_command'):
            command = 3
            city = request.POST.get('city')
            if city:
                planet_system = int(request.POST.get('planet_system'))
                planet_planet = int(request.POST.get('planet_planet'))
                planet_giper = request.POST.get('planet_giper')
                planet_null = request.POST.get('planet_null')
                target_system = System.objects.filter(id=planet_system).first()
                target_planet = Planet.objects.filter(system_id=planet_system, planet_num=planet_planet).first()
                fleet = Fleet.objects.filter(id=fleet_id).first()
                fleet_engine = Fleet_engine.objects.filter(fleet_id=fleet_id).first()
                fleet_energy_power = Fleet_energy_power.objects.filter(fleet_id=fleet_id).first()
                system = System.objects.filter(id=fleet.system).first()
                # XYZ - координаты звезд  xyz - соординаты планет  XxYyZz - межзвездные координаты планет
                flightplan_flight = Flightplan_flight.objects.filter(id_fleet=fleet_id).last()
                if flightplan_flight:
                    Xx1 = flightplan_flight.finish_x
                    Yy1 = flightplan_flight.finish_y
                    Zz1 = flightplan_flight.finish_z
                else:
                    if fleet.planet_status == 1:
                        system = System.objects.filter(id=fleet.system).first()
                        Xx1 = int(system.x) * 1000 + int(fleet.x)
                        Yy1 = int(system.y) * 1000 + int(fleet.y)
                        Zz1 = int(system.z) * 1000 + int(fleet.z)
                    else:
                        Xx1 = int(fleet.x) * 1000
                        Yy1 = int(fleet.y) * 1000
                        Zz1 = int(fleet.z) * 1000

                if target_planet:
                    Xx2 = int(target_system.x) * 1000 + int(target_planet.x)
                    Yy2 = int(target_system.y) * 1000 + int(target_planet.y)
                    Zz2 = int(target_system.z) * 1000 + int(target_planet.z)
                else:
                    distance = math.sqrt(
                        (Xx1 - int(target_system.x) * 1000) ** 2 + (Yy1 - int(target_system.y) * 1000) ** 2 + (
                            Zz1 - int(target_system.z) * 1000) ** 2)
                    Xx2 = Xx1 + (int(target_system.x) * 1000 - Xx1) * (
                        distance - int(target_system.system_size) * 1000) / distance
                    Yy2 = Yy1 + (int(target_system.y) * 1000 - Yy1) * (
                        distance - int(target_system.system_size) * 1000) / distance
                    Zz2 = Zz1 + (int(target_system.z) * 1000 - Zz1) * (
                        distance - int(target_system.system_size) * 1000) / distance

                distance = math.sqrt((Xx1 - Xx2) ** 2 + (Yy1 - Yy2) ** 2 + (Zz1 - Zz2) ** 2)

                if fleet.system != 0:
                    System.objects.filter(id=fleet.system).first()
                else:
                    flightplan_flight = Flightplan_flight.objects.filter(id_fleet=fleet_id).last()
                    if flightplan_flight:
                        system = flightplan_flight.system

                if system:
                    if int(system.id) == planet_system:
                        flight_time = math.sqrt(
                            distance / 2 * (int(fleet.ship_empty_mass) ) / int(fleet_engine.system_power)) * 2
                        id_command = 1
                    else:
                        if planet_giper:
                            fleet_ships = Ship.objects.filter(place_id=fleet_id, fleet_status=1)
                            check = 0
                            for fleet_ship in fleet_ships:
                                project_ship = Project_ship.objects.filter(id=fleet_ship.id_project_ship).first()
                                if project_ship.giper_power == 0:
                                    check = 1
                            if check == 0:
                                flight_time = math.sqrt(
                                    distance * 2 * (int(fleet.ship_empty_mass) ) / int(fleet_engine.giper_power)) * 2
                                id_command = 3
                            else:
                                flight_time = math.sqrt(
                                    distance / 2 * (int(fleet.ship_empty_mass) ) / int(fleet_engine.intersystem_power)) * 2
                                id_command = 2
                        elif planet_null:
                            fleet_ships = Ship.objects.filter(place_id=fleet_id, fleet_status=1)
                            check = 0
                            for fleet_ship in fleet_ships:
                                project_ship = Project_ship.objects.filter(id=fleet_ship.id_project_ship).first()
                                if project_ship.giper_power == 0:
                                    check = 1
                            if check == 0:
                                flight_time = math.sqrt(
                                    distance / 2 * (int(fleet.ship_empty_mass) ) / int(fleet_engine.null_power)) * 2
                                id_command = 4
                            else:
                                flight_time = math.sqrt(
                                    distance / 2 * (int(fleet.ship_empty_mass) ) / int(fleet_engine.intersystem_power)) * 2
                                id_command = 2
                        else:
                            flight_time = math.sqrt(
                                distance / 2 * (int(fleet.ship_empty_mass) ) / int(fleet_engine.intersystem_power)) * 2
                            id_command = 2
                else:
                    if planet_giper:
                        fleet_ships = Ship.objects.filter(place_id=fleet_id, fleet_status=1)
                        check = 0
                        for fleet_ship in fleet_ships:
                            project_ship = Project_ship.objects.filter(id=fleet_ship.id_project_ship).first()
                            if project_ship.giper_power == 0:
                                check = 1
                        if check == 0:
                            flight_time = math.sqrt(
                                distance * 2 * (int(fleet.ship_empty_mass) ) / int(fleet_engine.giper_power)) * 2
                            id_command = 3
                        else:
                            flight_time = math.sqrt(
                                distance / 2 * (int(fleet.ship_empty_mass) ) / int(fleet_engine.intersystem_power)) * 2
                            id_command = 2
                    elif planet_null:
                        fleet_ships = Ship.objects.filter(place_id=fleet_id, fleet_status=1)
                        check = 0
                        for fleet_ship in fleet_ships:
                            project_ship = Project_ship.objects.filter(id=fleet_ship.id_project_ship).first()
                            if project_ship.giper_power == 0:
                                check = 1
                        if check == 0:
                            flight_time = math.sqrt(
                                distance / 2 * (int(fleet.ship_empty_mass) ) / int(fleet_engine.null_power)) * 2
                            id_command = 4
                        else:
                            flight_time = math.sqrt(
                                distance / 2 * (int(fleet.ship_empty_mass) ) / int(fleet_engine.intersystem_power)) * 2
                            id_command = 2
                    else:
                        flight_time = math.sqrt(
                            distance / 2 * (int(fleet.ship_empty_mass) ) / int(fleet_engine.intersystem_power)) * 2
                        id_command = 2

                flightplan = Flightplan(
                    user=session_user,
                    id_fleet=fleet_id,
                    class_command=1,
                    id_command=id_command,
                    status=0,
                )
                flightplan.save()
                id_fleetplan = flightplan.pk
                flightplan_flight = Flightplan_flight(
                    user=session_user,
                    id_fleet=fleet_id,
                    id_fleetplan=id_fleetplan,
                    id_command=id_command,
                    start_x=Xx1,
                    start_y=Yy1,
                    start_z=Zz1,
                    finish_x=int(Xx2),
                    finish_y=int(Yy2),
                    finish_z=int(Zz2),
                    flight_time=flight_time,
                    planet=planet_planet,
                    system=planet_system
                )
                flightplan_flight.save()

            coordinate = request.POST.get('coordinate')
            if coordinate:
                coordinate_x = float(request.POST.get('coordinate_x'))
                coordinate_y = float(request.POST.get('coordinate_y'))
                coordinate_z = float(request.POST.get('coordinate_z'))
                coordinate_giper = request.POST.get('coordinate_giper')
                coordinate_null = request.POST.get('coordinate_null')
                coordinate_system = int(request.POST.get('coordinate_system'))
                coordinate_intersystem = request.POST.get('coordinate_intersystem')
                fleet = Fleet.objects.filter(id=fleet_id).first()
                system = System.objects.filter(id=fleet.system).first()
                flightplan_flight = Flightplan_flight.objects.filter(id_fleet=fleet_id).last()

                if flightplan_flight:
                    Xx1 = flightplan_flight.finish_x
                    Yy1 = flightplan_flight.finish_y
                    Zz1 = flightplan_flight.finish_z
                else:
                    if fleet.planet_status == 1:
                        system = System.objects.filter(id=fleet.system).first()
                        Xx1 = int(system.x) * 1000 + int(fleet.x)
                        Yy1 = int(system.y) * 1000 + int(fleet.y)
                        Zz1 = int(system.z) * 1000 + int(fleet.z)
                    else:
                        Xx1 = int(fleet.x) * 1000
                        Yy1 = int(fleet.y) * 1000
                        Zz1 = int(fleet.z) * 1000

                if coordinate_intersystem:
                    Xx2 = coordinate_x * 1000
                    Yy2 = coordinate_y * 1000
                    Zz2 = coordinate_z * 1000
                    distance = math.sqrt((Xx1 - Xx2) ** 2 + (Yy1 - Yy2) ** 2 + (Zz1 - Zz2) ** 2)
                else:
                    target_system = System.objects.filter(id=coordinate_system).first()
                    Xx2 = int(target_system.x) * 1000 + coordinate_x
                    Yy2 = int(target_system.y) * 1000 + coordinate_y
                    Zz2 = int(target_system.z) * 1000 + coordinate_z
                    distance = math.sqrt((Xx1 - Xx2) ** 2 + (Yy1 - Yy2) ** 2 + (Zz1 - Zz2) ** 2)

                if coordinate_system == fleet.system:
                    flight_time = math.sqrt(distance / 2 * (int(fleet.ship_empty_mass) ) / int(fleet_engine.system_power)) * 2
                    id_command = 1
                else:
                    if coordinate_giper:
                        fleet_ships = Ship.objects.filter(place_id=fleet_id, fleet_status=1)
                        check = 0
                        for fleet_ship in fleet_ships:
                            project_ship = Project_ship.objects.filter(id=fleet_ship.id_project_ship).first()
                            if project_ship.giper_power == 0:
                                check = 1
                        if check == 0:
                            flight_time = math.sqrt(
                                distance / 2 * (int(fleet.ship_empty_mass) ) / int(fleet_engine.giper_power)) * 2
                            id_command = 3
                        else:
                            flight_time = math.sqrt(
                                distance / 2 * (int(fleet.ship_empty_mass) ) / int(fleet_engine.intersystem_power)) * 2
                            id_command = 2
                    elif coordinate_null:
                        fleet_ships = Ship.objects.filter(place_id=fleet_id, fleet_status=1)
                        check = 0
                        for fleet_ship in fleet_ships:
                            project_ship = Project_ship.objects.filter(id=fleet_ship.id_project_ship).first()
                            if project_ship.giper_power == 0:
                                check = 1
                        if check == 0:
                            flight_time = math.sqrt(
                                distance / 2 * (int(fleet.ship_empty_mass) ) / int(fleet_engine.null_power)) * 2
                            id_command = 4
                        else:
                            flight_time = math.sqrt(
                                distance / 2 * (int(fleet.ship_empty_mass) ) / int(fleet_engine.intersystem_power)) * 2
                            id_command = 2
                    else:
                        flight_time = math.sqrt(
                            distance / 2 * (int(fleet.ship_empty_mass) ) / int(fleet_engine.intersystem_power)) * 2
                        id_command = 2

                flightplan = Flightplan(
                    user=session_user,
                    id_fleet=fleet_id,
                    class_command=1,
                    id_command=id_command,
                    status=0,
                )
                flightplan.save()
                id_fleetplan = flightplan.pk
                flightplan_flight = Flightplan_flight(
                    user=session_user,
                    id_fleet=fleet_id,
                    id_fleetplan=id_fleetplan,
                    id_command=id_command,
                    start_x=Xx1,
                    start_y=Yy1,
                    start_z=Zz1,
                    finish_x=Xx2,
                    finish_y=Yy2,
                    finish_z=Zz2,
                    flight_time=flight_time,
                    planet=0,
                    system=0,
                )
                flightplan_flight.save()

            resource_extraction = request.POST.get('resource_extraction')
            if resource_extraction:
                a =1

            scan = request.POST.get('scan')
            if scan:
                method_scanning = int(request.POST.get('scaning'))

                fleet_parametr_scan = Fleet_parametr_scan.objects.filter(fleet_id=fleet_id, method_scanning = method_scanning).first()

                flightplan = Flightplan(
                    user = session_user,
                    id_fleet = fleet_id,
                    class_command = 6,
                    id_command = method_scanning,
                    status = 0
                )
                flightplan.save()

                flightplan_scan = Flightplan_scan(
                    user = session_user,
                    id_fleet = fleet_id,
                    id_command = method_scanning,
                    range_scanning = fleet_parametr_scan.range_scanning,
                    start_time = datetime.now(),
                    time_scaning = fleet_parametr_scan.time_scanning,
                    id_fleetplan = flightplan.id
                )
                flightplan_scan.save()

        if request.POST.get('delete_command'):
            command = 3
            fleet_id = int(request.POST.get('hidden_fleet'))
            hidden_flightplan_id = int(request.POST.get('hidden_flightplan_id'))
            flightplan = Flightplan.objects.filter(id=hidden_flightplan_id).first()
            if flightplan.class_command == 1:
                flightplan_flight = Flightplan_flight.objects.filter(id_fleetplan=flightplan.id).delete()
            flightplan = Flightplan.objects.filter(id=hidden_flightplan_id).delete()

        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('id_resource')
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = User_city.objects.filter(user=int(session_user))
        user_fleets = Fleet.objects.filter(user=session_user)
        ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1)
        flightplans = Flightplan.objects.filter(id_fleet=fleet_id)
        flightplan_flights = Flightplan_flight.objects.filter(id_fleet=fleet_id)
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouses': warehouses, 'user_city': user_city, 'user_citys': user_citys,
                  'user_fleets': user_fleets, 'fleet_id': fleet_id, 'ship_fleets': ship_fleets,
                  'command': command, 'flightplans': flightplans, 'flightplan_flights': flightplan_flights,
                  'mail': mail, 'ast_mail': ast_mail}
        return render(request, "test.html", output)
