# -*- coding: utf-8 -*-

import math
from datetime import datetime
from my_game.flightplan.create.flight import calculation
from my_game.models import Fleet
from my_game.models import Flightplan, Flightplan_flight
from my_game.models import Fleet_engine


def start_flight(*args):
    fleet_id = args[0]
    fleet = Fleet.objects.filter(id=fleet_id).first()
    fleet_engine = Fleet_engine.objects.filter(fleet_id=fleet_id).first()
    #Повверка наличия топлива в зависимости от варианта полета. Проверка достаточности топлива для полета.
    flightplan = Flightplan.objects.filter(id_fleet=fleet_id).first()
    id_flightplan = flightplan.pk
    flightplan_flight = Flightplan_flight.objects.filter(id_fleet=fleet_id, id_command=flightplan.id_command).first()
    flightplan_flight_id = flightplan_flight.pk

    x1 = int(flightplan_flight.start_x)
    y1 = int(flightplan_flight.start_y)
    z1 = int(flightplan_flight.start_z)
    x2 = int(flightplan_flight.finish_x)
    y2 = int(flightplan_flight.finish_y)
    z2 = int(flightplan_flight.finish_z)

    distance =  math.sqrt((x1-x2)**2 + (y1-y2)**2 +(z1-z2)**2)
    if flightplan_flight.id_command == 1:
        flight_time = int(math.sqrt(distance / 2 * (int(fleet.ship_empty_mass) ) / int(fleet_engine.system_power)) * 2)
    elif flightplan_flight.id_command == 2:
        coordinate_giper = ''
        coordinate_null = ''
    elif flightplan_flight.id_command == 3:
        coordinate_giper = 1
        coordinate_null = ''
    elif flightplan_flight.id_command == 4:
        coordinate_giper = ''
        coordinate_null = 1
    if flightplan_flight.id_command == 2 or flightplan_flight.id_command == 3 or flightplan_flight.id_command == 4:
        answer = calculation(fleet_id, coordinate_giper, coordinate_null, distance)
        flight_time = int(answer['flight_time'])

    if flightplan_flight.flight_time != flight_time:
        new_time = flightplan_flight = Flightplan_flight.objects.filter(id=flightplan_flight.pk).update(flight_time=flight_time)

    if len(args) == 1:
        start_time = datetime.now()
    else:
        start_time = args[1]

    flightplan_flight = Flightplan_flight.objects.filter(id=flightplan_flight_id).update(start_time=start_time)
    flightplan = Flightplan.objects.filter(id=id_flightplan).update(status=1)
    fleet = Fleet.objects.filter(id=fleet_id).update(status=True, planet_status=0)
