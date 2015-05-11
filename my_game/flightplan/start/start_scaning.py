# -*- coding: utf-8 -*-

from datetime import datetime
from my_game.models import Fleet
from my_game.models import Flightplan, Flightplan_scan


def start_scaning(*args):
    fleet_id = args[0]

    start_time = 0

    if len(args) == 1:
        start_time = datetime.now()

    flightplan = Flightplan.objects.filter(id_fleet=fleet_id).first()
    id_flightplan = flightplan.pk

    flightplan_scan = Flightplan_scan.objects.filter(id_fleet=fleet_id).first()
    flightplan_scan = Flightplan_scan.objects.filter(id=flightplan_scan.pk).update(start_time=start_time)
    flightplan = Flightplan.objects.filter(id=id_flightplan).update(status=1)
    fleet = Fleet.objects.filter(id=fleet_id).update(status=True, planet_status=0)