# -*- coding: utf-8 -*-


from my_game.models import HullPattern, ArmorPattern, ShellPattern, ShieldPattern, WeaponPattern, FactoryPattern, \
    EnginePattern, GeneratorPattern, ModulePattern, BasicResource, FuelPattern, BasicMaterial


def find_name(*args):
    class_element = args[0]
    element_id = args[1]
    name = ''
    if class_element == 0:
        if element_id < 9:
            resource = BasicResource.objects.filter(id=element_id).first()
            name = resource.resource_name
        else:
            res_id = {'9': 1, '10': 2, '11': 3, '12': 4, '13': 5, '14': 6}
            element_id = res_id[str(element_id)]
            material = BasicMaterial.objects.filter(id=element_id).first()
            name = material.material_name

    elif class_element == 1:
        hull = HullPattern.objects.filter(id=element_id).first()
        name = hull.element_name

    elif class_element == 2:
        armor = ArmorPattern.objects.filter(id=element_id).first()
        name = armor.element_name

    elif class_element == 3:
        shield = ShieldPattern.objects.filter(id=element_id).first()
        name = shield.element_name

    elif class_element == 4:
        engine = EnginePattern.objects.filter(id=element_id).first()
        name = engine.element_name

    elif class_element == 5:
        generator = GeneratorPattern.objects.filter(id=element_id).first()
        name = generator.element_name

    elif class_element == 6:
        weapon = WeaponPattern.objects.filter(id=element_id).first()
        name = weapon.element_name

    elif class_element == 7:
        shell = ShellPattern.objects.filter(id=element_id).first()
        name = shell.element_name

    elif class_element == 8:
        module = ModulePattern.objects.filter(id=element_id).first()
        name = module.element_name

    elif class_element == 10:
        factory = FactoryPattern.objects.filter(id=element_id).first()
        name = factory.factory_name

    elif class_element == 14:
        fuel = FuelPattern.objects.filter(id=element_id).first()
        name = fuel.element_name
    return name
