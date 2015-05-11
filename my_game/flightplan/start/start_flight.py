# -*- coding: utf-8 -*-

import math
from datetime import datetime
from my_game.models import Fleet, Fleet_energy_power, Fuel_tank, Fuel_pattern
from my_game.models import Flightplan, Flightplan_flight
from my_game.models import Fleet_engine
from my_game.flightplan import fuel


def start_flight(*args):
    fleet_id = args[0]
    fleet = Fleet.objects.filter(id=fleet_id).first()
    fleet_engine = Fleet_engine.objects.filter(fleet_id=fleet_id).first()
    error = 0
    # Повверка наличия топлива в зависимости от варианта полета. Проверка достаточности топлива для полета.
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

    distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)

    fleet_energy_power = Fleet_energy_power.objects.filter(fleet_id=fleet_id).first()

    need_fuel = fuel.fuel(fleet_id, flightplan_flight, distance, fleet, fleet_energy_power, fleet_engine)

    fuel_tank = Fuel_tank.objects.filter(fleet_id=fleet_id).first()
    fuel_pattern = Fuel_pattern.objects.filter(user=fleet.user, fuel_class=fuel_tank.fuel_class).first()

    if need_fuel > fuel_tank.amount_fuel * fuel_pattern.efficiency:
        error = 1

    if len(args) == 1:
        start_time = datetime.now()
    else:
        start_time = args[1]

    if error == 0:
        flightplan_flight = Flightplan_flight.objects.filter(id=flightplan_flight_id).update(start_time=start_time)
        flightplan = Flightplan.objects.filter(id=id_flightplan).update(status=1)
        fleet = Fleet.objects.filter(id=fleet_id).update(status=True, planet_status=0)
