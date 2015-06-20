# -*- coding: utf-8 -*-


from datetime import datetime
from my_game.models import Fleet
from my_game.models import Flightplan, Flightplan_hold
from my_game.flightplan.fuel import fuel_process


def start_upload(*args):
    fleet_id = args[0]
    flightplan = Flightplan.objects.filter(id_fleet=fleet_id).first()
    id_flightplan = flightplan.pk

    if len(args) == 1:
        start_time = datetime.now()
    else:
        start_time = args[1]

    flightplan_upload = Flightplan_hold.objects.filter(id_fleet=fleet_id).first()
    flightplan_upload = Flightplan_hold.objects.filter(id=flightplan_upload.pk).update(start_time=start_time)
    flightplan = Flightplan.objects.filter(id=id_flightplan).update(status=1)
    fleet = Fleet.objects.filter(id=fleet_id).update(status=True, planet_status=0)