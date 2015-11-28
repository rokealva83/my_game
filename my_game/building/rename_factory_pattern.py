# -*- coding: utf-8 -*-

from my_game.models import FactoryPattern, BuildingPattern


# Переименовани шаблона фибрики
def rename_factory_pattern(*args):
    new_name = args[0]
    pattern_id = args[1]
    class_id = args[2]
    if class_id != 13:
        FactoryPattern.objects.filter(id=pattern_id).update(name=new_name)
    else:
        BuildingPattern.objects.filter(id=pattern_id).update(name=new_name)
    message = 'Шаблон переименован'
    return message
