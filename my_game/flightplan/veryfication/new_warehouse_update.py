# -*- coding: utf-8 -*-

from my_game.models import Warehouse, WarehouseElement, WarehouseFactory, WarehouseShip
from my_game.models import FactoryPattern


def new_warehouse_update(*args):
    class_element = args[0]
    city = args[1]
    flightplan_hold = args[2]
    new_amount = args[3]
    if class_element == 0:
        warehouse_up = Warehouse(
            user=city.user,
            user_city=city.id,
            id_resource=flightplan_hold.id_element,
            amount=new_amount
        )
        warehouse_up.save()
    elif class_element == 10:
        factory = FactoryPattern.objects.filter(id=flightplan_hold.id_element).first()
        warehouse_up = WarehouseFactory(
            user=city.user,
            user_city=city.id,
            factory_id=flightplan_hold.id_element,
            production_class=factory.production_class,
            production_id=factory.production_id,
            time_production=factory.time_production,
            amount=new_amount,
            size=factory.size,
            mass=factory.mass,
            power_consumption=factory.power_consumption
        )
        warehouse_up.save()
    elif class_element == 11:
        warehouse_up = WarehouseShip(
            user=city.user,
            user_city=city.id,
            ship_id=flightplan_hold.id_element,
            amount=new_amount
        )
        warehouse_up.save()
    else:
        warehouse_up = WarehouseElement(
            user=city.user,
            user_city=city.id,
            element_class=flightplan_hold.class_element,
            element_id=flightplan_hold.id_element,
            amount=new_amount
        )
        warehouse_up.save()
    return True
