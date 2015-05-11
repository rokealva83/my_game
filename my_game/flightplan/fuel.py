# -*- coding: utf-8 -*-


from my_game.flightplan.create.flight import calculation
import math
from my_game.models import Fleet_energy_power
from my_game.models import Flightplan_flight
from my_game.models import Fleet_engine


def fuel(*args):
    fleet_id = args[0]
    flightplan_flight = args[1]
    fleet = args[2]

    fleet_engine = Fleet_engine.objects.filter(fleet_id=fleet_id).first()
    fleet_energy_power = Fleet_energy_power.objects.filter(fleet_id=fleet_id).first()

    x1 = int(flightplan_flight.start_x)
    y1 = int(flightplan_flight.start_y)
    z1 = int(flightplan_flight.start_z)
    x2 = int(flightplan_flight.finish_x)
    y2 = int(flightplan_flight.finish_y)
    z2 = int(flightplan_flight.finish_z)

    distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)

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

    need_fuel = 1.0 * need_energy / (fleet_energy_power.produce_energy / fleet_energy_power.use_fuel_generator) * (
    flight_time / 3600.0)
    return need_fuel
