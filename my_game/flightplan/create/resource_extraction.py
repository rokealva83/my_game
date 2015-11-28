# -*- coding: utf-8 -*-

from my_game.models import FleetParametrResourceExtraction
from my_game.models import Flightplan, FlightplanProduction


def resource_extraction(*args):
    session_user = args[0]
    fleet = args[1]
    time_extraction = int(args[2])
    time_extraction *= 60
    full_hold = args[3]

    fleet_parametr_resource_extraction = FleetParametrResourceExtraction.objects.filter(fleet=fleet).first()
    if full_hold:
        time_extraction = int(fleet.empty_hold / fleet_parametr_resource_extraction.extraction_per_minute) * 60

    flightplan = Flightplan(
        user=session_user,
        fleet=fleet,
        class_command=3,
        command_id=1,
        status=0
    )
    flightplan.save()

    flightplan_production = FlightplanProduction(
        user=session_user,
        fleet=fleet,
        fleetplan=flightplan,
        command_id=1,
        production_per_minute=fleet_parametr_resource_extraction.extraction_per_minute,
        time_extraction=time_extraction
    )
    flightplan_production.save()
