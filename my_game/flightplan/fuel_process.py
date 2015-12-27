# -*- coding: utf-8 -*-


from my_game.models import Ship
from my_game.flightplan.need_fuel_process import need_fuel_process


def fuel_process(*args):
    fleet_id = args[0]
    flightplan_process = args[1]
    flightplan = args[2]
    time_process = 0
    ship_in_fleets = Ship.objects.filter(fleet_status=1, place_id=fleet_id)

    if flightplan.class_command == 3:
        time_process = flightplan_process.time_extraction
    elif flightplan.class_command == 4:
        time_process = flightplan_process.time_refill
    elif flightplan.class_command == 6:
        time_process = flightplan_process.time_scanning
    elif flightplan.class_command == 8:
        time_process = flightplan_process.time

    need_fuel = need_fuel_process(ship_in_fleets, flightplan, time_process, fleet_id)

    return need_fuel
