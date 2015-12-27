# -*- coding: utf-8 -*-

from my_game.models import Warehouse, WarehouseElement, WarehouseFactory, WarehouseShip


def warehouse_update(*args):
    class_element = args[0]
    city = args[1]
    flightplan_hold = args[2]
    new_amount = args[3]
    if class_element == 0:
        Warehouse.objects.filter(user_city=city.id, id_resource=flightplan_hold.id_element).update(amount=new_amount)
    elif class_element == 10:
        WarehouseFactory.objects.filter(user_city=city.id, id=flightplan_hold.id_element).update(amount=new_amount)
    elif class_element == 11:
        WarehouseShip.objects.filter(user_city=city.id, id=flightplan_hold.id_element).update(amount=new_amount)
    else:
        WarehouseElement.objects.filter(user_city=city.id, element_class=class_element,
                                        element_id=flightplan_hold.id_element).update(amount=new_amount)
    return True
