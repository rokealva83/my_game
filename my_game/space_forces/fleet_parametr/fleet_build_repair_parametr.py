# -*- coding: utf-8 -*-

from my_game.models import FleetParametrBuildRepair


def fleet_build_repair_parametr(*args):
    fleet = args[0]
    ship_repair_elements = args[1]
    amount_ship = args[2]
    fleet_parametr_build = 0
    fleet_parametr_repair = 0
    for ship_repair_element in ship_repair_elements:
        if ship_repair_element.param3 == 1:
            fleet_parametr_build += ship_repair_element.param1
        elif ship_repair_element.param3 == 2:
            fleet_parametr_repair += ship_repair_element.param1
    parametr_build = fleet_parametr_build * amount_ship
    parametr_repair = fleet_parametr_repair * amount_ship

    if parametr_build:
        fleet_parametr_build = FleetParametrBuildRepair.objects.filter(fleet=fleet, class_process=1).first()
        if fleet_parametr_build:
            new_process_per_minute = fleet_parametr_build.process_per_minute + parametr_build * amount_ship
            setattr(fleet_parametr_build, 'process_per_minute', new_process_per_minute)
            fleet_parametr_build.save()
        else:
            fleet_parametr_build = FleetParametrBuildRepair(
                fleet=fleet,
                class_process=1,
                process_per_minute=parametr_build)
            fleet_parametr_build.save()
    elif parametr_repair:
        fleet_parametr_repair = FleetParametrBuildRepair.objects.filter(fleet=fleet, class_process=2).first()
        if fleet_parametr_repair:
            new_process_per_minute = fleet_parametr_repair.process_per_minute + parametr_repair * amount_ship
            setattr(fleet_parametr_repair, 'process_per_minute', new_process_per_minute)
            fleet_parametr_repair.save()
        else:
            fleet_parametr_repair = FleetParametrBuildRepair(
                fleet=fleet,
                class_process=1,
                process_per_minute=parametr_repair)
            fleet_parametr_repair.save()
    return True
