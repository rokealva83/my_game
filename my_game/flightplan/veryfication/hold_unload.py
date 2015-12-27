# -*- coding: utf-8 -*-

from my_game.models import Fleet, Hold
from my_game.flightplan.veryfication.mass_size import mass_size
from my_game.flightplan.veryfication.warehouse_update import warehouse_update
from my_game.flightplan.veryfication.new_warehouse_update import new_warehouse_update


def hold_unload(*args):
    fleet = args[0]
    flightplan = args[1]
    flightplan_hold = args[2]
    class_element = flightplan_hold.class_element
    city = args[3]
    hold = args[4]
    if flightplan.id_command == 2:
        amount = flightplan_hold.amount
        if hold.amount_shipment < amount:
            amount = hold.amount_shipment
    else:
        amount = hold.amount_shipment
    answer = mass_size(class_element, city, flightplan_hold)
    warehouse = answer[0]
    delete_size = answer[1] * amount
    delete_mass = answer[2] * amount

    if warehouse:
        new_amount = warehouse.amount + amount
        warehouse_update(class_element, city, flightplan_hold, new_amount)
    else:
        new_warehouse_update(class_element, city, flightplan_hold, amount)

    if flightplan.id_command == 3:
        Hold.objects.filter(fleet_id=fleet.id, class_shipment=flightplan_hold.class_element,
                            id_shipment=flightplan_hold.id_element).delete()
    elif flightplan.id_command == 2:
        amount = flightplan_hold.amount
        if amount < hold.amount_shipment:
            new_amount = hold.amount_shipment - amount
            Hold.objects.filter(fleet_id=fleet.id, class_shipment=flightplan_hold.class_element,
                                id_shipment=flightplan_hold.id_element).update(amount_shipment=new_amount)
        else:
            Hold.objects.filter(fleet_id=fleet.id, class_shipment=flightplan_hold.class_element,
                                id_shipment=flightplan_hold.id_element).delete()
    new_fleet_mass = fleet.ship_empty_mass - delete_mass
    new_empty_hold = fleet.empty_hold - delete_size
    Fleet.objects.filter(id=fleet.id).update(empty_hold=new_empty_hold, ship_empty_mass=new_fleet_mass)
    return True
