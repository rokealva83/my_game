# -*- coding: utf-8 -*-

from datetime import datetime
from my_game.models import Flightplan, Flightplan_refill
from my_game.models import Hold
from my_game.flightplan.find_name import find_name


def refill(*args):
    session_user = args[0]
    fleet_id = args[1]
    request = args[2]
    refill_fleet = request.POST.get('refill_fleet')
    overload = request.POST.get('overload')
    yourself = request.POST.get('yourself')

    id_command = 0
    id_fleet_refill = 0
    class_refill = 0
    class_element = 0
    id_element = 0
    amount = 0
    time = 0
    name = ''

    if yourself:
        id_command = 1
        id_fleet_refill = fleet_id
        amount = request.POST.get('yourself_amount')
        class_element = 14
        id_fuel_yourself = request.POST.get('id_fuel_yourself')
        id_fuel_yourself = id_fuel_yourself.split(';')
        id_element = id_fuel_yourself[0]
        class_refill = 1
        time = 150
        name = find_name(class_element, id_element)
        yourself_full_tank = request.POST.get('yourself_full_tank')
        if yourself_full_tank:
            class_refill = 2
            amount = 0
            time = 300

    if refill_fleet:
        id_command = 2
        id_fleet_refill = request.POST.get('fleet_number')
        id_element = request.POST.get('id_fuel')
        amount = request.POST.get('amount')
        hold = Hold.objects.filter(id=id_element).first()
        name = find_name(hold.class_shipment, hold.id_shipment)
        class_refill = 1
        class_element = 0
        time = 150
        full_tank = request.POST.get('full_tank')
        if full_tank:
            class_refill = 2
            amount = 0
            time = 300

    elif overload:
        id_command = 3
        id_element = request.POST.get('id_hold_element')
        amount = request.POST.get('overload_amount')
        id_fleet_refill = request.POST.get('overload_fleet_number')
        hold = Hold.objects.filter(id=id_element).first()
        name = find_name(hold.class_shipment, hold.id_shipment)
        class_refill = 1
        class_element = 0
        time = 300
        all_goods = request.POST.get('all_goods')
        if all_goods:
            class_refill = 2
            amount = 0
            time = 450

    flightplan = Flightplan(
        user=session_user,
        id_fleet=fleet_id,
        class_command=4,
        id_command=id_command,
        status=0
    )
    flightplan.save()

    flightplan_refill = Flightplan_refill(
        user=session_user,
        id_fleet=fleet_id,
        id_command=id_command,
        id_fleet_refill=id_fleet_refill,
        class_refill=class_refill,
        class_element=class_element,
        id_element=id_element,
        amount=amount,
        start_time=datetime.now(),
        time_refill=time,
        id_fleetplan=flightplan.id,
        name=name
    )
    flightplan_refill.save()