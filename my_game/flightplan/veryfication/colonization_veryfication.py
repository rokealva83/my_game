# -*- coding: utf-8 -*-

from datetime import timedelta
from django.utils import timezone
import math
from my_game.models import Planet, Warehouse, Warehouse_element, Warehouse_factory, Warehouse_ship
from my_game.models import System, Asteroid_field, Flightplan_scan, Fleet_parametr_resource_extraction
from my_game.models import Fleet, Fuel_pattern, Fuel_tank, Armor_pattern, Shield_pattern, Weapon_pattern, \
    Engine_pattern, Generator_pattern, Shell_pattern, Module_pattern, Device_pattern
from my_game.models import Flightplan, Flightplan_flight, Fleet_parametr_scan, Flightplan_production, Flightplan_hold
from my_game.models import Mail, Hold, Ship, Project_ship, Hull_pattern, User_city, Factory_pattern, Flightplan_colonization
from my_game.flightplan.start import start_flight, start_colonization, start_extraction, start_refill, \
    start_repair_build, start_scaning, start_unload_hold, start_upload_hold
from my_game.flightplan.veryfication.flight_verification import verification_flight
from my_game.flightplan.veryfication.scan_veryfication import scan_veryfication
from my_game.flightplan.veryfication.extraction_veryfication import extraction_veryfication
from my_game.flightplan.veryfication.upload_unload_veryfication import upload_unload_veryfication
from my_game.flightplan import fuel

def colonization_veryfication(*args):
    fleet= args[0]
    flightplan = Flightplan.objects.filter(id_fleet=fleet.id).first()
    flightplan_colonization = Flightplan_colonization.objects.filter(id_fleetplan=flightplan.id).first()
    if flightplan_colonization:
        time = timezone.now()
        time_start = flightplan_colonization.start_time
        time_colonization = int(flightplan_colonization.time)
        delta_time = time - time_start
        new_delta = delta_time.seconds
        if new_delta > time_colonization:
            a=1