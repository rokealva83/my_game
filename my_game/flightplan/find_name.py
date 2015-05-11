# -*- coding: utf-8 -*-


from my_game.models import Hull_pattern, Armor_pattern, Shell_pattern, Shield_pattern, Weapon_pattern, Factory_pattern, \
    Engine_pattern, Generator_pattern, Module_pattern, Basic_resource, Fuel_pattern


def find_name(*args):
    class_element = args[0]
    id_element = args[1]
    name = ''
    if class_element == 0:
        resource = Basic_resource.objects.filter(id=id_element).first()
        name = resource.name

    elif class_element == 1:
        hull = Hull_pattern.objects.filter(id=id_element).first()
        name = hull.name

    elif class_element == 2:
        armor = Armor_pattern.objects.filter(id=id_element).first()
        name = armor.name

    elif class_element == 3:
        shield = Shield_pattern.objects.filter(id=id_element).first()
        name = shield.name

    elif class_element == 4:
        engine = Engine_pattern.objects.filter(id=id_element).first()
        name = engine.name

    elif class_element == 5:
        generator = Generator_pattern.objects.filter(id=id_element).first()
        name = generator.name

    elif class_element == 6:
        weapon = Weapon_pattern.objects.filter(id=id_element).first()
        name = weapon.name

    elif class_element == 7:
        shell = Shell_pattern.objects.filter(id=id_element).first()
        name = shell.name

    elif class_element == 8:
        module = Module_pattern.objects.filter(id=id_element).first()
        name = module.name

    elif class_element == 10:
        factory = Factory_pattern.objects.filter(id=id_element).first()
        name = factory.name

    elif class_element == 14:
        factory = Fuel_pattern.objects.filter(id=id_element).first()
        name = factory.name
    return name