# -*- coding: utf-8 -*-

import random
from my_game.models import GeneratorPattern
from my_game.models import BasicGenerator
from my_game.knowledge.element_open import element_open
from my_game.knowledge.new_factory_pattern import new_factory_pattern
from my_game.knowledge.price_increase import price_increase


def generator_upgrade(request):
    user = request
    basic_generator = BasicGenerator.objects.all()
    number_generator = len(basic_generator) - 1
    number_generator_scient = random.randint(0, number_generator)
    generator_scient = basic_generator[number_generator_scient]
    user_generator = GeneratorPattern.objects.filter(user=user, basic_generator=generator_scient).last()
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
                basic_generator=generator_scient,
                generator_name=generator_scient.generator_name,
                generator_health=generator_scient.generator_health,
                produced_energy=generator_scient.produced_energy * race.generator,
                fuel_necessary=generator_scient.fuel_necessary,
                generator_mass=generator_scient.generator_mass,
                generator_size=generator_scient.generator_size,
                price_internal_currency=generator_scient.price_internal_currency,
                price_resource1=generator_scient.price_resource1,
                price_resource2=generator_scient.price_resource2,
                price_resource3=generator_scient.price_resource3,
                price_resource4=generator_scient.price_resource4,
                price_mineral1=generator_scient.price_mineral1,
                price_mineral2=generator_scient.price_mineral2,
                price_mineral3=generator_scient.price_mineral3,
                price_mineral4=generator_scient.price_mineral4,
            )
            generator_pattern.save()
            new_factory_pattern(user, 5, generator_scient.id)
    else:
        studied_generator = GeneratorPattern.objects.filter(user=user, basic_generator=generator_scient,
                                                            bought_template=0)
        len_studied_generator = len(studied_generator)
        if len_studied_generator < 2:
            generator_attribute = ['generator_health', 'produced_energy', 'fuel_necessary', 'generator_mass',
                                   'generator_size']
            trying = random.random()
            percent_update = 1 + random.randint(5, 10) / 100.0
            if 0.15 <= trying <= 0.3 or 0.7 <= trying <= 0.85:
                number = random.randint(0, 4)
                attribute = generator_attribute[number]
                element = getattr(user_generator, attribute)
                element_basic = getattr(generator_scient, attribute)
                if element != 0:
                    if number == 2 or number == 3 or number == 4:
                        if element / element_basic > 0.7:
                            percent_update = 1 - random.randint(5, 10) / 100.0
                            element = element * percent_update
                            user_generator.pk = None
                            user_generator.save()
                            user_generator = GeneratorPattern.objects.filter(user=user,
                                                                             basic_generator=generator_scient).last()
                            setattr(user_generator, attribute, element)
                            user_generator.save()
                    else:
                        if element_basic / element > 0.7:
                            element = element * percent_update
                            user_generator.pk = None
                            user_generator.save()
                            user_generator = GeneratorPattern.objects.filter(user=user,
                                                                             basic_generator=generator_scient).last()
                            setattr(user_generator, attribute, element)
                            user_generator.save()

                user_generator = GeneratorPattern.objects.filter(user=user, basic_generator=generator_scient).last()
                price_increase(user_generator)
