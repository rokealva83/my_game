# -*- coding: utf-8 -*-

from my_game.models import HullPattern, ShellPattern, ShieldPattern, GeneratorPattern, EnginePattern, \
    ArmorPattern, ModulePattern, WeaponPattern, FactoryInstalled, FuelPattern, DevicePattern


def rename_element_pattern(*args):
    pattern_id = args[2]
    element_id = args[3]
    new_names = args[4]
    factory = FactoryInstalled.objects.filter(id=pattern_id).first()
    production_class = factory.production_class
    if production_class == 1:
        HullPattern.objects.filter(id=element_id).update(name=new_names)
    if production_class == 2:
        ArmorPattern.objects.filter(id=element_id).update(name=new_names)
    if production_class == 3:
        ShieldPattern.objects.filter(id=element_id).update(name=new_names)
    if production_class == 4:
        EnginePattern.objects.filter(id=element_id).update(name=new_names)
    if production_class == 5:
        GeneratorPattern.objects.filter(id=element_id).update(name=new_names)
    if production_class == 6:
        WeaponPattern.objects.filter(id=element_id).update(name=new_names)
    if production_class == 7:
        ShellPattern.objects.filter(id=element_id).update(name=new_names)
    if production_class == 8:
        ModulePattern.objects.filter(id=element_id).update(name=new_names)
    if production_class == 9:
        DevicePattern.objects.filter(id=element_id).update(name=new_names)
    if production_class == 14:
        FuelPattern.objects.filter(id=element_id).update(name=new_names)
    message = 'Модуль переименован'
    return message
