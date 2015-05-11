# -*- coding: utf-8 -*-


from datetime import datetime
from my_game.models import Fleet
from my_game.models import Flightplan, Flightplan_build_repair


def start_repair_build(*args):
    fleet_id = args[0]

    start_time = 0

    # Проверка наличия необходимого количества ресурсов для ремонта. Пороверка на наличие болванки для развертывания

    if len(args) == 1:
        start_time = datetime.now()

    flightplan = Flightplan.objects.filter(id_fleet=fleet_id).first()
    id_flightplan = flightplan.pk

    flightplan_repair = Flightplan_build_repair.objects.filter(id_fleet=fleet_id).first()
    flightplan_repair = Flightplan_build_repair.objects.filter(id=flightplan_repair.pk).update(start_time=start_time)
    flightplan = Flightplan.objects.filter(id=id_flightplan).update(status=1)
    fleet = Fleet.objects.filter(id=fleet_id).update(status=True, planet_status=0)
