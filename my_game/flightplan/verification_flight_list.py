# -*- coding: utf-8 -*-

from datetime import timedelta
from django.utils import timezone
import math
from my_game.models import Planet
from my_game.models import System, Asteroid_field, Flightplan_scan
from my_game.models import Fleet, Fuel_pattern, Fuel_tank
from my_game.models import Flightplan, Flightplan_flight, Fleet_parametr_scan, Flightplan_production
from my_game.models import Mail
from my_game.flightplan.start import start_flight, start_colonization, start_extraction, start_refill, \
    start_repair_build, start_scaning, start_unload_hold, start_upload_hold
from my_game.flightplan.veryfication.flight_verification import verification_flight
from my_game.flightplan.veryfication.scan_veryfication import scan_veryfication
from my_game.flightplan import fuel


def verification_flight_list(request):
    user = request
    fleets = Fleet.objects.filter(user=user)
    finish_time = timezone.now()
    for fleet in fleets:
        flightplans = Flightplan.objects.filter(id_fleet=fleet.id)
        flightplan_len = len(flightplans)
        lens = 0
        for flightplan in flightplans:
            flightplan_id = flightplan.id
            if flightplan.status == 1:
                if flightplan.class_command == 1:
                    finish_time = verification_flight(fleet)
                    flightplan = Flightplan.objects.filter(id_fleet=fleet.id, status=0).first()


                elif flightplan.class_command == 6:
                    finish_time = scan_veryfication(fleet)
                    flightplan = Flightplan.objects.filter(id_fleet=fleet.id, status=0).first()

                if flightplan:
                    if flightplan.class_command == 1:
                        start_flight.start_flight(fleet.id, finish_time)
                    elif flightplan.class_command == 6:
                        start_scaning.start_scaning(fleet.id, finish_time)
                else:
                    fleet_up = Fleet.objects.filter(id=fleet.id).update(status=0)





                # elif flightplan.class_command == 3:
                # asteroid_field = Asteroid_field.objects.filter(x=fleet.x, y=fleet.y, z=fleet.z).first()
                # flightplan_production = Flightplan_production.objects.filter(fleetplan_id=flightplan.id).first()
                # time = datetime.now()
                # time_start = flightplan_production.start_time
                # delta_time = time - time_start
                # new_delta = delta_time.seconds
                # new_delta = int(new_delta/60)
                # if new_delta >= flightplan_production.time_extraction:
                # extraction_mine = flightplan_production.time_extraction * flightplan_production.production_per_minute
                # else:
                # new_time_extraction =  flightplan_production.time_extraction - new_delta
                # extraction_mine = new_delta * flightplan_production.production_per_minute
                # resource1 = extraction_mine * asteroid_field.koef_res_1
                # resource2 = extraction_mine * asteroid_field.koef_res_2
                # resource3 = extraction_mine * asteroid_field.koef_res_3
                # resource4 = extraction_mine * asteroid_field.koef_res_4
                # mineral1 = extraction_mine * asteroid_field.koef_min_1
                # mineral2 = extraction_mine * asteroid_field.koef_min_2
                # mineral3 = extraction_mine * asteroid_field.koef_min_3
                # mineral4 = extraction_mine * asteroid_field.koef_min_4
                #

                #
                #
                #
                # lens = lens + 1
                # if lens == flightplan_len:
                # fleet_up = Fleet.objects.filter(id=fleet.id).update(status=0)
                # else:
                # flightplan = Flightplan.objects.filter(id_fleet=fleet.id).first().update(status=1)
                #
                # flightplan = Flightplan.objects.filter(id=flightplan_id).delete()
