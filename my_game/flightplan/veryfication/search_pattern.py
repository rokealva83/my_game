# -*- coding: utf-8 -*-

from my_game.models import ArmorPattern, ShieldPattern, WeaponPattern, \
    EnginePattern, GeneratorPattern, ShellPattern, ModulePattern, DevicePattern
from my_game.models import HullPattern


def search_pattern(*args):
    class_element = args[0]
    warehouse = args[1]
    pattern = None
    if class_element == 1:
        pattern = HullPattern.objects.filter(id=warehouse.id_element).first()
    elif class_element == 2:
        pattern = ArmorPattern.objects.filter(id=warehouse.id_element).first()
    elif class_element == 3:
        pattern = ShieldPattern.objects.filter(id=warehouse.id_element).first()
    elif class_element == 4:
        pattern = EnginePattern.objects.filter(id=warehouse.id_element).first()
    elif class_element == 5:
        pattern = GeneratorPattern.objects.filter(id=warehouse.id_element).first()
    elif class_element == 6:
        pattern = WeaponPattern.objects.filter(id=warehouse.id_element).first()
    elif class_element == 7:
        pattern = ShellPattern.objects.filter(id=warehouse.id_element).first()
    elif class_element == 8:
        pattern = ModulePattern.objects.filter(id=warehouse.id_element).first()
    elif class_element == 9:
        pattern = DevicePattern.objects.filter(id=warehouse.id_element).first()

    return pattern
