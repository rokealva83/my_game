# -*- coding: utf-8 -*-

import random
from my_game.models import ArmorPattern
from my_game.models import BasicArmor
from my_game.knowledge.element_open import element_open
from my_game.knowledge.new_factory_pattern import new_factory_pattern
from my_game.knowledge.price_increase import price_increase


def armor_upgrade(request):
    user = request
    basic_armor = BasicArmor.objects.all()
    number_armor = len(basic_armor) - 1
    number_armor_scient = random.randint(0, number_armor)
    armor_scient = basic_armor[number_armor_scient]
    user_armor = ArmorPattern.objects.filter(user=user, basic_pattern=armor_scient).last()
    if not user_armor:
        koef = element_open(user, armor_scient)
        if koef < 0:
            koef = 0.00001
        upper_scope = 0.33 * koef
        new_armor = random.random()
        race = user.race
        if 0 < new_armor < upper_scope:
            armor_pattern = ArmorPattern(
                user=user,
                basic_pattern=armor_scient,
                element_name=armor_scient.element_name,
                armor_health=armor_scient.armor_health,
                value_energy_resistance=armor_scient.value_energy_resistance * race.armor,
                value_phisical_resistance=armor_scient.value_phisical_resistance * race.armor,
                armor_regeneration=armor_scient.armor_regeneration * race.armor,
                armor_power=armor_scient.armor_power,
                armor_mass=armor_scient.armor_mass,
                price_internal_currency=armor_scient.price_internal_currency,
                price_nickel=armor_scient.price_nickel,
                price_iron=armor_scient.price_iron,
                price_cooper=armor_scient.price_cooper,
                price_aluminum=armor_scient.price_aluminum,
                price_veriarit=armor_scient.price_veriarit,
                price_inneilit=armor_scient.price_inneilit,
                price_renniit=armor_scient.price_renniit,
                price_cobalt=armor_scient.price_cobalt,
                price_construction_material=armor_scient.price_construction_material,
                price_chemical=armor_scient.price_chemical,
                price_high_strength_allov=armor_scient.price_high_strength_allov,
                price_nanoelement=armor_scient.price_nanoelement,
                price_microprocessor_element=armor_scient.price_microprocessor_element,
                price_fober_optic_element=armor_scient.price_fober_optic_element
            )
            armor_pattern.save()
            new_factory_pattern(user, 2, armor_scient.id)
    else:
        studied_armor = ArmorPattern.objects.filter(user=user, basic_pattern=armor_scient, bought_template=0)
        len_studied_armor = len(studied_armor)
        if len_studied_armor < 3:
            user_armor = ArmorPattern.objects.filter(user=user, basic_pattern=armor_scient).last()
            armor_attribute = ['armor_health', 'value_energy_resistance', 'value_phisical_resistance',
                               'armor_regeneration', 'armor_power', 'armor_mass']
            trying = random.random()
            if 0.15 <= trying <= 0.3 or 0.7 <= trying <= 0.85:
                summary_percent_up = 0
                user_armor.pk = None
                user_armor.save()
                user_armor = ArmorPattern.objects.filter(user=user, basic_pattern=armor_scient).last()
                for attribute in armor_attribute:
                    percent_update = 1.0 + random.randint(5, 20) / 100.0
                    element = getattr(user_armor, attribute)
                    element_basic = getattr(armor_scient, attribute)
                    if element_basic / element > 4.0:
                        if attribute == 'armor_mass':
                            percent_update = 1 - random.randint(2, 5) / 100.0
                            element *= percent_update
                            setattr(user_armor, attribute, element)
                            user_armor.save()
                        else:
                            element *= percent_update
                            setattr(user_armor, attribute, element)
                            user_armor.save()
                    summary_percent_up += percent_update
                price_increase(user_armor, summary_percent_up)
