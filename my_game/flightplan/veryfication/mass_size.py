# -*- coding: utf-8 -*-

from my_game.models import Warehouse, WarehouseElement, WarehouseFactory, WarehouseShip
from my_game.models import Ship, ProjectShip, HullPattern
from my_game.flightplan.veryfication.search_pattern import search_pattern


def mass_size(*args):
    class_element = args[0]
    city = args[1]
    flightplan_hold = args[2]
    mass = 0
    size = 0
    if class_element == 0:
        warehouse = Warehouse.objects.filter(user_city=city.id, id_resource=flightplan_hold.id_element).first()
        size = 1
        mass = 1
    elif class_element == 10:
        warehouse = WarehouseFactory.objects.filter(user_city=city.id, id=flightplan_hold.id_element).first()
        if warehouse:
            size = warehouse.size
            mass = warehouse.mass
    elif class_element == 11:
        warehouse = WarehouseShip.objects.filter(user_city=city.id, id=flightplan_hold.id_element).first()
        if warehouse:
            ship = Ship.objects.filter(id=warehouse.ship_id).first()
            project_ship = ProjectShip.objects.filter(id=ship.id_project_ship).first()
            hull = HullPattern.objects.filter(id=project_ship.hull_id).first()
            size = hull.size
            mass = project_ship.mass
    else:
        warehouse = WarehouseElement.objects.filter(user_city=city.id, element_class=class_element,
                                                    element_id=flightplan_hold.id_element).first()
        if warehouse:
            pattern = search_pattern(class_element, warehouse)
            if class_element != 2:
                size = pattern.size
            else:
                size = pattern.mass / 4
            mass = pattern.mass
    answer = [warehouse, size, mass]
    return answer
