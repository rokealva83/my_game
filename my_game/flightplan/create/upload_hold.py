# -*- coding: utf-8 -*-

from datetime import datetime
from my_game.models import Flightplan, Flightplan_hold
from my_game.flightplan.find_name import find_name


def upload_hold(*args):
    session_user = args[0]
    fleet_id = args[1]
    upload_amount = args[2]
    name_upload_element = args[3]

    name_upload_element = name_upload_element.split(';')
    id_element = int(name_upload_element[0])
    class_element = int(name_upload_element[1])
    name = find_name(class_element, id_element)

    flightplan = Flightplan(
        user=session_user,
        id_fleet=fleet_id,
        class_command=2,
        id_command=1,
        status=0
    )
    flightplan.save()

    flightplan_hold = Flightplan_hold(
        user=session_user,
        id_fleet=fleet_id,
        id_command=1,
        amount=upload_amount,
        start_time=datetime.now(),
        id_fleetplan=flightplan.id,
        time=300,
        class_element=class_element,
        id_element=id_element,
        name=name
    )
    flightplan_hold.save()