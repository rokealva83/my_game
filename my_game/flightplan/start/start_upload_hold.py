# -*- coding: utf-8 -*-


from datetime import datetime
from my_game.models import Flightplan, Flightplan_hold
from my_game.models import Fleet, Fuel_pattern, Fuel_tank
from my_game.flightplan.fuel import fuel_process


def start_upload(*args):
    fleet_id = args[0]
    fleet = Fleet.objects.filter(id=fleet_id).first()
    flightplan = Flightplan.objects.filter(id_fleet=fleet_id).first()
    id_flightplan = flightplan.pk
    flightplan_upload = Flightplan_hold.objects.filter(id_fleet=fleet_id).first()
    message = ''
    error = 0

    need_fuel = fuel_process(fleet_id, flightplan_upload, flightplan)
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
                start_time = args[2]

            flightplan_upload = Flightplan_hold.objects.filter(id_fleet=fleet_id).first()
            flightplan_upload = Flightplan_hold.objects.filter(id=flightplan_upload.pk).update(start_time=start_time)
            flightplan = Flightplan.objects.filter(id=id_flightplan).update(status=1)
            fleet = Fleet.objects.filter(id=fleet_id).update(status=True, planet_status=0)
    else:
        message = 'Нет топлива'

    return message