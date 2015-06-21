# -*- coding: utf-8 -*-

from datetime import timedelta
from django.utils import timezone
import math
from my_game.models import Planet, Warehouse, Warehouse_element, Warehouse_factory, Warehouse_ship
from my_game.models import System, Asteroid_field, Flightplan_scan, Fleet_parametr_resource_extraction
from my_game.models import Fleet, Fuel_pattern, Fuel_tank, Armor_pattern, Shield_pattern, Weapon_pattern, \
    Engine_pattern, Generator_pattern, Shell_pattern, Module_pattern, Device_pattern
from my_game.models import Flightplan, Flightplan_flight, Fleet_parametr_scan, Flightplan_production, Flightplan_hold
from my_game.models import Mail, Hold, Ship, Project_ship, Hull_pattern, User_city, Factory_pattern
from my_game.flightplan.start import start_flight, start_colonization, start_extraction, start_refill, \
    start_repair_build, start_scaning, start_unload_hold, start_upload_hold
from my_game.flightplan.veryfication.flight_verification import verification_flight
from my_game.flightplan.veryfication.scan_veryfication import scan_veryfication
from my_game.flightplan.veryfication.extraction_veryfication import extraction_veryfication
from my_game.flightplan.veryfication.upload_unload_veryfication import upload_unload_veryfication
from my_game.flightplan.veryfication.colonization_veryfication import colonization_veryfication
from my_game.flightplan import fuel


def verification_flight_list(request):
    user = request
    fleets = Fleet.objects.filter(user=user)
    finish_time = timezone.now()
    for fleet in fleets:
        flightplans = Flightplan.objects.filter(id_fleet=fleet.id)
        for flightplan in flightplans:
            if flightplan.status == 1:
                if flightplan.class_command == 1:
                    finish_time = verification_flight(fleet)
                    flightplan = Flightplan.objects.filter(id_fleet=fleet.id, status=0).first()

                elif flightplan.class_command == 2:
                    finish_time = upload_unload_veryfication(fleet)
                    flightplan = Flightplan.objects.filter(id_fleet=fleet.id, status=0).first()

                elif flightplan.class_command == 3:
                    finish_time = extraction_veryfication(fleet)
                    flightplan = Flightplan.objects.filter(id_fleet=fleet.id, status=0).first()

                elif flightplan.class_command == 6:
                    finish_time = scan_veryfication(fleet)
                    flightplan = Flightplan.objects.filter(id_fleet=fleet.id, status=0).first()

                elif flightplan.class_command == 8:
                    finish_time = colonization_veryfication(fleet)
                    flightplan = Flightplan.objects.filter(id_fleet=fleet.id, status=0).first()

                if flightplan:

                    if flightplan.class_command == 1:
                        start_flight.start_flight(fleet.id, finish_time)

                    elif flightplan.class_command == 2:
                        if flightplan.id_command == 1:
                            start_upload_hold.start_upload(fleet.id, finish_time)
                        else:
                            start_unload_hold.start_unload(fleet.id, finish_time)

                    elif flightplan.class_command == 3:
                        start_extraction.start_extraction(fleet.id, finish_time)

                    elif flightplan.class_command == 4:
                        start_refill.start_refill(user, fleet.id, finish_time)

                    elif flightplan.class_command == 6:
                        start_scaning.start_scaning(fleet.id, finish_time)
                else:
                    fleet_up = Fleet.objects.filter(id=fleet.id).update(status=0)