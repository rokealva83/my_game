# -*- coding: utf-8 -*-

from datetime import datetime
from my_game.models import Fleet, FuelTank, FuelPattern
from my_game.models import Flightplan, FlightplanFlight
from my_game.flightplan import fuel


def start_flight(*args):
    fleet_id = args[0]
    fleet = Fleet.objects.filter(id=fleet_id).first()

    error = 0
    # Повверка наличия топлива в зависимости от варианта полета. Проверка достаточности топлива для полета.
    flightplan = Flightplan.objects.filter(id_fleet=fleet_id).first()
    id_flightplan = flightplan.pk
    flightplan_flight = FlightplanFlight.objects.filter(id_fleet=fleet_id, id_command=flightplan.id_command).first()
    message = ''
    if flightplan_flight:
        flightplan_flight_id = flightplan_flight.pk
        need_fuel = fuel.fuel(fleet_id, flightplan_flight, fleet)
        fuel_tank = FuelTank.objects.filter(fleet_id=fleet_id).first()
        if fuel_tank:
            fuel_pattern = FuelPattern.objects.filter(user=fleet.user, fuel_class=fuel_tank.fuel_class).first()
            if need_fuel > fuel_tank.amount_fuel * fuel_pattern.efficiency:
                error = 1
                message = 'Нет топлива'

            if error == 0:
                if len(args) == 1:
                    start_time = datetime.now()
                else:
                    start_time = args[1]
                flightplan_flight = FlightplanFlight.objects.filter(id=flightplan_flight_id).update(
                    start_time=start_time)
                flightplan = Flightplan.objects.filter(id=id_flightplan).update(status=1)
                fleet = Fleet.objects.filter(id=fleet_id).update(status=True, planet_status=0)
        else:
            message = 'Нет топлива'

        return message
