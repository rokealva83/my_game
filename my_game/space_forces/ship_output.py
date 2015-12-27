# -*- coding: utf-8 -*-

from my_game.models import UserCity
from my_game.models import Ship, Fleet


def ship_output(*args):
    session_user = args[0]
    session_user_city = args[1]
    fleet = args[2]
    flightplans = args[3]
    flightplan_flights = args[4]
    warehouse_factorys = args[5]
    command = args[6]
    message = args[7]

    warehouse = session_user_city.warehouse
    user_citys = UserCity.objects.filter(user=session_user).all()
    user_fleets = Fleet.objects.filter(user=session_user).all()
    ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city.id).all()
    add_ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city.id).all()
    ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1).all()

    return {'user': session_user, 'warehouse': warehouse, 'user_city': session_user_city, 'user_citys': user_citys,
            'user_fleets': user_fleets, 'add_ships': add_ships, 'fleet_id': fleet.id,
            'ship_fleets': ship_fleets, 'ships': ships, 'fleet': fleet,
            'command': command, 'flightplans': flightplans, 'flightplan_flights': flightplan_flights,
            'warehouse_factorys': warehouse_factorys, 'message': message}
