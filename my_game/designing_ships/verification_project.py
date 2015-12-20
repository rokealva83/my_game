# -*- coding: utf-8 -*-

from my_game.models import ShieldPattern, GeneratorPattern, EnginePattern, ArmorPattern, ModulePattern, WeaponPattern


def verification(*args):
    chosen_hull = args[0]
    my_dictionary = args[1]

    choice_engine = my_dictionary.get('choice_engine')
    system_power = 0
    intersystem_power = 0
    if choice_engine:
        for i in range(chosen_hull.engine):
            engine = EnginePattern.objects.filter(id=choice_engine[i]).first()
            if engine:
                system_power = system_power + engine.system_power
                intersystem_power = intersystem_power + engine.intersystem_power
    if system_power == 0 or intersystem_power == 0:
        return False
    use_energy = 0
    use_energy = use_energy + chosen_hull.power_consuption

    choice_armor = my_dictionary.get('choice_armor')
    if choice_armor:
        for i in range(chosen_hull.armor):
            armor = ArmorPattern.objects.filter(id=choice_armor[i]).first()
            if armor:
                use_energy = use_energy + armor.armor_power

    choice_shield = my_dictionary.get('choice_shield')
    if choice_shield:
        for i in range(chosen_hull.shield):
            shield = ShieldPattern.objects.filter(id=choice_shield[i]).first()
            if shield:
                use_energy = use_energy + shield.power_consuption

    choice_engine = my_dictionary.get('choice_engine')
    if choice_engine:
        for i in range(chosen_hull.engine):
            engine = EnginePattern.objects.filter(id=choice_engine[i]).first()
            if engine:
                use_energy = use_energy + engine.power_consuption

    choice_weapon = my_dictionary.get('choice_weapon')
    if choice_weapon:
        for i in range(chosen_hull.main_weapon):
            weapon = WeaponPattern.objects.filter(id=choice_weapon[i]).first()
            if weapon:
                use_energy = use_energy + weapon.power_consuption

    choice_main_weapon = my_dictionary.get('choice_main_weapon')
    if choice_main_weapon:
        for i in range(chosen_hull.main_weapon):
            weapon = WeaponPattern.objects.filter(id=choice_weapon[i]).first()
            if weapon:
                use_energy = use_energy + weapon.power_consuption

    choice_module = my_dictionary.get('choice_module')
    if choice_module:
        for i in range(chosen_hull.module):
            module = ModulePattern.objects.filter(id=choice_module[i]).first()
            if module:
                use_energy = use_energy + module.power_consuption

    choice_generator = my_dictionary.get('choice_generator')
    produced_energy = 0
    if choice_generator:
        for i in range(chosen_hull.generator):
            generator = GeneratorPattern.objects.filter(id=choice_generator[i]).first()
            if generator:
                produced_energy = produced_energy + generator.produced_energy
            else:
                return False

    if produced_energy < use_energy:
        return False
    return True
