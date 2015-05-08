# -*- coding: utf-8 -*-

from datetime import datetime

from django.shortcuts import render

from my_game.models import MyUser, User_city
from my_game.models import Warehouse
from my_game import function
from my_game.models import Ship, Fleet, Fleet_parametr_scan, Fleet_engine, Fleet_parametr_resource_extraction
from my_game.models import Flightplan, Flightplan_flight, Flightplan_scan, Flightplan_production, Flightplan_hold, \
    Flightplan_refill, Flightplan_build_repair, Fleet_parametr_build_repair, Flightplan_colonization, Device_pattern
from my_game.models import Hull_pattern, Armor_pattern, Shell_pattern, Shield_pattern, Weapon_pattern, \
    Warehouse_factory, Warehouse_element, Factory_pattern, Engine_pattern, Generator_pattern, Module_pattern, \
    Basic_resource, Hold, Fuel_pattern
from my_game.flightplan.find_name import find_name


def unload_hold(*args):
    session_user = args[0]
    fleet_id = args[1]
    unload_all = args[2]
    unload_all_hold = args[3]
    unload_amount = args[4]
    id_hold_element = args[5]


    hold = Hold.objects.filter(id=id_hold_element).first()
    class_element = hold.class_shipment
    id_element = hold.id_shipment

    name = find_name(class_element, id_element)
    error = 0
    if unload_all_hold:
        id_command = 4
        unload_amount = 0
        class_element = 0
        id_element = 0
        time = 600
    elif unload_all:
        id_command = 3
        unload_amount = hold.amount_shipment
        class_element = 0
        id_element = id_hold_element
        time = 300
    else:
        if unload_amount:
            id_command = 2
            class_element = hold.class_shipment
            id_element = hold.id_shipment
            time = 150
        else:
            message = ''
            error = 1
    if error == 0:
        flightplan = Flightplan(
            user=session_user,
            id_fleet=fleet_id,
            class_command=2,
            id_command=id_command,
            status=0
        )
        flightplan.save()

        flightplan_hold = Flightplan_hold(
            user=session_user,
            id_fleet=fleet_id,
            id_command=id_command,
            amount=unload_amount,
            start_time=datetime.now(),
            id_fleetplan=flightplan.id,
            time=time,
            class_element=class_element,
            id_element=id_element,
            name=name
        )
        flightplan_hold.save()


