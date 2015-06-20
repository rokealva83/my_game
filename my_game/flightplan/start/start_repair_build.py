# -*- coding: utf-8 -*-


from datetime import datetime
from my_game.models import Fleet, Fuel_pattern, Fuel_tank
from my_game.models import Flightplan, Flightplan_build_repair
from my_game.flightplan.fuel import fuel_process


def start_repair_build(*args):
    fleet_id = args[0]
    fleet = Fleet.objects.filter(id=fleet_id).first()
    flightplan = Flightplan.objects.filter(id_fleet=fleet_id).first()
    flightplan_repair = Flightplan_build_repair.objects.filter(id_fleet=fleet_id).first()
    error = 0
    message = ''

    # Проверка наличия необходимого количества ресурсов для ремонта. Пороверка на наличие болванки для развертывания

    need_fuel = fuel_process(fleet_id, flightplan_repair, flightplan)
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

            flightplan_repair = Flightplan_build_repair.objects.filter(id_fleet=fleet_id).first()
            flightplan_repair = Flightplan_build_repair.objects.filter(id=flightplan_repair.pk).update(
                start_time=start_time)
            flightplan = Flightplan.objects.filter(id=id_flightplan).update(status=1)
            fleet = Fleet.objects.filter(id=fleet_id).update(status=True, planet_status=0)
    else:
        message = 'Нет топлива'
    return message
