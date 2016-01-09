# -*- coding: utf-8 -*-

from datetime import datetime
from my_game.models import Flightplan, FlightplanRefill
from my_game.models import Hold, FleetFuelRefill, FleetOverload
from my_game.flightplan.find_name import find_name
from my_game.models.base_models import UserVariables
from ast import literal_eval


def refill(*args):
    session_user = args[0]
    fleet = args[1]
    request = args[2]
    refill_fleet = request.POST.get('refill_fleet')
    overload = request.POST.get('overload')
    yourself = request.POST.get('yourself')
    user_variables = UserVariables.objects.first()

    command_id = fleet_refill_id = class_refill = class_element = element_id = amount = time = error = 0
    name = message = ''

    if yourself:
        command_id = 1
        fleet_refill_id = fleet.id
        amount = request.POST.get('yourself_amount')
        class_element = 14
        fuel_yourself_id = request.POST.get('id_fuel_yourself')
        fuel_yourself_id = fuel_yourself_id.split(';')
        element_id = fuel_yourself_id[0]
        class_refill = 1
        time = user_variables.time_refill
        name = find_name(class_element, element_id)
        yourself_full_tank = request.POST.get('yourself_full_tank')
        if yourself_full_tank:
            class_refill = 2
            amount = 0
            time = UserVariables.objects.first().time_refill_all_goods

    if refill_fleet:
        fuel_refill = FleetFuelRefill.objects.filter(fleet=fleet).first()
        command_id = 2
        fleet_refill_id = request.POST.get('fleet_number')
        element_id = request.POST.get('id_fuel')
        amount = request.POST.get('amount')
        if fleet_refill_id:
            hold = Hold.objects.filter(id=element_id).first()
            name = find_name(hold.class_shipment, hold.shipment_id)
            class_refill = 1
            class_element = 0
            full_tank = request.POST.get('full_tank')
            if full_tank:
                class_refill = 2
                amount = 0
                time = 0
            else:
                time = int(amount) / (int(fuel_refill.fuel_refill) / 60)
        else:
            message = 'Не задано номер флота'
            error = 1

    elif overload:
        overload = FleetOverload.objects.filter(fleet=fleet).first()
        command_id = 3
        element_id = request.POST.get('id_hold_element')
        amount = request.POST.get('overload_amount')
        fleet_refill_id = request.POST.get('overload_fleet_number')
        all_goods = request.POST.get('all_goods')
        if fleet_refill_id:
            if element_id and len(element_id) != 1:
                element_ids = [item for item in literal_eval(element_id)]
                element_id = element_ids[1]
                class_element = 0
                name = find_name(class_element, element_id)
                class_refill = 1
                if not amount:
                    if all_goods:
                        amount = 0
                        class_refill = 2
                    else:
                        error = 1
                        message = 'Не задано количество товара'
            else:
                if element_id:
                    hold = Hold.objects.filter(id=element_id).first()
                    class_element = hold.class_shipment
                    element_id = hold.shipment_id
                    name = find_name(class_element, element_id)
                    class_refill = 1
                    if amount:
                        time = int(amount) / (int(overload.overload) / 60)
                    else:
                        if all_goods:
                            amount = 0
                            class_refill = 2
                        else:
                            error = 1
                            message = 'Не задано количество товара'
                elif all_goods:
                    class_element = 0
                    class_refill = 2
                    element_id = 0
                    amount = 0
                    time = 0
                else:
                    message = 'Не выбрано товара'
                    error = 1
        else:
            message = 'Не задано номер флота'
            error = 1
    if not error:
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
            fleet=fleet,
            command_id=command_id,
            fleet_refill_id=fleet_refill_id,
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
    return message
