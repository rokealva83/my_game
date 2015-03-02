# -*- coding: utf-8 -*-


from datetime import datetime, timedelta
from django.shortcuts import render
from my_game.models import MyUser, User_city
from my_game.models import Warehouse
from my_game import function
from my_game.models import Ship, Fleet
from my_game.models import Flightplan, Flightplan_flight



def start_flight(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        command = 0
        if request.POST.get('start_flight'):
            fleet_id = int(request.POST.get('hidden_fleet'))
            flightplan = Flightplan.objects.filter(id_fleet=fleet_id).first()
            id_flightplan = flightplan.pk
            if flightplan.class_command == 1:
                flightplan_flight = Flightplan_flight.objects.filter(id_fleet=fleet_id,
                                                                     id_command=flightplan.id_command).first()
                start_time = datetime.now()
                finish_time = start_time + timedelta(seconds=flightplan_flight.flight_time)
                flightplan_flight = Flightplan_flight.objects.filter(id_fleet=fleet_id,
                                                                     id_command=flightplan.id_command).update(
                    start_time=start_time, finish_time=finish_time)

            flightplan = Flightplan.objects.filter(id=id_flightplan, id_fleet=fleet_id).update(status=1)
            fleet = Fleet.objects.filter(id=fleet_id).update(status=True, planet_status=0)
            command = 0

        if request.POST.get('delete_list'):
            fleet_id = int(request.POST.get('hidden_fleet'))
            flightplan = Flightplan.objects.filter(id_fleet=fleet_id).delete()
            flightplan_flight = Flightplan_flight.objects.filter(id_fleet=fleet_id).delete()
            command = 3

        warehouse = Warehouse.objects.filter(user=session_user).first()
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
        output = {'user': user, 'warehouse': warehouse, 'user_city': user_city, 'user_citys': user_citys,
                  'user_fleets': user_fleets, 'fleet_id': fleet_id, 'ship_fleets': ship_fleets,
                  'command': command, 'flightplans': flightplans, 'flightplan_flights': flightplan_flights}
        return render(request, "space_forces.html", output)
