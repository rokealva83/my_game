# -*- coding: utf-8 -*-

from my_game.models import FuelTank
from my_game.space_forces.hold_and_tank.unload_fuel import unload_fuel


def unload_fuel_all(*args):
    session_user = args[0]
    session_user_city = args[1]
    fleet = args[2]
    message = ''
    fuel_tanks = FuelTank.objects.filter(fleet=fleet).all()
    for fuel_tank in fuel_tanks:
        message = unload_fuel(session_user, session_user_city, fleet, fuel_tank.amount_fuel, fuel_tank.id)
    return message
