# -*- coding: utf-8 -*-

import math
from my_game.models import ProjectShip, Ship, Fleet, FleetEngine


def calculation(*args):
    fleet = args[0]
    coordinate_giper = args[1]
    coordinate_null = args[2]
    distance = args[3]
    if coordinate_giper:
        fleet_ships = Ship.objects.filter(place_id=fleet, fleet_status=1)
        check = 0
        for fleet_ship in fleet_ships:
            project_ship = ProjectShip.objects.filter(id=fleet_ship.project_ship).first()
            if project_ship.giper_power == 0:
                check = 1
        if check == 0:
            flight_time = math.sqrt(
                distance / 2 * (int(fleet.ship_empty_mass)) / int(fleet.fleet_engine.giper_power)) * 2
            command_id = 3
        else:
            flight_time = math.sqrt(
                distance / 2 * (int(fleet.ship_empty_mass)) / int(fleet.fleet_engine.intersystem_power)) * 2
            command_id = 2
    elif coordinate_null:
        fleet_ships = Ship.objects.filter(place_id=fleet, fleet_status=1)
        check = 0
        for fleet_ship in fleet_ships:
            project_ship = ProjectShip.objects.filter(id=fleet_ship.project_ship).first()
            if project_ship.giper_power == 0:
                check = 1
        if check == 0:
            flight_time = math.sqrt(
                distance / 2 * (int(fleet.ship_empty_mass)) / int(fleet.fleet_engine.null_power)) * 2
            command_id = 4
        else:
            flight_time = math.sqrt(
                distance / 2 * (int(fleet.ship_empty_mass)) / int(fleet.fleet_engine.intersystem_power)) * 2
            command_id = 2
    else:
        flight_time = math.sqrt(
            distance / 2 * (int(fleet.ship_empty_mass)) / int(fleet.fleet_engine.intersystem_power)) * 2
        command_id = 2
    return {'flight_time': flight_time, 'command_id': command_id}
