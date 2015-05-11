# -*- coding: utf-8 -*-

from datetime import datetime
from my_game.models import Flightplan, Flightplan_build_repair, Fleet_parametr_build_repair
from my_game.models import Factory_pattern, Hold


def repair_build(*args):
    session_user = args[0]
    fleet_id = args[1]
    request = args[2]
    repair = request.POST.get('repair')
    build = request.POST.get('build')

    id_command = 0
    time = 0
    fleet_repair = 0

    if build:
        id_hold_factory = request.POST.get('id_factory')
        id_command = 5
        fleet_repair = 0
        hold = Hold.objects.filter(id=id_hold_factory).first()
        factory = Factory_pattern.objects.filter(id=hold.id_shipment).first().time_deployment
        fleet_parametr_build = Fleet_parametr_build_repair.objects.filter(fleet_id=fleet_id,
                                                                          class_process=1).first().process_per_minute
        time = factory * fleet_parametr_build

    if repair:
        fleet_repair = request.POST.get('fleet_number')
        repair_yourself = request.POST.get('repair_yourself')
        id_command = 7
        if repair_yourself:
            fleet_repair = fleet_id
        time = 0

    flightplan = Flightplan(
        user=session_user,
        id_fleet=fleet_id,
        class_command=id_command,
        id_command=id_command,
        status=0
    )
    flightplan.save()

    flightplan_build_repair = Flightplan_build_repair(
        id_fleet=fleet_id,
        id_fleetplan=flightplan.id,
        id_command=id_command,
        fleet_repair=fleet_repair,
        start_time=datetime.now(),
        time=time,
    )
    flightplan_build_repair.save()
