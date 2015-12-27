# -*- coding: utf-8 -*-

from datetime import datetime
from my_game.models import Fleet, FuelPattern, FuelTank
from my_game.models import Flightplan, FlightplanScan
from my_game.flightplan.fuel_process import fuel_process


def start_scaning(*args):
    fleet_id = args[0]
    fleet = Fleet.objects.filter(id=fleet_id).first()

    error = 0
    flightplan = Flightplan.objects.filter(id_fleet=fleet_id).first()
    flightplan_scan = FlightplanScan.objects.filter(id_fleet=fleet_id).first()
    message = ''
    need_fuel = fuel_process(fleet_id, flightplan_scan, flightplan)

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
                start_time = args[2]

            flightplan = Flightplan.objects.filter(id_fleet=fleet_id).first()
            id_flightplan = flightplan.pk

            FlightplanScan.objects.filter(id=flightplan_scan.pk).update(start_time=start_time)
            Flightplan.objects.filter(id=id_flightplan).update(status=1)
            Fleet.objects.filter(id=fleet_id).update(status=True, planet_status=0)
    else:
        message = 'Нет топлива'
    return message
