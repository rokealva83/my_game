# -*- coding: utf-8 -*-

from datetime import datetime
from my_game.models import Flightplan, FlightplanHold
from my_game.models import Hold
from my_game.flightplan.find_name import find_name


def unload_hold(*args):
    session_user = args[0]
    fleet = args[1]
    unload_all = args[2]
    unload_all_hold = args[3]
    unload_amount = args[4]
    hold_element_id = args[5]

    command_id = 0
    time = 0

    hold = Hold.objects.filter(id=hold_element_id).first()
    class_element = hold.class_shipment
    element_id = hold.shipment_id

    name = find_name(class_element, element_id)
    error = 0
    if unload_all_hold:
        command_id = 4
        unload_amount = 0
        class_element = 0
        element_id = 0
        time = 600
    elif unload_all:
        command_id = 3
        unload_amount = hold.amount_shipment
        class_element = 0
        element_id = hold_element_id
        time = 300
    else:
        if unload_amount:
            command_id = 2
            class_element = hold.class_shipment
            element_id = hold.shipment_id
            time = 150
        else:
            message = ''
            error = 1
    if error == 0:
        flightplan = Flightplan(
            user=session_user,
            fleet=fleet,
            class_command=2,
            command_id=command_id,
            status=0
        )
        flightplan.save()

        flightplan_hold = FlightplanHold(
            user=session_user,
            fleet=fleet,
            command_id=command_id,
            amount=unload_amount,
            start_time=datetime.now(),
            fleetplan=flightplan,
            time=time,
            class_element=class_element,
            element=element_id,
            name=name
        )
        flightplan_hold.save()