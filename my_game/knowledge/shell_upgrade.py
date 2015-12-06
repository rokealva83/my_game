# -*- coding: utf-8 -*-

import random
from my_game.models import ShellPattern, WeaponPattern
from my_game.models import BasicShell
from my_game.knowledge.open_shell import open_shell
from my_game.knowledge.price_increase import price_increase


def shell_upgrade(request):
    user = request
    weapon_patterns = WeaponPattern.objects.filter(user=user, weapon_class__in=[3, 4]).all()
    if weapon_patterns:
        len_weapon_patterns = len(weapon_patterns) - 1
        number_weapon_pattern = random.randint(0, len_weapon_patterns)
        weapon_pattern = weapon_patterns[number_weapon_pattern]
        basic_shell = BasicShell.objects.filter(shell_class=weapon_pattern.shell_class).all()
        number_shell = len(basic_shell) - 1
        number_shell_scient = random.randint(0, number_shell)
        shell_scient = basic_shell[number_shell_scient]
        user_shell = ShellPattern.objects.filter(user=user, basic_pattern=shell_scient).last()
        if user_shell is None:
            open_shell(user, weapon_pattern, 2, shell_scient)
        else:
            studied_shell = ShellPattern.objects.filter(user=user, basic_pattern=shell_scient, bought_template=0)
            len_studied_shell = len(studied_shell)
            if len_studied_shell < 3:
                shell_attribute = ['shell_phisical_damage', 'shell_speed', 'shell_mass', 'shell_size']
                trying = random.random()
                if 0.15 <= trying <= 0.3 or 0.7 <= trying <= 0.85:
                    summary_percent_up = 0
                    user_shell.pk = None
                    user_shell.save()
                    user_shell = ShellPattern.objects.filter(user=user, basic_pattern=shell_scient).last()
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
