# -*- coding: utf-8 -*-

from my_game.models import Fleet_parametr_resource_extraction
from my_game.models import Flightplan, Flightplan_production


def resource_extraction(*args):
    session_user = args[0]
    fleet_id = args[1]
    fleet = args[2]
    time_extraction = int(args[3])
    time_extraction = time_extraction*60
    full_hold = args[4]

    fleet_parametr_resource_extraction = Fleet_parametr_resource_extraction.objects.filter(
        fleet_id=fleet_id).first()
    if full_hold:
        time_extraction = int(fleet.empty_hold / fleet_parametr_resource_extraction.extraction_per_minute)*60

    flightplan = Flightplan(
        user=session_user,
        id_fleet=fleet_id,
        class_command=3,
        id_command=1,
        status=0
    )
    flightplan.save()

    flightplan_production = Flightplan_production(
        user=session_user,
        id_fleet=fleet_id,
        id_fleetplan=flightplan.id,
        id_command=1,
        production_per_minute=fleet_parametr_resource_extraction.extraction_per_minute,
        time_extraction=time_extraction
    )
    flightplan_production.save()