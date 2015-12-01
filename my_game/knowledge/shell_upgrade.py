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
                price_resource1=shell_scient.price_resource1,
                price_resource2=shell_scient.price_resource2,
                price_resource3=shell_scient.price_resource3,
                price_resource4=shell_scient.price_resource4,
                price_mineral1=shell_scient.price_mineral1,
                price_mineral2=shell_scient.price_mineral2,
                price_mineral3=shell_scient.price_mineral3,
                price_mineral4=shell_scient.price_mineral4,
            )
            shell_pattern.save()
            new_factory_pattern(user, 7, shell_scient.id)
    else:
        studied_shell = ShellPattern.objects.filter(user=user, basic_shell=shell_scient, bought_template=0)
        len_studied_shell = len(studied_shell)
        if len_studied_shell < 2:
            shell_attribute = ['shell_phisical_damage', 'shell_speed', 'shell_mass', 'shell_size']
            trying = random.random()
            percent_update = 1 + random.randint(5, 10) / 100.0
            if 0.15 <= trying <= 0.3 or 0.7 <= trying <= 0.85:
                number = random.randint(0, 3)
                attribute = shell_attribute[number]
                element = getattr(user_shell, attribute)
                element_basic = getattr(shell_scient, attribute)
                if element != 0:
                    if number == 2 or number == 3:
                        if element / element_basic > 0.7:
                            percent_update = 1 - random.randint(5, 10) / 100.0
                            element = element * percent_update
                            user_shell.pk = None
                            user_shell.save()
                            user_shell = ShellPattern.objects.filter(user=user, basic_shell=shell_scient).last()
                            setattr(user_shell, attribute, element)
                            user_shell.save()
                    else:
                        if element_basic / element > 0.7:
                            element = element * percent_update
                            user_shell.pk = None
                            user_shell.save()
                            user_shell = ShellPattern.objects.filter(user=user, basic_shell=shell_scient).last()
                            setattr(user_shell, attribute, element)
                            user_shell.save()
                user_shell = ShellPattern.objects.filter(user=user, basic_shell=shell_scient).last()
                price_increase(user_shell)