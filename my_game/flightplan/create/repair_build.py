# -*- coding: utf-8 -*-

from datetime import datetime
from my_game.models import Flightplan, FlightplanBuildRepair, FleetParametrBuildRepair
from my_game.models import FactoryPattern, Hold


def repair_build(*args):
    session_user = args[0]
    fleet = args[1]
    request = args[2]
    repair = request.POST.get('repair')
    build = request.POST.get('build')

    command_id = 0
    time = 0
    fleet_repair = 0

    if build:
        hold_factory_id = request.POST.get('id_factory')
        command_id = 5
        fleet_repair = 0
        hold = Hold.objects.filter(id=hold_factory_id).first()
        factory = FactoryPattern.objects.filter(id=hold.shipment_id).first().time_deployment
        fleet_parametr_build = FleetParametrBuildRepair.objects.filter(fleet=fleet,
                                                                          class_process=1).first().process_per_minute
        time = factory * fleet_parametr_build

    if repair:
        fleet_repair = request.POST.get('fleet_number')
        repair_yourself = request.POST.get('repair_yourself')
        command_id = 7
        if repair_yourself:
            fleet_repair = fleet
        time = 0

    flightplan = Flightplan(
        user=session_user,
        fleet=fleet,
        class_command=command_id,
        command_id=command_id,
        status=0
    )
    flightplan.save()

    flightplan_build_repair = FlightplanBuildRepair(
        fleet=fleet,
        fleetplan=flightplan,
        command_id=command_id,
        fleet_repair=fleet_repair,
        start_time=datetime.now(),
        time=time,
    )
    flightplan_build_repair.save()
