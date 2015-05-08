# -*- coding: utf-8 -*-

from datetime import datetime
from my_game.models import Asteroid_field
from my_game.models import Fleet
from my_game.models import Flightplan, Flightplan_production


def start_extraction(*args):
    fleet_id = args[0]

    fleet = Fleet.objects.filter(id=fleet_id).first()
    x = fleet.x
    y = fleet.y
    z = fleet.z
    asteroid_field = Asteroid_field.objects.filter(x=x, y=y, z=z).first()
    message = 'По даным координатам отсутствуют астероиды'
    if asteroid_field:
        if len(args) == 1:
            start_time = datetime.now()

        flightplan = Flightplan.objects.filter(id_fleet=fleet_id).first()
        id_flightplan = flightplan.pk

        flightplan_extraction = Flightplan_production.objects.filter(id_fleet=fleet_id).first()
        flightplan_extraction = Flightplan_production.objects.filter(id=flightplan_extraction.pk).update(
            start_time=start_time)
        flightplan = Flightplan.objects.filter(id=id_flightplan).update(status=1)
        fleet = Fleet.objects.filter(id=fleet_id).update(status=True, planet_status=0)
        message = 'Переработка начата'

    return message