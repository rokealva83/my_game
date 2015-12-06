# -*- coding: utf-8 -*-

import random
from my_game.models import ShellPattern
from my_game.models import BasicShell
from my_game.knowledge.element_open import element_open
from my_game.knowledge.new_factory_pattern import new_factory_pattern


def open_shell(*args):
    user = args[0]
    weapon_pattern = args[1]
    open_upgrade = args[2]
    if open_upgrade == 1:
        basic_shell = BasicShell.objects.filter(shell_class=weapon_pattern.shell_class).all()
        number_shell = len(basic_shell) - 1
        number_shell_scient = random.randint(0, number_shell)
        shell_scient = basic_shell[number_shell_scient]
        new_shell = 0.5
        upper_scope = 1
    else:
        shell_scient = args[3]
        koef = element_open(user, shell_scient)
        if koef < 0:
            koef = 0.00001
        upper_scope = 0.33 * koef
        new_shell = random.random()

    if 0 < new_shell < upper_scope:
        shell_pattern = ShellPattern(
            user=user,
            basic_shell=shell_scient,
            shell_name=shell_scient.shell_name,
            shell_phisical_damage=shell_scient.shell_phisical_damage,
            shell_speed=shell_scient.shell_speed,
            shell_mass=shell_scient.shell_mass,
            shell_size=shell_scient.shell_size,
            price_internal_currency=shell_scient.price_internal_currency,
            price_nickel=shell_scient.price_nickel,
            price_iron=shell_scient.price_iron,
            price_cooper=shell_scient.price_cooper,
            price_aluminum=shell_scient.price_aluminum,
            price_veriarit=shell_scient.price_veriarit,
            price_inneilit=shell_scient.price_inneilit,
            price_renniit=shell_scient.price_renniit,
            price_cobalt=shell_scient.price_cobalt,
            price_construction_material=shell_scient.price_construction_material,
            price_chemical=shell_scient.price_chemical,
            price_high_strength_allov=shell_scient.price_high_strength_allov,
            price_nanoelement=shell_scient.price_nanoelement,
            price_microprocessor_element=shell_scient.price_microprocessor_element,
            price_fober_optic_element=shell_scient.price_fober_optic_element,
            shell_class=shell_scient.shell_class
        )
        shell_pattern.save()
        new_factory_pattern(user, 7, shell_scient.id)
