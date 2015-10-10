# -*- coding: utf-8 -*-

from datetime import datetime
from my_game.models import FleetParametrScan
from my_game.models import Flightplan, FlightplanScan


def scan(*args):
    session_user = args[0]
    fleet_id = args[1]
    method_scanning = args[2]
    fleet_parametr_scan = FleetParametrScan.objects.filter(fleet_id=fleet_id,
                                                             method_scanning=method_scanning).first()
    flightplan = Flightplan(
        user=session_user,
        id_fleet=fleet_id,
        class_command=6,
        id_command=method_scanning,
        status=0
    )
    flightplan.save()

    flightplan_scan = FlightplanScan(
        user=session_user,
        id_fleet=fleet_id,
        id_command=method_scanning,
        range_scanning=fleet_parametr_scan.range_scanning,
        start_time=datetime.now(),
        time_scanning=fleet_parametr_scan.time_scanning,
        id_fleetplan=flightplan.id
    )
    flightplan_scan.save()
