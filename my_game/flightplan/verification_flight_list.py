# -*- coding: utf-8 -*-

from datetime import timedelta
from django.utils import timezone
import math
from my_game.models import Planet
from my_game.models import System, Asteroid_field, Flightplan_scan, Fleet_parametr_resource_extraction
from my_game.models import Fleet, Fuel_pattern, Fuel_tank
from my_game.models import Flightplan, Flightplan_flight, Fleet_parametr_scan, Flightplan_production
from my_game.models import Mail, Hold
from my_game.flightplan.start import start_flight, start_colonization, start_extraction, start_refill, \
    start_repair_build, start_scaning, start_unload_hold, start_upload_hold
from my_game.flightplan.veryfication.flight_verification import verification_flight
from my_game.flightplan.veryfication.scan_veryfication import scan_veryfication
from my_game.flightplan.veryfication.extraction_veryficate import extraction_veryfication
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

                elif flightplan.class_command == 3:
                    flightplan_extraction = Flightplan_production.objects.filter(id_fleetplan=flightplan.id).first()
                    if flightplan_extraction:
                        finish_time = timezone.now()
                        time = timezone.now()
                        time_start = flightplan_extraction.start_time
                        delta_time = time - time_start
                        new_delta = delta_time.seconds
                        delta = int(flightplan_extraction.time_extraction)
                        if new_delta > delta:
                            finish_time = time_start + timedelta(seconds=delta)
                            fleet_resource_extraction = Fleet_parametr_resource_extraction.objects.filter(
                                fleet_id=fleet.id).first()
                            extract_per_second = int(fleet_resource_extraction.extraction_per_minute) / 60
                            extraction = delta * extract_per_second
                            x = fleet.x
                            y = fleet.y
                            z = fleet.z

                            asteroid_field = Asteroid_field.objects.filter(x=x, y=y, z=z).first()
                            if asteroid_field:
                                if extraction > fleet.empty_hold:
                                    extraction = fleet.empty_hold
                                    if extraction > asteroid_field.size:
                                        extraction = asteroid_field.size
                                        asteroid_field = Asteroid_field.objects.filter(x=x, y=y, z=z).delete()
                                    else:
                                        new_size = asteroid_field.size - extraction
                                        asteroid_field = Asteroid_field.objects.filter(x=x, y=y, z=z).update(size=new_size)

                                resource1 = extraction * asteroid_field.koef_res_1
                                resource2 = extraction * asteroid_field.koef_res_2
                                resource3 = extraction * asteroid_field.koef_res_3
                                resource4 = extraction * asteroid_field.koef_res_4
                                mineral1 = extraction * asteroid_field.koef_min_1
                                mineral2 = extraction * asteroid_field.koef_min_2
                                mineral3 = extraction * asteroid_field.koef_min_3
                                mineral4 = extraction * asteroid_field.koef_min_4

                                res1 = Hold.objects.filter(fleet_id=fleet.id, class_shipment=0, id_shipment=1).first()
                                res2 = Hold.objects.filter(fleet_id=fleet.id, class_shipment=0, id_shipment=2).first()
                                res3 = Hold.objects.filter(fleet_id=fleet.id, class_shipment=0, id_shipment=3).first()
                                res4 = Hold.objects.filter(fleet_id=fleet.id, class_shipment=0, id_shipment=4).first()
                                min1 = Hold.objects.filter(fleet_id=fleet.id, class_shipment=0, id_shipment=5).first()
                                min2 = Hold.objects.filter(fleet_id=fleet.id, class_shipment=0, id_shipment=6).first()
                                min3 = Hold.objects.filter(fleet_id=fleet.id, class_shipment=0, id_shipment=7).first()
                                min4 = Hold.objects.filter(fleet_id=fleet.id, class_shipment=0, id_shipment=8).first()

                                add_res(fleet, res1, resource1)
                                add_res(fleet, res2, resource2)
                                add_res(fleet, res3, resource3)
                                add_res(fleet, res4, resource4)
                                add_res(fleet, min1, mineral1)
                                add_res(fleet, min2, mineral2)
                                add_res(fleet, min3, mineral3)
                                add_res(fleet, min4, mineral4)

                                new_hold = fleet.hold + extraction
                                mass = extraction
                                new_mass = fleet.ship_empty_mass + mass
                                new_empty_hold = fleet.empty_hold - extraction

                                fleet_up = Fleet.objects.filter(id=fleet.id).update(hold=new_hold, ship_empty_mass=new_mass, empty_hold=new_empty_hold)


                        #  Дописать:
                        #     а) отнятие ресурсов из поля с учетом оставшегося размера
                        #     б) дописать пересчет трюма
                        #     в) переделать скрипт под каждую проверку
                        #       а) пересчет идет без проверки на окончание задачи
                        #       б) сделать пересчет оставшегося времени
                        #       в) сдеалть пересчет топлива в баке
                        #       г) сделать запуск следующей команды




                                # finish_time = extract_veryfication(fleet)


                elif flightplan.class_command == 6:
                    finish_time = scan_veryfication(fleet)
                    flightplan = Flightplan.objects.filter(id_fleet=fleet.id, status=0).first()

                if flightplan:
                    if flightplan.class_command == 1:
                        start_flight.start_flight(fleet.id, finish_time)
                    elif flightplan.class_command == 3:
                        start_extraction.start_extraction(fleet.id, finish_time)
                    elif flightplan.class_command == 6:
                        start_scaning.start_scaning(fleet.id, finish_time)
                else:
                    fleet_up = Fleet.objects.filter(id=fleet.id).update(status=0)





                    # lens = lens + 1
                    # if lens == flightplan_len:
                    # fleet_up = Fleet.objects.filter(id=fleet.id).update(status=0)
                    # else:
                    # flightplan = Flightplan.objects.filter(id_fleet=fleet.id).first().update(status=1)
                    #
                    # flightplan = Flightplan.objects.filter(id=flightplan_id).delete()


def add_res(*args):
    fleet=args[0]
    res=args[1]
    resource=args[2]

    if res:
        new_res = int(res.amount_shipment) + int(resource)
        up_res = Hold.objects.filter(fleet_id=fleet.id, class_shipment=0,
                                      id_shipment=1).update(amount_shipment=new_res)
    else:
        new_res=Hold(
            fleet_id = fleet.id,
            class_shipment = 0,
            id_shipment = 1,
            mount_shipment = resource,
            mass_shipment = resource,
            size_shipment = resource,

        )
        new_res.save()
