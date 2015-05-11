# -*- coding: utf-8 -*-

from datetime import datetime
from my_game.models import Fleet
from my_game.models import Flightplan
from my_game.models import Flightplan_colonization
from my_game.models import Hold, Device_pattern


def start_colonization(*args):
    fleet_id = args[0]

    start_time = 0

    fleet = Fleet.objects.filter(id=fleet_id).first()
    flightplan = Flightplan.objects.filter(id_fleet=fleet_id).first()
    hold_modules = Hold.objects.filter(fleet_id=fleet_id, class_shipment=9)
    error = 1
    message = 'В трюме нет необходимого колонизационного устройства'

    if fleet.planet != 0 and flightplan.id_command == 1:
        for hold_module in hold_modules:
            device = int(Device_pattern.objects.filter(id=hold_module.id_shipment).first().param3)
            if device == 1:
                error = 0
                message = 'Колонизация начата'

    elif fleet.planet == 0 and flightplan.id_command == 2:
        for hold_module in hold_modules:
            device = int(Device_pattern.objects.filter(id=hold_module.id_shipment).first().param3)
            if device == 2:
                error = 0
                message = 'Развертка основы базы начата'

    if error == 0:
        if len(args) == 1:
            start_time = datetime.now()

        id_flightplan = flightplan.pk
        flightplan_colonization = Flightplan_colonization.objects.filter(id_fleet=fleet_id).first()
        flightplan_colonization = Flightplan_colonization.objects.filter(id=flightplan_colonization.pk).update(
            start_time=start_time)
        flightplan = Flightplan.objects.filter(id=id_flightplan).update(status=1)
        fleet = Fleet.objects.filter(id=fleet_id).update(status=True, planet_status=0)

    return message