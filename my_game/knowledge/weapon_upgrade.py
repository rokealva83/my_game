# -*- coding: utf-8 -*-

import random
from my_game.models import WeaponPattern
from my_game.models import BasicWeapon
from my_game.knowledge.element_open import element_open
from my_game.knowledge.new_factory_pattern import new_factory_pattern
from my_game.knowledge.price_increase import price_increase


def weapon_upgrade(request):
    user = request
    basic_weapon = BasicWeapon.objects.all()
    number_weapon = len(basic_weapon) - 1
    number_weapon_scient = random.randint(0, number_weapon)
    weapon_scient = basic_weapon[number_weapon_scient]
    user_weapon = WeaponPattern.objects.filter(user=user, basic_weapon=weapon_scient).last()
    if user_weapon is None:
        koef = element_open(user, weapon_scient)
        if koef < 0:
            koef = 0.00001
        upper_scope = 0.33 * koef
        new_weapon = random.random()
        race = user.race
        weapon_class = weapon_scient.weapon_class
        if weapon_class == 1:
            weapon = race.weapon_attack
        else:
            weapon = race.weapon_defense
        if 0 < new_weapon < upper_scope:
            weapon_pattern = WeaponPattern(
                user=user,
                basic_weapon=weapon_scient,
                weapon_name=weapon_scient.weapon_name,
                weapon_health=weapon_scient.weapon_health,
                weapon_energy_damage=weapon_scient.weapon_energy_damage * weapon,
                weapon_regenerations=weapon_scient.weapon_regenerations * weapon,
                number_of_bursts=weapon_scient.number_of_bursts * weapon,
                weapon_range=weapon_scient.weapon_range * weapon,
                weapon_accuracy=weapon_scient.weapon_accuracy * weapon,
                weapon_ass=weapon_scient.weapon_mass,
                weapon_size=weapon_scient.weapon_size,
                power_consuption=weapon_scient.power_consuption,
                weapon_class=weapon_scient.weapon_class,
                price_internal_currency=weapon_scient.price_internal_currency,
                price_resource1=weapon_scient.price_resource1,
                price_resource2=weapon_scient.price_resource2,
                price_resource3=weapon_scient.price_resource3,
                price_resource4=weapon_scient.price_resource4,
                price_mineral1=weapon_scient.price_mineral1,
                price_mineral2=weapon_scient.price_mineral2,
                price_mineral3=weapon_scient.price_mineral3,
                price_mineral4=weapon_scient.price_mineral4,
            )
            weapon_pattern.save()
            new_factory_pattern(user, 6, weapon_scient.id)
    else:
        studied_weapon = WeaponPattern.objects.filter(user=user, basic_weapon=weapon_scient, bought_template=0)
        len_studied_weapon = len(studied_weapon)
        if len_studied_weapon < 2:
            user_weapon = WeaponPattern.objects.filter(user=user, basic_weapon=weapon_scient).last()
            weapon_attribute = ['health', 'energy_damage', 'regenerations', 'number_of_bursts', 'range', 'accuracy',
                                'mass', 'size', 'power_consuption']
            trying = random.random()
            percent_update = 1 + random.randint(5, 10) / 100.0
            if 0.15 <= trying <= 0.3 or 0.7 <= trying <= 0.85:
                number = random.randint(0, 8)
                attribute = weapon_attribute[number]
                element = getattr(user_weapon, attribute)
                element_basic = getattr(weapon_scient, attribute)
                if element != 0:
                    if number == 6 or number == 7 or number == 8:
                        if element / element_basic > 0.7:
                            percent_update = 1 - random.randint(5, 10) / 100.0
                            element = element * percent_update
                            user_weapon.pk = None
                            user_weapon.save()
                            user_weapon = WeaponPattern.objects.filter(user=user, basic_weapon=weapon_scient).last()
                            setattr(user_weapon, attribute, element)
                            user_weapon.save()
                    else:
                        if number == 3 and element / element_basic < 2:
                            element = element + 1
                            user_weapon.pk = None
                            user_weapon.save()
                            user_weapon = WeaponPattern.objects.filter(user=user, basic_weapon=weapon_scient).last()
                            setattr(user_weapon, attribute, element)
                            user_weapon.save()
                        else:
                            if number == 5:
                                if element_basic / element > 0.75:
                                    element = element * percent_update
                                    user_weapon.pk = None
                                    user_weapon.save()
                                    user_weapon = WeaponPattern.objects.filter(user=user,
                                                                               basic_weapon=weapon_scient).last()
                                    setattr(user_weapon, attribute, element)
                                    user_weapon.save()
                            else:
                                if element_basic / element > 0.7:
                                    element = element * percent_update
                                    user_weapon.pk = None
                                    user_weapon.save()
                                    user_weapon = WeaponPattern.objects.filter(user=user,
                                                                               basic_weapon=weapon_scient).last()
                                    setattr(user_weapon, attribute, element)
                                    user_weapon.save()
                user_weapon = WeaponPattern.objects.filter(user=user, basic_weapon=weapon_scient).last()
                price_increase(user_weapon)
