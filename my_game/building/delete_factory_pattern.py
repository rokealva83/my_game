# -*- coding: utf-8 -*-

from my_game.models import FactoryPattern, FactoryInstalled, BuildingPattern


# Удаление шаблона
def delete_factory_pattern(*args):
    pattern_id = int(args[0])
    class_id = int(args[1])
    factory_pattern = FactoryPattern.objects.filter(id=pattern_id).first()
    factory = FactoryInstalled.objects.filter(factory_pattern=factory_pattern).first()
    if factory is not None:
        message = 'Шаблон не может быть удален'
    else:
        if class_id != 13:
            FactoryPattern.objects.filter(id=pattern_id).delete()
        else:
            BuildingPattern.objects.filter(id=pattern_id).delete()
        message = 'Шаблон удален'
    return message
