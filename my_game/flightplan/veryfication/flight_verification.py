# -*- coding: utf-8 -*-

from datetime import timedelta
from django.utils import timezone
from my_game.models import Planet, System
from my_game.models import Fleet
from my_game.models import Flightplan, FlightplanFlight
from my_game.flightplan.fuel import fuel
from my_game.flightplan.minus_fuel import minus_fuel


def verification_flight(*args):
    fleet = args[0]
    flightplan = Flightplan.objects.filter(fleet=fleet.id).first()
    if flightplan:
        finish_time = timezone.now()
        flightplan_flight = FlightplanFlight.objects.filter(fleetplan=flightplan.id).first()
        if flightplan_flight:
            time = timezone.now()
            time_start = flightplan_flight.start_time
            delta_time = time - time_start
            new_delta = delta_time.total_seconds()
            delta = flightplan_flight.flight_time
            if new_delta > delta:
                finish_time = time_start + timedelta(seconds=delta)
                if flightplan_flight.planet != 0:
                    planet_status = 1
                    system = System.objects.filter(id=flightplan_flight.system_id).first()
                    planet = Planet.objects.filter(system=system, planet_num=flightplan_flight.planet_id).first()
                    x = planet.global_x
                    y = planet.global_y
                    z = planet.global_z

                else:
                    planet_status = 0
                    x = flightplan_flight.finish_x
                    y = flightplan_flight.finish_y
                    z = flightplan_flight.finish_z

                Fleet.objects.filter(id=fleet.id).update(x=x, y=y, z=z, planet_status=planet_status,
                                                         planet=flightplan_flight.planet,
                                                         system=flightplan_flight.system)

                need_fuel = fuel(fleet.id, flightplan_flight, fleet)
                minus_fuel(fleet, need_fuel)

                FlightplanFlight.objects.filter(fleetplan=flightplan.id).delete()
                Flightplan.objects.filter(id=flightplan.id).delete()
            else:
                new_x = flightplan_flight.start_x - (
                    (flightplan_flight.start_x - flightplan_flight.finish_x) / (
                        flightplan_flight.flight_time * new_delta))
                new_y = flightplan_flight.start_y - (
                    (flightplan_flight.start_y - flightplan_flight.finish_y) / (
                        flightplan_flight.flight_time * new_delta))
                new_z = flightplan_flight.start_z - (
                    (flightplan_flight.start_z - flightplan_flight.finish_z) / (
                        flightplan_flight.flight_time * new_delta))
                Fleet.objects.filter(id=fleet.id).update(x=new_x, y=new_y, z=new_z, planet_status=0, planet=0, system=0)
            return finish_time
