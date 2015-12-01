# -*- coding: utf-8 -*-

import random
from my_game.models import ModulePattern
from my_game.models import BasicModule
from my_game.knowledge.element_open import element_open
from my_game.knowledge.new_factory_pattern import new_factory_pattern
from my_game.knowledge.price_increase import price_increase


def module_upgrade(request):
    user = request
    basic_module = BasicModule.objects.all()
    number_module = len(basic_module) - 1
    number_module_scient = random.randint(0, number_module)
    module_scient = basic_module[number_module_scient]
    user_module = ModulePattern.objects.filter(user=user, basic_module=module_scient).last()
    if user_module is None:
        koef = element_open(user, module_scient)
        if koef < 0:
            koef = 0.00001
        upper_scope = 0.33 * koef
        new_module = random.random()
        race = user.race
        module_class = module_scient.module_class
        if module_class == 1:
            module = race.exploration
        else:
            if module_class == 2:
                module = race.disguse
            else:
                module = race.auximilary
        if 0 < new_module < upper_scope:
            module_pattern = ModulePattern(
                user=user,
                basic_module=module_scient,
                module_name=module_scient.module_name,
                module_health=module_scient.module_health,
                param1=module_scient.param1 * module,
                param2=module_scient.param2 * module,
                param3=module_scient.param3 * module,
                module_mass=module_scient.module_mass,
                module_size=module_scient.module_size,
                power_consuption=module_scient.power_consuption,
                module_class=module_scient.module_class,
                price_internal_currency=module_scient.price_internal_currency,
                price_resource1=module_scient.price_resource1,
                price_resource2=module_scient.price_resource2,
                price_resource3=module_scient.price_resource3,
                price_resource4=module_scient.price_resource4,
                price_mineral1=module_scient.price_mineral1,
                price_mineral2=module_scient.price_mineral2,
                price_mineral3=module_scient.price_mineral3,
                price_mineral4=module_scient.price_mineral4,
            )
            module_pattern.save()
            new_factory_pattern(user, 8, module_scient.id)
    else:
        studied_module = ModulePattern.objects.filter(user=user, basic_module=module_scient, bought_template=0)
        len_studied_module = len(studied_module)
        if len_studied_module < 2:
            module_attribute = ['module_health', 'param1', 'param2', 'param3', 'module_mass', 'module_size',
                                'power_consuption']
            trying = random.random()
            percent_update = 1 + random.randint(5, 10) / 100.0
            if 0.15 <= trying <= 0.3 or 0.7 <= trying <= 0.85:
                number = random.randint(0, 6)
                attribute = module_attribute[number]
                element = getattr(user_module, attribute)
                element_basic = getattr(module_scient, attribute)
                if element != 0:
                    if number == 4 or number == 5 or number == 6:
                        if element / element_basic > 0.7:
                            percent_update = 1 - random.randint(5, 10) / 100.0
                            element = element * percent_update
                            user_module.pk = None
                            user_module.save()
                            user_module = ModulePattern.objects.filter(user=user, basic_module=module_scient).last()
                            setattr(user_module, attribute, element)
                            user_module.save()
                    else:
                        if element_basic / element > 0.7:
                            element = element * percent_update
                            user_module.pk = None
                            user_module.save()
                            user_module = ModulePattern.objects.filter(user=user, basic_module=module_scient).last()
                            setattr(user_module, attribute, element)
                            user_module.save()
                user_module = ModulePattern.objects.filter(user=user, basic_module=module_scient).last()
                price_increase(user_module)
