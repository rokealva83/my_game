# -*- coding: utf-8 -*-

import math
from my_game.flightplan.create.flight import calculation
from my_game.models import Flightplan_flight


def fuel(*args):
    fleet_id = args[0]
    flightplan_flight = args[1]
    distance = args[2]
    fleet = args[3]
    fleet_energy_power = args[4]
    fleet_engine = args[5]

    coordinate_giper = ''
    coordinate_null = ''
    flight_time = 600
    need_energy = 1

    if flightplan_flight.id_command == 1:
        flight_time = int(math.sqrt(distance / 2 * (int(fleet.ship_empty_mass)) / int(fleet_engine.system_power)) * 2)
        need_energy = fleet_energy_power.use_fuel_system
    elif flightplan_flight.id_command == 2:
        coordinate_giper = ''
        coordinate_null = ''
        need_energy = fleet_energy_power.use_fuel_intersystem
    elif flightplan_flight.id_command == 3:
        coordinate_giper = 1
        coordinate_null = ''
        need_energy = fleet_energy_power.use_energy_giper
    elif flightplan_flight.id_command == 4:
        coordinate_giper = ''
        coordinate_null = 1
        need_energy = fleet_energy_power.use_energy_null
    if flightplan_flight.id_command == 2 or flightplan_flight.id_command == 3 or flightplan_flight.id_command == 4:
        answer = calculation(fleet_id, coordinate_giper, coordinate_null, distance)
        flight_time = int(answer['flight_time'])

    if flightplan_flight.flight_time != flight_time:
        new_time = Flightplan_flight.objects.filter(id=flightplan_flight.pk).update(flight_time=flight_time)

    need_fuel = need_energy / (fleet_energy_power.produce_energy / fleet_energy_power.use_fuel_generator) * (
        flight_time / 3600)
    return need_fuel
