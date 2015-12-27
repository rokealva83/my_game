# -*- coding: utf-8 -*-

from my_game.models import Fleet
from my_game.models import Hold
from my_game.flightplan.veryfication.mass_size import mass_size
from my_game.flightplan.veryfication.warehouse_update import warehouse_update


def upload_hold_element(*args):
    fleet = args[0]
    flightplan_hold = args[1]
    class_element = flightplan_hold.class_element
    city = args[2]

    answer = mass_size(class_element, city, flightplan_hold)
    warehouse = answer[0]
    size = answer[1]
    mass = answer[2]

    if warehouse:
        need_amount = flightplan_hold.amount
        if need_amount > warehouse.amount:
            need_amount = warehouse.amount

        need_size = need_amount * size

        hold_size_free = fleet.empty_hold
        if need_size > hold_size_free:
            need_size = hold_size_free
            need_amount = int(need_size / size) - 1

        new_amount = warehouse.amount - need_amount

        warehouse_update(class_element, city, flightplan_hold, new_amount)

        fleet_hold = Hold.objects.filter(fleet_id=fleet.id, class_shipment=class_element,
                                         id_shipment=flightplan_hold.id_element).first()
        if fleet_hold:
            new_amount = fleet_hold.amount_shipment + need_amount
            new_size = fleet_hold.size_shipment + need_size
            new_mass = fleet_hold.mass_shipment + mass * need_amount
            Hold.objects.filter(fleet_id=fleet.id, class_shipment=class_element,
                                id_shipment=flightplan_hold.id_element).update(amount_shipment=new_amount,
                                                                               mass_shipment=new_mass,
                                                                               size_shipment=new_size)
        else:
            hold = Hold(
                fleet_id=fleet.id,
                class_shipment=class_element,
                id_shipment=flightplan_hold.id_element,
                amount_shipment=need_amount,
                mass_shipment=mass * need_amount,
                size_shipment=need_size
            )
            hold.save()

        new_fleet_mass = fleet.ship_empty_mass + mass * need_amount
        new_empty_hold = fleet.empty_hold - need_size
        Fleet.objects.filter(id=fleet.id).update(empty_hold=new_empty_hold, ship_empty_mass=new_fleet_mass)
        message = ''
    else:
        message = 'На складе нет такого модуля'

    return message
