# -*- coding: utf-8 -*-

from datetime import datetime
from my_game.models import AsteroidField
from my_game.models import Fleet, FuelTank, FuelPattern
from my_game.models import Flightplan, FlightplanProduction
from my_game.flightplan.fuel_process import fuel_process


def start_extraction(*args):
    fleet_id = args[0]
    error = 0
    fleet = Fleet.objects.filter(id=fleet_id).first()
    x = int(fleet.x)
    y = int(fleet.y)
    z = int(fleet.z)
    flightplan = Flightplan.objects.filter(id_fleet=fleet_id).first()
    asteroid_field = AsteroidField.objects.filter(x=x, y=y, z=z).first()
    message = 'По даным координатам отсутствуют астероиды'
    if asteroid_field:
        message = ''
        flightplan_extraction = FlightplanProduction.objects.filter(id_fleet=fleet_id).first()
        need_fuel = fuel_process(fleet_id, flightplan_extraction, flightplan)

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
                flightplan = Flightplan.objects.filter(id_fleet=fleet_id).first()
                id_flightplan = flightplan.pk
                FlightplanProduction.objects.filter(id=flightplan_extraction.pk).update(start_time=start_time)
                Flightplan.objects.filter(id=id_flightplan).update(status=1)
                Fleet.objects.filter(id=fleet_id).update(status=True, planet_status=0)
        else:
            message = 'Нет топлива'
    return message
