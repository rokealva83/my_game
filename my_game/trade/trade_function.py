# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from django.utils import timezone
import math
from my_game.models import Trade_flight, User_city, Fleet_engine


def flight_record_sheet_flight(*args):
    session_user = args[0]
    session_user_city = args[1]
    user_city = args[2]
    id_fleet = args[3]
    trade_element = args[4]
    lot = args[5]
    fleet = args[6]
    lot_amount = args[7]
    distance = args[8]
    mass_element = trade_element.mass_element
    size_element = trade_element.size_element
    mass = lot * mass_element + fleet.ship_empty_mass
    trade_flight = Trade_flight.objects.filter(id_fleet=id_fleet).last()
    fleet_engine = Fleet_engine.objects.filter(fleet_id=id_fleet).first()

    flight_time = math.sqrt(distance / 2 * mass / int(fleet_engine.intersystem_power)) * 2
    if trade_flight:
        start_time = trade_flight.finish_time
    else:
        start_time = timezone.now()
    finish_time = start_time + timedelta(seconds=flight_time)
    if lot == 0:
        start_x = int(user_city.x)
        start_y = int(user_city.y)
        start_z = int(user_city.z)
        finish_x = int(trade_element.x)
        finish_y = int(trade_element.y)
        finish_z = int(trade_element.z)
    else:
        start_x = int(trade_element.x)
        start_y = int(trade_element.y)
        start_z = int(trade_element.z)
        finish_x = int(user_city.x)
        finish_y = int(user_city.y)
        finish_z = int(user_city.z)
    trade_flight = Trade_flight(
        user=session_user,
        user_city=session_user_city,
        id_fleet=id_fleet,
        id_flight=1,
        name=trade_element.name,
        class_element=trade_element.class_element,
        id_element=trade_element.id_element,
        amount=lot,
        mass=mass_element * lot,
        size=size_element * lot,
        start_x=start_x,
        start_y=start_y,
        start_z=start_z,
        finish_x=finish_x,
        finish_y=finish_y,
        finish_z=finish_z,
        flight_time=flight_time,
        start_time=start_time,
        finish_time=finish_time,
        planet=user_city.planet_id,
    )
    trade_flight.save()


def flight_record_sheet_loading_holds(*args):
    session_user = args[0]
    session_user_city = args[1]
    id_fleet = args[2]
    trade_element = args[3]
    lot = args[4]

    flight_time = 300
    trade_flight = Trade_flight.objects.filter(id_fleet=id_fleet).last()
    mass_element = trade_element.mass_element
    size_element = trade_element.size_element
    if trade_flight:
        start_time = trade_flight.finish_time
    else:
        start_time = timezone.now()
    finish_time = start_time + timedelta(seconds=flight_time)
    user_city = User_city.objects.filter(id=session_user_city).first()
    trade_flight = Trade_flight(
        user=session_user,
        user_city=session_user_city,
        id_fleet=id_fleet,
        id_flight=2,
        name=trade_element.name,
        class_element=trade_element.class_element,
        id_element=trade_element.id_element,
        amount=lot,
        mass=mass_element * lot,
        size=size_element * lot,
        start_x=trade_element.x,
        start_y=trade_element.y,
        start_z=trade_element.z,
        finish_x=trade_element.x,
        finish_y=trade_element.y,
        finish_z=trade_element.z,
        flight_time=flight_time,
        start_time=start_time,
        finish_time=finish_time,
        planet=user_city.planet_id,
    )
    trade_flight.save()


def flight_record_sheet_unloading_holds(*args):
    session_user = args[0]
    session_user_city = args[1]
    user_city = args[2]
    id_fleet = args[3]
    trade_element = args[4]
    lot = args[5]
    flight_time = 300
    trade_flight = Trade_flight.objects.filter(id_fleet=id_fleet).last()
    if trade_flight:
        start_time = trade_flight.finish_time
    else:
        start_time = datetime.now()
    finish_time = start_time + timedelta(seconds=flight_time)
    trade_flight = Trade_flight(
        user=session_user,
        user_city=session_user_city,
        id_fleet=id_fleet,
        id_flight=3,
        name=trade_element.name,
        class_element=trade_element.class_element,
        id_element=trade_element.id_element,
        amount=lot,
        start_x=user_city.x,
        start_y=user_city.y,
        start_z=user_city.z,
        finish_x=user_city.x,
        finish_y=user_city.y,
        finish_z=user_city.z,
        flight_time=flight_time,
        start_time=start_time,
        finish_time=finish_time,
        planet=user_city.planet_id,
    )
    trade_flight.save()