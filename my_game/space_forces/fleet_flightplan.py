# -*- coding: utf-8 -*-

import math
from datetime import datetime

from django.shortcuts import render

from my_game.models import System
from my_game.models import MyUser, User_city
from my_game.models import Warehouse
from my_game import function
from my_game.models import Project_ship, Ship, Fleet, Fleet_parametr_scan, Fleet_engine, \
    Fleet_parametr_resource_extraction
from my_game.models import Flightplan, Flightplan_flight, Flightplan_scan, Flightplan_production
from space_forces import flight


def fleet_flightplan(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        fleet_id = int(request.POST.get('hidden_fleet'))
        fleet_engine = Fleet_engine.objects.filter(fleet_id=fleet_id).first()
        fleet = Fleet.objects.filter(id=fleet_id).first()
        command = 0
        if request.POST.get('add_command'):
            command = 3
            answer = request

            city = request.POST.get('city')
            coordinate = request.POST.get('coordinate')
            if city or coordinate:
                flight.flight_system(session_user, session_user_city, answer)


            resource_extraction = request.POST.get('resource_extraction')
            if resource_extraction:
                time_extraction = request.POST.get('time_extraction')
                full_hold = request.POST.get('full_hold')

                fleet_parametr_resource_extraction = Fleet_parametr_resource_extraction.objects.filter(
                    fleet_id=fleet_id).first()
                if full_hold:
                    time_extraction = int(fleet.empty_hold / fleet_parametr_resource_extraction.extraction_per_minute)

                flightplan = Flightplan(
                    user=session_user,
                    id_fleet=fleet_id,
                    class_command=3,
                    id_command=1,
                    status=0
                )
                flightplan.save()

                flightplan_production = Flightplan_production(
                    user=session_user,
                    id_fleet=fleet_id,
                    id_fleetplan=flightplan.id,
                    id_command=1,
                    production_per_minute=fleet_parametr_resource_extraction.extraction_per_minute,
                    time_extraction=time_extraction
                )
                flightplan_production.save()

            scan = request.POST.get('scan')
            if scan:
                method_scanning = int(request.POST.get('scaning'))
                fleet_parametr_scan = Fleet_parametr_scan.objects.filter(fleet_id=fleet_id,
                                                                         method_scanning=method_scanning).first()
                flightplan = Flightplan(
                    user=session_user,
                    id_fleet=fleet_id,
                    class_command=6,
                    id_command=method_scanning,
                    status=0
                )
                flightplan.save()

                flightplan_scan = Flightplan_scan(
                    user=session_user,
                    id_fleet=fleet_id,
                    id_command=method_scanning,
                    range_scanning=fleet_parametr_scan.range_scanning,
                    start_time=datetime.now(),
                    time_scanning=fleet_parametr_scan.time_scanning,
                    id_fleetplan=flightplan.id
                )
                flightplan_scan.save()

        if request.POST.get('delete_command'):
            command = 3
            fleet_id = int(request.POST.get('hidden_fleet'))
            hidden_flightplan_id = int(request.POST.get('hidden_flightplan_id'))
            flightplan = Flightplan.objects.filter(id=hidden_flightplan_id).first()
            if flightplan.class_command == 1:
                flightplan_flight = Flightplan_flight.objects.filter(id_fleetplan=flightplan.id).delete()
            if flightplan.class_command == 3:
                flightplan_scan = Flightplan_scan.objects.filter(id_fleetplan=flightplan.id).delete()
            if flightplan.class_command == 6:
                flightplan_production = Flightplan_production.objects.filter(id_fleetplan=flightplan.id).delete()
            flightplan = Flightplan.objects.filter(id=hidden_flightplan_id).delete()

        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('id_resource')
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = User_city.objects.filter(user=int(session_user))
        user_fleets = Fleet.objects.filter(user=session_user)
        ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1)
        flightplans = Flightplan.objects.filter(id_fleet=fleet_id)
        flightplan_flights = Flightplan_flight.objects.filter(id_fleet=fleet_id)
        flightplan_scans = Flightplan_scan.objects.filter(id_fleet=fleet_id)
        flightplan_productions = Flightplan_production.objects.filter(id_fleet=fleet_id)
        fleet_engine = Fleet_engine.objects.filter(fleet_id=fleet_id).first()
        fleet_parametr_scans = Fleet_parametr_scan.objects.filter(fleet_id=fleet_id)
        fleet_parametr_resource_extraction = Fleet_parametr_resource_extraction.objects.filter(
            fleet_id=fleet_id).first()

        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouses': warehouses, 'user_city': user_city, 'user_citys': user_citys,
                  'user_fleets': user_fleets, 'fleet_id': fleet_id, 'ship_fleets': ship_fleets,
                  'command': command, 'flightplans': flightplans, 'flightplan_flights': flightplan_flights,
                  'flightplan_scans': flightplan_scans, 'flightplan_productions': flightplan_productions,
                  'fleet_engine': fleet_engine, 'fleet_parametr_scans': fleet_parametr_scans,
                  'fleet_parametr_resource_extraction': fleet_parametr_resource_extraction}
        return render(request, "flightplan.html", output)
