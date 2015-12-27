# -*- coding: utf-8 -*-

import random
from my_game.models import GeneratorPattern
from my_game.models import BasicGenerator
from my_game.knowledge.element_open import element_open
from my_game.knowledge.new_factory_pattern import new_factory_pattern
from my_game.knowledge.price_increase import price_increase
from my_game.knowledge.open_fuel import open_fuel


def generator_upgrade(request):
    user = request
    basic_generator = BasicGenerator.objects.all()
    number_generator = len(basic_generator) - 1
    number_generator_scient = random.randint(0, number_generator)
    generator_scient = basic_generator[number_generator_scient]
    user_generator = GeneratorPattern.objects.filter(user=user, basic_pattern=generator_scient).last()
    if user_generator is None:
        koef = element_open(user, generator_scient)
        if koef < 0:
            koef = 0.00001
        upper_scope = 0.33 * koef
        new_generator = random.random()
        race = user.race
        if 0 < new_generator < upper_scope:
            generator_pattern = GeneratorPattern(
                user=user,
                basic_pattern=generator_scient,
                element_name=generator_scient.generator_name,
                generator_health=generator_scient.generator_health,
                produced_energy=generator_scient.produced_energy * race.generator,
                fuel_necessary=generator_scient.fuel_necessary,
                generator_mass=generator_scient.generator_mass,
                generator_size=generator_scient.generator_size,
                price_internal_currency=generator_scient.price_internal_currency,
                price_nickel=generator_scient.price_nickel,
                price_iron=generator_scient.price_iron,
                price_cooper=generator_scient.price_cooper,
                price_aluminum=generator_scient.price_aluminum,
                price_veriarit=generator_scient.price_veriarit,
                price_inneilit=generator_scient.price_inneilit,
                price_renniit=generator_scient.price_renniit,
                price_cobalt=generator_scient.price_cobalt,
                price_construction_material=generator_scient.price_construction_material,
                price_chemical=generator_scient.price_chemical,
                price_high_strength_allov=generator_scient.price_high_strength_allov,
                price_nanoelement=generator_scient.price_nanoelement,
                price_microprocessor_element=generator_scient.price_microprocessor_element,
                price_fober_optic_element=generator_scient.price_fober_optic_element
            )
            generator_pattern.save()
            new_factory_pattern(user, 5, generator_scient.id)
            open_fuel(user, None, generator_scient)
    else:
        studied_generator = GeneratorPattern.objects.filter(user=user, basic_pattern=generator_scient,
                                                            bought_template=0)
        len_studied_generator = len(studied_generator)
        if len_studied_generator < 3:
            generator_attribute = ['generator_health', 'produced_energy', 'fuel_necessary', 'generator_mass',
                                   'generator_size']
            trying = random.random()
            if 0.15 <= trying <= 0.3 or 0.7 <= trying <= 0.85:
                summary_percent_up = 0
                user_generator.pk = None
                user_generator.save()
                user_generator = GeneratorPattern.objects.filter(user=user, basic_pattern=generator_scient).last()
                for attribute in generator_attribute:
                    percent_update = 1.0 + random.randint(5, 20) / 100.0
                    element = getattr(user_generator, attribute)
                    element_basic = getattr(generator_scient, attribute)
                    if element / element_basic < 4.0:
                        if attribute == 'fuel_necessary' or attribute == 'generator_mass' or attribute == 'generator_size':
                            percent_update = 1 - random.randint(2, 5) / 100.0
                            element *= percent_update
                            setattr(user_generator, attribute, element)
                        else:
                            element *= percent_update
                            setattr(user_generator, attribute, element)
                    summary_percent_up += percent_update
                user_generator.save()
                price_increase(user_generator, (summary_percent_up/len(generator_attribute)))
