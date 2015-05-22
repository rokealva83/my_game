# -*- coding: utf-8 -*-


from my_game.flightplan.create.flight import calculation
import math
from my_game.models import Fleet_energy_power
from my_game.models import Flightplan_flight
from my_game.models import Fleet_engine
from my_game.models import Ship, Element_ship, Module_pattern, Hull_pattern, Project_ship


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

    ship_in_fleets = Ship.objects.filter(fleet_status=1, place_id=fleet_id)
    hull_energy = 0
    for ship in ship_in_fleets:
        project = Project_ship.objects.filter(id=ship.id_project_ship).first()
        hull = Hull_pattern.objects.filter(id=project.hull_id).first()
        hull_energy = hull_energy + hull.power_consuption * ship.amount_ship

    need_energy = need_energy + hull_energy
    need_fuel = 1.0 * need_energy / (fleet_energy_power.produce_energy / fleet_energy_power.use_fuel_generator) * (
        flight_time / 3600.0)
    return need_fuel


def fuel_process(*args):
    fleet_id = args[0]
    flightplan_process = args[1]
    flightplan = args[2]
    find = 0
    hull_energy = 0
    need_energy = 0
    time_process = 0
    fleet_energy_power = Fleet_energy_power.objects.filter(fleet_id=fleet_id).first()
    ship_in_fleets = Ship.objects.filter(fleet_status=1, place_id=fleet_id)

    if flightplan.class_command == 3:
        time_process = flightplan_process.time_extraction
    elif flightplan.class_command == 6:
        time_process = flightplan_process.time_scanning

    for ship in ship_in_fleets:
        element_ships = Element_ship.objects.filter(id_project_ship=ship.id_project_ship)
        for element_ship in element_ships:
            if element_ship.class_element == 8:
                element_pattern = Module_pattern.objects.filter(id=element_ship.id_element_pattern).first()

                if flightplan.class_command == 3:
                    if element_pattern.module_class == 3:
                        need_energy = element_pattern.power_consuption

                elif flightplan.class_command == 6:
                    if element_pattern.module_class == 6 and element_pattern.param3 == flightplan_process.id_command and find == 0:
                        find = 1
                        need_energy = element_pattern.power_consuption

        project = Project_ship.objects.filter(id=ship.id_project_ship).first()
        hull = Hull_pattern.objects.filter(id=project.hull_id).first()
        hull_energy = hull_energy + hull.power_consuption * ship.amount_ship
        if flightplan.class_command != 6:
            need_energy = need_energy * ship.amount_ship

    need_energy = need_energy + hull_energy
    need_fuel = 1.0 * need_energy / (fleet_energy_power.produce_energy / fleet_energy_power.use_fuel_generator) * (
        time_process / 3600.0)

    return need_fuel