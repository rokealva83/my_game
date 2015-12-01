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
                price_resource1=hull_scient.price_resource1,
                price_resource2=hull_scient.price_resource2,
                price_resource3=hull_scient.price_resource3,
                price_resource4=hull_scient.price_resource4,
                price_mineral1=hull_scient.price_mineral1,
                price_mineral2=hull_scient.price_mineral2,
                price_mineral3=hull_scient.price_mineral3,
                price_mineral4=hull_scient.price_mineral4,
            )
            hull_pattern.save()
            new_factory_pattern(user, 1, hull_scient.id)
    else:
        studied_hull = HullPattern.objects.filter(user=user, basic_hull=hull_scient, bought_template=0)
        len_studied_hull = len(studied_hull)
        if len_studied_hull < 2:
            user_hull = HullPattern.objects.filter(user=user, basic_hull=hull_scient).last()
            hull_attribute = ['hull_health', 'generator', 'engine', 'weapon', 'armor', 'shield', 'module',
                              'main_weapon',
                              'hold_size', 'hull_mass', 'hull_size', 'power_consuption']
            trying = random.random()
            if 0.15 <= trying <= 0.3 or 0.7 <= trying <= 0.85:
                number = random.randint(0, 11)
                attribute = hull_attribute[number]
                element = getattr(user_hull, attribute)
                element_basic = getattr(hull_scient, attribute)
                if user_hull.basic_hull.id == 1:
                    if number == 5 and element == 0:
                        element = 1
                    else:
                        if number == 9 or number == 11:
                            percent_update = 1 - random.randint(5, 10) / 100.0
                            if element / element_basic > 0.7:
                                element = element * percent_update
                                user_hull.pk = None
                                user_hull.save()
                                user_hull = HullPattern.objects.filter(user=user, basic_hull=hull_scient).last()
                                setattr(user_hull, attribute, element)
                                user_hull.save()
                        if number == 0 or number == 8 or number == 10:
                            percent_update = 1 + random.randint(5, 10) / 100.0
                            if element != 0 and element_basic / element > 0.7:
                                element = element * percent_update
                                user_hull.pk = None
                                user_hull.save()
                                user_hull = HullPattern.objects.filter(user=user, basic_hull=hull_scient).last()
                                setattr(user_hull, attribute, element)
                                user_hull.save()
                        else:
                            if element != 0 and element / element_basic < 2:
                                element = element + 1
                                user_hull.pk = None
                                user_hull.save()
                                user_hull = HullPattern.objects.filter(user=user, basic_hull=hull_scient).last()
                                setattr(user_hull, attribute, element)
                                user_hull.save()
                else:
                    if element != 0:
                        if number == 9 or number == 11:
                            percent_update = 1 - random.randint(5, 10) / 100.0
                            if element / element_basic > 0.7:
                                element = element * percent_update
                                user_hull.pk = None
                                user_hull.save()
                                user_hull = HullPattern.objects.filter(user=user, basic_hull=hull_scient).last()
                                setattr(user_hull, attribute, element)
                                user_hull.save()
                        else:
                            if number == 0 or number == 8 or number == 10:
                                percent_update = 1 + random.randint(5, 10) / 100.0
                                if element_basic / element > 0.7:
                                    element = element * percent_update
                                    user_hull.pk = None
                                    user_hull.save()
                                    user_hull = HullPattern.objects.filter(user=user, basic_hull=hull_scient).last()
                                    setattr(user_hull, attribute, element)
                                    user_hull.save()
                            else:
                                if element / element_basic < 2:
                                    element = element + 1
                                    user_hull.pk = None
                                    user_hull.save()
                                    user_hull = HullPattern.objects.filter(user=user, basic_hull=hull_scient).last()
                                    setattr(user_hull, attribute, element)
                                    user_hull.save()
                user_hull = HullPattern.objects.filter(user=user, basic_hull=hull_scient).last()
                price_increase(user_hull)
