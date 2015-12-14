# -*- coding: utf-8 -*-


from django.shortcuts import render
from my_game.models import MyUser, UserCity, Warehouse, UserVariables
from my_game.models import WarehouseElement
from my_game.models import Ship
from my_game.models import HullPattern, ShieldPattern, GeneratorPattern, EnginePattern, \
    ArmorPattern, ModulePattern, WeaponPattern
from my_game.models import ProjectShip, ElementShip, TurnShipBuild
import math
from datetime import datetime, timedelta


def error_function(*args):
    session_user_city = args[0]
    new_ship_element = args[1]
    new_ship_project = args[2]
    ship_amount = args[3]
    id_element = new_ship_element.id_element_pattern
    class_element = new_ship_element.class_element
    amount_element = len(
        ElementShip.objects.filter(project_ship=new_ship_project, class_element=class_element,
                                   id_element_pattern=id_element)) * int(ship_amount)
    warehouse_element = WarehouseElement.objects.filter(user_city=session_user_city,
                                                        element_class=class_element,
                                                        element_id=id_element).first()
    warehouse_element_amount = int(warehouse_element.amount)

    if warehouse_element_amount < amount_element:
        error = True
    else:
        error = False
    return error
