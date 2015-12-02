# -*- coding: utf-8 -*-

import random
from my_game.models import ShellPattern
from my_game.models import BasicShell
from my_game.knowledge.element_open import element_open
from my_game.knowledge.new_factory_pattern import new_factory_pattern
from my_game.knowledge.price_increase import price_increase

def shell_upgrade(request):
    user = request
    basic_shell = BasicShell.objects.all()
    number_shell = len(basic_shell) - 1
    number_shell_scient = random.randint(0, number_shell)
    shell_scient = basic_shell[number_shell_scient]
    user_shell = ShellPattern.objects.filter(user=user, basic_shell=shell_scient).last()
    if user_shell is None:
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
                price_fober_optic_element=shell_scient.price_fober_optic_element
            )
            shell_pattern.save()
            new_factory_pattern(user, 7, shell_scient.id)
    else:
        studied_shell = ShellPattern.objects.filter(user=user, basic_shell=shell_scient, bought_template=0)
        len_studied_shell = len(studied_shell)
        if len_studied_shell < 3:
            shell_attribute = ['shell_phisical_damage', 'shell_speed', 'shell_mass', 'shell_size']
            trying = random.random()
            if 0.15 <= trying <= 0.3 or 0.7 <= trying <= 0.85:
                summary_percent_up = 0
                user_shell.pk = None
                user_shell.save()
                user_shell = ShellPattern.objects.filter(user=user, basic_shell=shell_scient).last()
                for attribute in shell_attribute:
                    percent_update = 1.0 + random.randint(5, 20) / 100.0
                    element = getattr(user_shell, attribute)
                    element_basic = getattr(shell_scient, attribute)
                    if element_basic / element > 4.0:
                        if attribute == 'shell_mass' or attribute == 'shell_size':
                            percent_update = 1 - random.randint(2, 5) / 100.0
                            element *= percent_update
                            setattr(user_shell, attribute, element)
                            user_shell.save()
                        else:
                            element *= percent_update
                            setattr(user_shell, attribute, element)
                            user_shell.save()
                    summary_percent_up += percent_update
                price_increase(user_shell)