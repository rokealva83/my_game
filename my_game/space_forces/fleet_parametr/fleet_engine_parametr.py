# -*- coding: utf-8 -*-

from my_game.models import Ship


def fleet_engine_parametr(*args):
    fleet = args[0]
    fleet_ships = Ship.objects.filter(fleet_status=1, place_id=fleet.id).all()
    system_power = intersystem_power = giper_power = null_power = giper_accuracy = null_accuracy = ship_amount = 0
    for fleet_ship in fleet_ships:
        system_power += int(fleet_ship.project_ship.system_power) * fleet_ship.amount_ship
        intersystem_power += int(fleet_ship.project_ship.intersystem_power) * fleet_ship.amount_ship
        giper_power += int(fleet_ship.project_ship.giper_power) * fleet_ship.amount_ship
        giper_accuracy += int(fleet_ship.project_ship.giper_accuracy) * fleet_ship.amount_ship
        null_power += int(fleet_ship.project_ship.null_power) * fleet_ship.amount_ship
        null_accuracy += int(fleet_ship.project_ship.null_accuracy) * fleet_ship.amount_ship
        ship_amount += fleet_ship.amount_ship
        if ship_amount:
            giper_accuracy = giper_accuracy / ship_amount
            null_accuracy = null_accuracy / ship_amount
    fleet_engine = fleet.fleet_engine
    setattr(fleet_engine, 'system_power', system_power)
    setattr(fleet_engine, 'intersystem_power', intersystem_power)
    setattr(fleet_engine, 'giper_power', giper_power)
    setattr(fleet_engine, 'giper_accuracy', giper_accuracy)
    setattr(fleet_engine, 'null_power', null_power)
    setattr(fleet_engine, 'null_accuracy', null_accuracy)
    fleet_engine.save()
    return True
