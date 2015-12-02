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
                weapon_mass=weapon_scient.weapon_mass,
                weapon_size=weapon_scient.weapon_size,
                power_consuption=weapon_scient.power_consuption,
                weapon_class=weapon_scient.weapon_class,
                price_internal_currency=weapon_scient.price_internal_currency,
                price_nickel=weapon_scient.price_nickel,
                price_iron=weapon_scient.price_iron,
                price_cooper=weapon_scient.price_cooper,
                price_aluminum=weapon_scient.price_aluminum,
                price_veriarit=weapon_scient.price_veriarit,
                price_inneilit=weapon_scient.price_inneilit,
                price_renniit=weapon_scient.price_renniit,
                price_cobalt=weapon_scient.price_cobalt,
                price_construction_material=weapon_scient.price_construction_material,
                price_chemical=weapon_scient.price_chemical,
                price_high_strength_allov=weapon_scient.price_high_strength_allov,
                price_nanoelement=weapon_scient.price_nanoelement,
                price_microprocessor_element=weapon_scient.price_microprocessor_element,
                price_fober_optic_element=weapon_scient.price_fober_optic_element
            )
            weapon_pattern.save()
            new_factory_pattern(user, 6, weapon_scient.id)
    else:
        studied_weapon = WeaponPattern.objects.filter(user=user, basic_weapon=weapon_scient, bought_template=0)
        len_studied_weapon = len(studied_weapon)
        if len_studied_weapon < 3:
            user_weapon = WeaponPattern.objects.filter(user=user, basic_weapon=weapon_scient).last()
            weapon_attribute = ['weapon_health', 'weapon_energy_damage', 'weapon_regenerations', 'number_of_bursts',
                                'weapon_range', 'weapon_accuracy', 'weapon_mass', 'weapon_size', 'power_consuption']
            trying = random.random()
            if 0.15 <= trying <= 0.3 or 0.7 <= trying <= 0.85:
                summary_percent_up = 0
                user_weapon.pk = None
                user_weapon.save()
                user_weapon = WeaponPattern.objects.filter(user=user, basic_armor=weapon_scient).last()
                for attribute in weapon_attribute:
                    percent_update = 1.0 + random.randint(5, 20) / 100.0
                    element = getattr(user_weapon, attribute)
                    element_basic = getattr(weapon_scient, attribute)
                    if element_basic / element > 4.0:
                        if attribute == 'weapon_mass' or attribute == 'weapon_size' or attribute == 'power_consuption':
                            percent_update = 1 - random.randint(2, 5) / 100.0
                            element *= percent_update
                            setattr(user_weapon, attribute, element)
                            user_weapon.save()
                        elif attribute == 'number_of_bursts' and element / element_basic < 2:
                            element += 1
                            setattr(user_weapon, attribute, element)
                            user_weapon.save()
                        elif attribute == 'weapon_accuracy':
                            if element_basic / element > 0.75:
                                element *= percent_update
                                setattr(user_weapon, attribute, element)
                                user_weapon.save()
                        else:
                            element *= percent_update
                            setattr(user_weapon, attribute, element)
                            user_weapon.save()
                    summary_percent_up += percent_update
                price_increase(user_weapon)
