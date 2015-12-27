# -*- coding: utf-8 -*-

from datetime import timedelta
from django.utils import timezone
from my_game.models import Flightplan, FlightplanHold
from my_game.models import Ship, UserCity
from my_game.flightplan.need_fuel_process import need_fuel_process
from my_game.flightplan.minus_fuel import minus_fuel
from my_game.flightplan.veryfication.upload_hold_element import upload_hold_element
from my_game.flightplan.veryfication.unload_hold_element import unload_hold_element


def upload_unload_veryfication(*args):
    fleet = args[0]
    user = fleet.user
    flightplan = Flightplan.objects.filter(id_fleet=fleet.id).first()
    city = UserCity.objects.filter(user=user, x=fleet.x, y=fleet.y, z=fleet.z).first()
    finish_time = timezone.now()
    if city:
        flightplan_hold = FlightplanHold.objects.filter(id_fleetplan=flightplan.id).first()
        if flightplan_hold:
            time = timezone.now()
            time_start = flightplan_hold.start_time
            time_upload = flightplan_hold.time
            delta_time = time - time_start
            new_delta = delta_time.total_seconds()

            if new_delta > time_upload:
                finish_time = time_start + timedelta(seconds=time_upload)
                if flightplan.id_command == 1:
                    upload_hold_element(fleet, flightplan_hold, city)
                else:
                    unload_hold_element(fleet, flightplan, flightplan_hold, city)

                ship_in_fleets = Ship.objects.filter(fleet_status=1, place_id=fleet.id)
                need_fuel = need_fuel_process(ship_in_fleets, flightplan, time_upload, fleet.id)
                minus_fuel(fleet, need_fuel)

                Flightplan.objects.filter(id=flightplan.id).delete()
                FlightplanHold.objects.filter(id=flightplan_hold.id).delete()

    return finish_time
