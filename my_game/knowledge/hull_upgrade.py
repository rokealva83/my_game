# -*- coding: utf-8 -*-

import random
from my_game.models import HullPattern
from my_game.models import BasicHull
from my_game.knowledge.element_open import element_open
from my_game.knowledge.new_factory_pattern import new_factory_pattern
from my_game.knowledge.price_increase import price_increase


def hull_upgrade(request):
    user = request
    basic_hull = BasicHull.objects.all()
    number_hull = len(basic_hull) - 1
    number_hull_scient = random.randint(0, number_hull)
    hull_scient = basic_hull[number_hull_scient]
    user_hull = HullPattern.objects.filter(user=user, basic_hull=hull_scient).last()
    if user_hull is None:
        koef = element_open(user, hull_scient)
        if koef < 0:
            koef = 0.00001
        upper_scope = 0.33 * koef
        new_hull = random.random()
        if 0 < new_hull < upper_scope:
            hull_pattern = HullPattern(
                user=user,
                basic_hull=hull_scient,
                hull_name=hull_scient.hull_name,
                hull_health=hull_scient.hull_health,
                generator=hull_scient.generator,
                engine=hull_scient.engine,
                weapon=hull_scient.weapon,
                armor=hull_scient.armor,
                shield=hull_scient.shield,
                module=hull_scient.module,
                main_weapon=hull_scient.main_weapon,
                hold_size=hull_scient.hold_size,
                hull_mass=hull_scient.hull_mass,
                hull_size=hull_scient.hull_size,
                fuel_tank=hull_scient.fuel_tank,
                power_consuption=hull_scient.power_consuption,
                price_internal_currency=hull_scient.price_internal_currency,
                price_nickel=hull_scient.price_nickel,
                price_iron=hull_scient.price_iron,
                price_cooper=hull_scient.price_cooper,
                price_aluminum=hull_scient.price_aluminum,
                price_veriarit=hull_scient.price_veriarit,
                price_inneilit=hull_scient.price_inneilit,
                price_renniit=hull_scient.price_renniit,
                price_cobalt=hull_scient.price_cobalt,
                price_construction_material=hull_scient.price_construction_material,
                price_chemical=hull_scient.price_chemical,
                price_high_strength_allov=hull_scient.price_high_strength_allov,
                price_nanoelement=hull_scient.price_nanoelement,
                price_microprocessor_element=hull_scient.price_microprocessor_element,
                price_fober_optic_element=hull_scient.price_fober_optic_element
            )
            hull_pattern.save()
            new_factory_pattern(user, 1, hull_scient.id)
    else:
        studied_hull = HullPattern.objects.filter(user=user, basic_hull=hull_scient, bought_template=0)
        len_studied_hull = len(studied_hull)
        if len_studied_hull < 2:
            user_hull = HullPattern.objects.filter(user=user, basic_hull=hull_scient).last()
            hull_attribute = ['hull_health', 'generator', 'engine', 'weapon', 'armor', 'shield', 'module',
                              'main_weapon', 'hold_size', 'hull_mass', 'hull_size', 'power_consuption']
            trying = random.random()
            if 0.15 <= trying <= 0.3 or 0.7 <= trying <= 0.85:
                summary_percent_up = 0
                user_hull.pk = None
                user_hull.save()
                user_hull = HullPattern.objects.filter(user=user, basic_hull=hull_scient).last()
                for attribute in hull_attribute:
                    element = getattr(user_hull, attribute)
                    element_basic = getattr(hull_scient, attribute)
                    percent_update = 1 + random.randint(5, 20) / 100.0
                    if element_basic / element > 4:
                        if attribute == 'hull_health' and element_basic / element > 2.5:
                            element *= percent_update
                            setattr(user_hull, attribute, element)
                            user_hull.save()
                        elif attribute == 'hull_mass' or attribute == 'power_consuption':
                            percent_update = 1 - random.randint(2, 4) / 100.0
                            element *= percent_update
                            setattr(user_hull, attribute, element)
                            user_hull.save()
                        elif attribute == 'hold_size' or attribute == 'hull_size':
                            percent_update = 1 + random.randint(3, 10) / 100.0
                            element *= percent_update
                            setattr(user_hull, attribute, element)
                            user_hull.save()
                        else:
                            element += 1
                            setattr(user_hull, attribute, element)
                            user_hull.save()
                    summary_percent_up += percent_update
                price_increase(user_hull)
