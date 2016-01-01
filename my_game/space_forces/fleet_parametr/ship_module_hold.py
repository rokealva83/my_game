# -*- coding: utf-8 -*-

from my_game.models import ModulePattern


def ship_module_hold(*args):
    ship_elements = args[0]
    ship_module_hold = 0
    for ship_element in ship_elements:
        if ship_element.class_element == 8:
            element_pattern = ModulePattern.objects.filter(id=ship_element.element_pattern_id, module_class=2).first()
            if element_pattern:
                ship_module_hold += element_pattern.param1
    return ship_module_hold
