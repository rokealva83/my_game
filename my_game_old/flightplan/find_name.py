# -*- coding: utf-8 -*-


from my_game.models import HullPattern, ArmorPattern, ShellPattern, ShieldPattern, WeaponPattern, FactoryPattern, \
    EnginePattern, GeneratorPattern, ModulePattern, BasicResource, FuelPattern


def find_name(*args):
    class_element = args[0]
    id_element = args[1]
    name = ''
    if class_element == 0:
        resource = BasicResource.objects.filter(id=id_element).first()
        name = resource.name

    elif class_element == 1:
        hull = HullPattern.objects.filter(id=id_element).first()
        name = hull.name

    elif class_element == 2:
        armor = ArmorPattern.objects.filter(id=id_element).first()
        name = armor.name

    elif class_element == 3:
        shield = ShieldPattern.objects.filter(id=id_element).first()
        name = shield.name

    elif class_element == 4:
        engine = EnginePattern.objects.filter(id=id_element).first()
        name = engine.name

    elif class_element == 5:
        generator = GeneratorPattern.objects.filter(id=id_element).first()
        name = generator.name

    elif class_element == 6:
        weapon = WeaponPattern.objects.filter(id=id_element).first()
        name = weapon.name

    elif class_element == 7:
        shell = ShellPattern.objects.filter(id=id_element).first()
        name = shell.name

    elif class_element == 8:
        module = ModulePattern.objects.filter(id=id_element).first()
        name = module.name

    elif class_element == 10:
        factory = FactoryPattern.objects.filter(id=id_element).first()
        name = factory.name

    elif class_element == 14:
        factory = FuelPattern.objects.filter(id=id_element).first()
        name = factory.name
    return name