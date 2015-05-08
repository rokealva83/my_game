# -*- coding: utf-8 -*-


from datetime import datetime, timedelta
from django.shortcuts import render
from my_game.models import MyUser, User_city
from my_game.models import Warehouse
from my_game import function
from my_game.models import Ship, Fleet
from my_game.models import Flightplan, Flightplan_flight, Flightplan_scan, Flightplan_hold, Flightplan_production
from my_game.models import Hull_pattern, Armor_pattern, Shell_pattern, Shield_pattern, Weapon_pattern, \
    Warehouse_factory, Warehouse_element, Factory_pattern, Engine_pattern, Generator_pattern, Module_pattern, \
    Basic_resource, Hold, Fleet_engine, Fleet_parametr_scan, Fleet_parametr_resource_extraction, Fuel_pattern, \
    Flightplan_build_repair, Flightplan_refill, Fleet_parametr_build_repair, Flightplan_colonization


def start_repair_build(*args):
    fleet_id = args[0]

    if len(args) == 1:
        start_time = datetime.now()

    flightplan = Flightplan.objects.filter(id_fleet=fleet_id).first()
    id_flightplan = flightplan.pk

    flightplan_repair = Flightplan_build_repair.objects.filter(id_fleet=fleet_id).first()
    flightplan_repair = Flightplan_build_repair.objects.filter(id=flightplan_repair.pk).update(start_time=start_time)
    flightplan = Flightplan.objects.filter(id=id_flightplan).update(status=1)
    fleet = Fleet.objects.filter(id=fleet_id).update(status=True, planet_status=0)
