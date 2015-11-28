# -*- coding: utf-8 -*-

from datetime import datetime
from my_game.models import Flightplan, FlightplanRefill
from my_game.models import Hold
from my_game.flightplan.find_name import find_name
from my_game.models.base_models import UserVariables


def refill(*args):
    session_user = args[0]
    fleet = args[1]
    request = args[2]
    refill_fleet = request.POST.get('refill_fleet')
    overload = request.POST.get('overload')
    yourself = request.POST.get('yourself')

    command_id = fleet_refill_id = class_refill = class_element = element_id = amount = time = 0
    name = ''

    if yourself:
        command_id = 1
        fleet_refill_id = fleet.id
        amount = request.POST.get('yourself_amount')
        class_element = 14
        fuel_yourself_id = request.POST.get('id_fuel_yourself')
        fuel_yourself_id = fuel_yourself_id.split(';')
        element_id = fuel_yourself_id[0]
        class_refill = 1
        time = UserVariables.objects.first().time_refill_youself_all_goods
        name = find_name(class_element, element_id)
        yourself_full_tank = request.POST.get('yourself_full_tank')
        if yourself_full_tank:
            class_refill = 2
            amount = 0
            time = UserVariables.objects.first().time_refill_youself

    if refill_fleet:
        command_id = 2
        fleet_refill_id = request.POST.get('fleet_number')
        element_id = request.POST.get('id_fuel')
        amount = request.POST.get('amount')
        hold = Hold.objects.filter(id=element_id).first()
        name = find_name(hold.class_shipment, hold.id_shipment)
        class_refill = 1
        class_element = 0
        time = UserVariables.objects.first().time_refill
        full_tank = request.POST.get('full_tank')
        if full_tank:
            class_refill = 2
            amount = 0
            time = UserVariables.objects.first().time_refill_all_goods

    elif overload:
        command_id = 3
        element_id = request.POST.get('id_hold_element')
        amount = request.POST.get('overload_amount')
        fleet_refill_id = request.POST.get('overload_fleet_number')
        hold = Hold.objects.filter(fleet=fleet, class_shipment=class_element, shipment_id=element_id).first()
        name = find_name(hold.class_shipment, hold.id_shipment)
        class_refill = 1
        class_element = 0
        time = UserVariables.objects.first().time_refill
        all_goods = request.POST.get('all_goods')
        if all_goods:
            class_refill = 2
            amount = 0
            time = UserVariables.objects.first().time_refill_all_goods

    flightplan = Flightplan(
        user=session_user,
        fleet=fleet,
        class_command=4,
        command_id=command_id,
        status=0
    )
    flightplan.save()

    flightplan_refill = FlightplanRefill(
        user=session_user,
        id_fleet=fleet,
        command_id=command_id,
        id_fleet_refill=fleet_refill_id,
        class_refill=class_refill,
        class_element=class_element,
        element_id=element_id,
        amount=amount,
        start_time=datetime.now(),
        time_refill=time,
        flightplan=flightplan,
        name=name
    )
    flightplan_refill.save()
