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
                price_nickel=module_scient.price_nickel,
                price_iron=module_scient.price_iron,
                price_cooper=module_scient.price_cooper,
                price_aluminum=module_scient.price_aluminum,
                price_veriarit=module_scient.price_veriarit,
                price_inneilit=module_scient.price_inneilit,
                price_renniit=module_scient.price_renniit,
                price_cobalt=module_scient.price_cobalt,
                price_construction_material=module_scient.price_construction_material,
                price_chemical=module_scient.price_chemical,
                price_high_strength_allov=module_scient.price_high_strength_allov,
                price_nanoelement=module_scient.price_nanoelement,
                price_microprocessor_element=module_scient.price_microprocessor_element,
                price_fober_optic_element=module_scient.price_fober_optic_element
            )
            module_pattern.save()
            new_factory_pattern(user, 8, module_scient.id)
    else:
        studied_module = ModulePattern.objects.filter(user=user, basic_module=module_scient, bought_template=0)
        len_studied_module = len(studied_module)
        if len_studied_module < 3:
            module_attribute = ['module_health', 'param1', 'param2', 'param3', 'module_mass', 'module_size',
                                'power_consuption']
            trying = random.random()
            if 0.15 <= trying <= 0.3 or 0.7 <= trying <= 0.85:
                summary_percent_up = 0
                user_module.pk = None
                user_module.save()
                user_module = ModulePattern.objects.filter(user=user, basic_module=module_scient).last()
                for attribute in module_attribute:
                    percent_update = 1.0 + random.randint(5, 20) / 100.0
                    element = getattr(user_module, attribute)
                    element_basic = getattr(module_scient, attribute)
                    if element_basic / element > 4.0:
                        if attribute == 'module_mass' or attribute == 'module_size' or attribute == 'power_consuption':
                            percent_update = 1 - random.randint(2, 5) / 100.0
                            element *= percent_update
                            setattr(user_module, attribute, element)
                            user_module.save()
                        else:
                            element *= percent_update
                            setattr(user_module, attribute, element)
                            user_module.save()
                    summary_percent_up += percent_update
                price_increase(user_module, summary_percent_up)
