# -*- coding: utf-8 -*-

from datetime import datetime
from my_game.models import Asteroid_field
from my_game.models import Fleet, Fuel_tank, Fuel_pattern
from my_game.models import Flightplan, Flightplan_production
from my_game.flightplan.fuel import fuel_process


def start_extraction(*args):
    fleet_id = args[0]
    error = 0
    fleet = Fleet.objects.filter(id=fleet_id).first()
    x = int(fleet.x)
    y = int(fleet.y)
    z = int(fleet.z)
    flightplan = Flightplan.objects.filter(id_fleet=fleet_id).first()
    asteroid_field = Asteroid_field.objects.filter(x=x, y=y, z=z).first()
    message = 'По даным координатам отсутствуют астероиды'
    if asteroid_field:
        message = ''
        flightplan_extraction = Flightplan_production.objects.filter(id_fleet=fleet_id).first()
        need_fuel = fuel_process(fleet_id, flightplan_extraction, flightplan)

        fuel_tank = Fuel_tank.objects.filter(fleet_id=fleet_id).first()
        if fuel_tank:
            fuel_pattern = Fuel_pattern.objects.filter(user=fleet.user, fuel_class=fuel_tank.fuel_class).first()
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
                flightplan_extraction = Flightplan_production.objects.filter(id=flightplan_extraction.pk).update(
                    start_time=start_time)
                flightplan = Flightplan.objects.filter(id=id_flightplan).update(status=1)
                fleet = Fleet.objects.filter(id=fleet_id).update(status=True, planet_status=0)
        else:
            message = 'Нет топлива'
    return message
