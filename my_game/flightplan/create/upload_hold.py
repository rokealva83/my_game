# -*- coding: utf-8 -*-

from datetime import datetime
from my_game.models import Flightplan, FlightplanHold
from my_game.flightplan.find_name import find_name


def upload_hold(*args):
    session_user = args[0]
    fleet = args[1]
    upload_amount = args[2]
    name_upload_element = args[3]

    name_upload_element = name_upload_element.split(';')
    element_id = int(name_upload_element[0])
    class_element = int(name_upload_element[1])
    name = find_name(class_element, element_id)

    flightplan = Flightplan(
        user=session_user,
        fleet=fleet,
        class_command=2,
        command_id=1,
        status=0
    )
    flightplan.save()

    flightplan_hold = FlightplanHold(
        user=session_user,
        fleet=fleet,
        command_id=1,
        amount=upload_amount,
        start_time=datetime.now(),
        flightplan=flightplan,
        time=300,
        class_element=class_element,
        element_id=element_id,
        name=name
    )
    flightplan_hold.save()
