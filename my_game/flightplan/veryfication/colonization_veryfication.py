# -*- coding: utf-8 -*-

from datetime import timedelta
from django.utils import timezone
import math
from my_game.models import Planet, Warehouse, Warehouse_element, Warehouse_factory, Warehouse_ship
from my_game.models import System
from my_game.models import Fleet, Fuel_pattern, Fuel_tank, Armor_pattern, Shield_pattern, Weapon_pattern, \
    Engine_pattern, Generator_pattern, Shell_pattern, Module_pattern, Device_pattern
from my_game.models import Flightplan, Flightplan_flight, Fleet_parametr_scan, Flightplan_production, Flightplan_hold
from my_game.models import Mail, Hold, Ship, Project_ship, Hull_pattern, User_city, Factory_pattern, \
    Flightplan_colonization
from my_game.flightplan.start import start_flight, start_colonization, start_extraction, start_refill, \
    start_repair_build, start_scaning, start_unload_hold, start_upload_hold
from my_game.flightplan.fuel import need_fuel_process, minus_fuel


def colonization_veryfication(*args):
    fleet = args[0]
    flightplan = Flightplan.objects.filter(id_fleet=fleet.id).first()
    flightplan_colonization = Flightplan_colonization.objects.filter(id_fleetplan=flightplan.id).first()
    if flightplan_colonization:
        time = timezone.now()
        time_start = flightplan_colonization.start_time
        time_colonization = int(flightplan_colonization.time)
        delta_time = time - time_start
        new_delta = delta_time.seconds
        if new_delta > time_colonization:

            if flightplan_colonization.id_command == 1:
                planet = Planet.objects.filter(global_x=fleet.x, global_y=fleet.y, global_z=fleet.z,
                                               planet_free=1).first()
                if planet:
                    user_city = User_city(
                        user=fleet.user,
                        system_id=planet.system_id,
                        planet=planet.id,
                        x=planet.global_x,
                        y=planet.global_y,
                        z=planet.global_z,
                        city_size_free=planet.work_area_planet,
                        founding_date=timezone.now(),
                        extraction_date=timezone.now()
                    )
                    user_city.save()
                    planet_up = Planet.objects.filter(pk=planet.id).update(planet_free=0)

                else:
                    message = ''
            else:
                user_city = User_city(
                    user=fleet.user,
                    system_id=0,
                    planet=0,
                    x=fleet.x,
                    y=fleet.y,
                    z=fleet.z,
                    city_size_free=0,
                    founding_date=timezone.now(),
                    extraction_date=timezone.now()
                )
                user_city.save()

        ship_in_fleets = Ship.objects.filter(fleet_status=1, place_id=fleet.id)
        need_fuel = need_fuel_process(ship_in_fleets, flightplan, time_colonization, fleet.id)
        minus_fuel(fleet, need_fuel)
