# -*- coding: utf-8 -*-

from datetime import datetime

from django.shortcuts import render

from my_game.models import MyUser, User_city
from my_game.models import Warehouse
from my_game import function
from my_game.models import Ship, Fleet, Fleet_parametr_scan, Fleet_engine, Fleet_parametr_resource_extraction
from my_game.models import Flightplan, Flightplan_flight, Flightplan_scan, Flightplan_production, Flightplan_hold, \
    Flightplan_refill, Flightplan_build_repair, Fleet_parametr_build_repair, Flightplan_colonization, Device_pattern
from my_game.flightplan.create import flight
from my_game.flightplan.create import resource_extraction
from my_game.models import Hull_pattern, Armor_pattern, Shell_pattern, Shield_pattern, Weapon_pattern, \
    Warehouse_factory, Warehouse_element, Factory_pattern, Engine_pattern, Generator_pattern, Module_pattern, \
    Basic_resource, Hold, Fuel_pattern

def scan(*args):
    session_user = args[0]
    fleet_id = args[1]
    method_scanning = args[2]
    fleet_parametr_scan = Fleet_parametr_scan.objects.filter(fleet_id=fleet_id,
                                                             method_scanning=method_scanning).first()
    flightplan = Flightplan(
        user=session_user,
        id_fleet=fleet_id,
        class_command=6,
        id_command=method_scanning,
        status=0
    )
    flightplan.save()

    flightplan_scan = Flightplan_scan(
        user=session_user,
        id_fleet=fleet_id,
        id_command=method_scanning,
        range_scanning=fleet_parametr_scan.range_scanning,
        start_time=datetime.now(),
        time_scanning=fleet_parametr_scan.time_scanning,
        id_fleetplan=flightplan.id
    )
    flightplan_scan.save()
