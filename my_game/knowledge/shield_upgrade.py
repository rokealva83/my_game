# -*- coding: utf-8 -*-

import random
from my_game.models import ShieldPattern
from my_game.models import BasicShield
from my_game.knowledge.element_open import element_open
from my_game.knowledge.new_factory_pattern import new_factory_pattern
from my_game.knowledge.price_increase import price_increase


def shield_upgrade(request):
    user = request
    basic_shield = BasicShield.objects.all()
    number_shield = len(basic_shield) - 1
    number_shield_scient = random.randint(0, number_shield)
    shield_scient = basic_shield[number_shield_scient]
    user_shield = ShieldPattern.objects.filter(user=user, basic_shield=shield_scient).last()
    if user_shield is None:
        koef = element_open(user, shield_scient)
        if koef < 0:
            koef = 0.00001
        upper_scope = 0.33 * koef
        new_shield = random.random()
        race = user.race
        if 0 < new_shield < upper_scope:
            shield_pattern = ShieldPattern(
                user=user,
                basic_shield=shield_scient,
                element_name=shield_scient.element_name,
                shield_health=shield_scient.shield_health,
                value_energy_resistance=shield_scient.value_energy_resistance * race.shield,
                value_phisical_resistance=shield_scient.value_phisical_resistance * race.shield,
                shield_regeneration=shield_scient.shield_regeneration * race.shield,
                number_of_emitter=shield_scient.number_of_emitter,
                shield_mass=shield_scient.shield_mass,
                shield_size=shield_scient.shield_size,
                power_consuption=shield_scient.power_consuption,
                price_internal_currency=shield_scient.price_internal_currency,
                price_nickel=shield_scient.price_nickel,
                price_iron=shield_scient.price_iron,
                price_cooper=shield_scient.price_cooper,
                price_aluminum=shield_scient.price_aluminum,
                price_veriarit=shield_scient.price_veriarit,
                price_inneilit=shield_scient.price_inneilit,
                price_renniit=shield_scient.price_renniit,
                price_cobalt=shield_scient.price_cobalt,
                price_construction_material=shield_scient.price_construction_material,
                price_chemical=shield_scient.price_chemical,
                price_high_strength_allov=shield_scient.price_high_strength_allov,
                price_nanoelement=shield_scient.price_nanoelement,
                price_microprocessor_element=shield_scient.price_microprocessor_element,
                price_fober_optic_element=shield_scient.price_fober_optic_element
            )
            shield_pattern.save()
            new_factory_pattern(user, 3, shield_scient.id)
    else:
        studied_shield = ShieldPattern.objects.filter(user=user, basic_shield=shield_scient, bought_template=0)
        len_studied_shield = len(studied_shield)
        if len_studied_shield < 3:
            shield_attribute = ['shield_health', 'value_energy_resistance', 'value_phisical_resistance',
                                'shield_regeneration', 'number_of_emitter', 'shield_mass', 'shield_size',
                                'power_consuption']
            trying = random.random()
            if 0.15 <= trying <= 0.3 or 0.7 <= trying <= 0.85:
                summary_percent_up = 0
                user_shield.pk = None
                user_shield.save()
                user_shield = ShieldPattern.objects.filter(user=user, basic_shield=shield_scient).last()
                for attribute in shield_attribute:
                    percent_update = 1.0 + random.randint(5, 20) / 100.0
                    element = getattr(user_shield, attribute)
                    element_basic = getattr(shield_scient, attribute)
                    if attribute == 'shield_mass' or attribute == 'shield_size' or attribute == 'power_consuption':
                        percent_update = 1.0 - random.randint(2, 5) / 100.0
                        element *= percent_update
                        setattr(user_shield, attribute, element)
                        user_shield.save()
                    elif attribute == 'number_of_emitter' and element_basic / element > 0.5:
                        element += 1
                        setattr(user_shield, attribute, element)
                        user_shield.save()
                    else:
                        element *= percent_update
                        setattr(user_shield, attribute, element)
                        user_shield.save()
                summary_percent_up += percent_update
            price_increase(user_shield)
