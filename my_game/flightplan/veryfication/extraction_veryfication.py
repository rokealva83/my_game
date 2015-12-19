# -*- coding: utf-8 -*-

from datetime import timedelta
from django.utils import timezone
from my_game.models import AsteroidField, FleetParametrResourceExtraction
from my_game.models import Fleet, Ship
from my_game.models import Flightplan, FlightplanProduction, Hold
from my_game.flightplan.fuel import need_fuel_process, minus_fuel



def extraction_veryfication(*args):
    fleet = args[0]
    flightplan = Flightplan.objects.filter(id_fleet=fleet.id).first()
    flightplan_extraction = FlightplanProduction.objects.filter(id_fleetplan=flightplan.id).first()
    if flightplan_extraction:

        time = timezone.now()
        time_start = flightplan_extraction.start_time
        time_extraction = int(flightplan_extraction.time_extraction)
        delta_time = time - time_start
        new_delta = delta_time.total_seconds()
        if time_extraction > new_delta:
            delta = new_delta
            finish_time = time + timedelta(seconds=time_extraction)
        else:
            delta = time_extraction
            finish = new_delta - time_extraction
            finish_time = time - timedelta(seconds=finish)

        fleet_resource_extraction = FleetParametrResourceExtraction.objects.filter(
            fleet_id=fleet.id).first()
        extract_per_second = int(fleet_resource_extraction.extraction_per_minute) / 60
        extraction = delta * extract_per_second
        x = fleet.x
        y = fleet.y
        z = fleet.z

        asteroid_field = AsteroidField.objects.filter(x=x, y=y, z=z).first()
        if asteroid_field:
            if extraction > fleet.empty_hold:
                extraction = fleet.empty_hold
                if extraction > asteroid_field.size:
                    extraction = asteroid_field.size
                    asteroid_field = AsteroidField.objects.filter(x=x, y=y, z=z).delete()
                else:
                    new_size = asteroid_field.size - extraction
                    asteroid_field = AsteroidField.objects.filter(x=x, y=y, z=z).update(size=new_size)

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
            fleet_up = Fleet.objects.filter(id=fleet.id).update(hold=new_hold, ship_empty_mass=new_mass,
                                                                empty_hold=new_empty_hold)
            new_time = flightplan_extraction.time_extraction - delta
            if new_time > 0:
                flightplan_extraction = FlightplanProduction.objects.filter(id_fleetplan=flightplan.id).update(
                    start_time=time, time_extraction=new_time)
            else:
                flightplan_del = Flightplan.objects.filter(id=flightplan.id).delete()
                flightplan_extraction_del = FlightplanProduction.objects.filter(id=flightplan_extraction.id).delete()

            ship_in_fleets = Ship.objects.filter(fleet_status=1, place_id=fleet.id)
            need_fuel = need_fuel_process(ship_in_fleets, flightplan, delta, fleet.id)
            minus_fuel(fleet, need_fuel)

            return finish_time


def add_res(*args):
    fleet = args[0]
    res = args[1]
    resource = args[2]

    if res:
        new_res = int(res.amount_shipment) + int(resource)
        up_res = Hold.objects.filter(fleet_id=fleet.id, class_shipment=0,
                                     id_shipment=1).update(amount_shipment=new_res)
    else:
        new_res = Hold(
            fleet_id=fleet.id,
            class_shipment=0,
            id_shipment=1,
            mount_shipment=resource,
            mass_shipment=resource,
            size_shipment=resource,

        )
        new_res.save()
