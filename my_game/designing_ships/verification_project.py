# -*- coding: utf-8 -*-

from my_game.models import Hull_pattern, Shield_pattern, Generator_pattern, Engine_pattern, \
    Armor_pattern, Module_pattern, Weapon_pattern


def verification(*args):
    session_user = args[0]
    session_user_city = args[1]
    chosen_hull = args[2]
    chosen_hull_id = args[3]
    myDict = args[4]

    choice_engine = myDict.get('choice_engine')
    system_power = 0
    intersystem_power = 0
    if choice_engine:
        for i in range(chosen_hull.engine):
            engine = Engine_pattern.objects.filter(id=choice_engine[i]).first()
            system_power = system_power + engine.system_power
            intersystem_power = intersystem_power + engine.intersystem_power
    if system_power == 0 or intersystem_power == 0:
        return (False)

    use_energy = 0
    hull = Hull_pattern.objects.filter(user=session_user, id=chosen_hull_id).first()
    use_energy = use_energy + hull.power_consuption

    choice_armor = myDict.get('choice_armor')
    if choice_armor:
        for i in range(chosen_hull.armor):
            if int(choice_armor[i]) != 0:
                armor = Armor_pattern.objects.filter(id=choice_armor[i]).first()
                use_energy = use_energy + armor.power

    choice_shield = myDict.get('choice_shield')
    if choice_shield:
        for i in range(chosen_hull.shield):
            if int(choice_shield[i]) != 0:
                shield = Shield_pattern.objects.filter(id=choice_shield[i]).first()
                use_energy = use_energy + shield.power_consuption

    choice_engine = myDict.get('choice_engine')
    if choice_engine:
        for i in range(chosen_hull.engine):
            if int(choice_engine[i]) != 0:
                engine = Engine_pattern.objects.filter(id=choice_engine[i]).first()
                use_energy = use_energy + engine.power_consuption

    choice_weapon = myDict.get('choice_weapon')
    if choice_weapon:
        for i in range(chosen_hull.main_weapon):
            if int(choice_weapon[i]) != 0:
                weapon = Weapon_pattern.objects.filter(id=choice_weapon[i]).first()
                use_energy = use_energy + weapon.power_consuption

    choice_main_weapon = myDict.get('choice_main_weapon')
    if choice_main_weapon:
        for i in range(chosen_hull.main_weapon):
            if int(choice_main_weapon[i]) != 0:
                weapon = Weapon_pattern.objects.filter(id=choice_weapon[i]).first()
                use_energy = use_energy + weapon.power_consuption

    choice_module = myDict.get('choice_module')
    if choice_module:
        for i in range(chosen_hull.module):
            if int(choice_module[i]) != 0:
                module = Module_pattern.objects.filter(id=choice_module[i]).first()
                use_energy = use_energy + module.power_consuption

    choice_generator = myDict.get('choice_generator')
    produced_energy = 0
    if choice_generator:
        for i in range(chosen_hull.generator):
            if int(choice_generator[i]) != 0:
                generator = Generator_pattern.objects.filter(id=choice_generator[i]).first()
                produced_energy = produced_energy + generator.produced_energy

    if produced_energy < use_energy:
        return False
    return True