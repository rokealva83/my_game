# -*- coding: utf-8 -*-

import random
from my_game.models import EnginePattern
from my_game.models import BasicEngine
from my_game.knowledge.element_open import element_open
from my_game.knowledge.new_factory_pattern import new_factory_pattern
from my_game.knowledge.price_increase import price_increase
from my_game.knowledge.open_fuel import open_fuel


def engine_upgrade(request):
    user = request
    basic_engine = BasicEngine.objects.all()
    number_engine = len(basic_engine) - 1
    number_engine_scient = random.randint(0, number_engine)
    engine_scient = basic_engine[number_engine_scient]
    user_engine = EnginePattern.objects.filter(user=user, basic_engine=engine_scient).last()
    if user_engine is None:
        koef = element_open(user, engine_scient)
        if koef < 0:
            koef = 0.00001
        upper_scope = 0.33 * koef
        new_engine = random.random()
        race = user.race
        if 0 < new_engine < upper_scope:
            engine_pattern = EnginePattern(
                user=user,
                basic_engine=engine_scient,
                engine_name=engine_scient.engine_name,
                engine_health=engine_scient.engine_health,
                system_power=engine_scient.system_power * race.engine_system,
                intersystem_power=engine_scient.intersystem_power * race.engine_intersystem,
                giper_power=engine_scient.giper_power * race.engine_giper,
                nullT_power=engine_scient.nullT_power * race.engine_null,
                engine_mass=engine_scient.engine_mass,
                engine_size=engine_scient.engine_size,
                power_consuption=engine_scient.power_consuption,
                price_internal_currency=engine_scient.price_internal_currency,
                price_resource1=engine_scient.price_resource1,
                price_resource2=engine_scient.price_resource2,
                price_resource3=engine_scient.price_resource3,
                price_resource4=engine_scient.price_resource4,
                price_mineral1=engine_scient.price_mineral1,
                price_mineral2=engine_scient.price_mineral2,
                price_mineral3=engine_scient.price_mineral3,
                price_mineral4=engine_scient.price_mineral4,
            )
            engine_pattern.save()
            new_factory_pattern(user, 4, engine_scient.id)
            if engine_pattern.system_power != 0 or engine_pattern.intersystem_power != 0:
                open_fuel(user, engine_pattern.system_power, engine_pattern.intersystem_power)
    else:
        studied_engine = EnginePattern.objects.filter(user=user, basic_engine=engine_scient, bought_template=0)
        len_studied_engine = len(studied_engine)
        if len_studied_engine < 2:
            user_engine = EnginePattern.objects.filter(user=user, basic_engine=engine_scient).last()
            engine_attribute = ['engine_health', 'system_power', 'intersystem_power', 'giper_power', 'nullT_power',
                                'engine_mass', 'engine_size', 'power_consuption']
            trying = random.random()
            percent_update = 1 + random.randint(5, 10) / 100.0
            if 0.15 <= trying <= 0.3 or 0.7 <= trying <= 0.85:
                number = random.randint(1, 7)
                attribute = engine_attribute[number]
                element = getattr(user_engine, attribute)
                element_basic = getattr(engine_scient, attribute)
                if element != 0:
                    if number == 5 or number == 6 or number == 7:
                        if element / element_basic > 0.7:
                            percent_update = 1 - random.randint(5, 10) / 100.0
                            element = element * percent_update
                            user_engine.pk = None
                            user_engine.save()
                            user_engine = EnginePattern.objects.filter(user=user, basic_engine=engine_scient).last()
                            setattr(user_engine, attribute, element)
                            user_engine.save()
                    else:
                        if element_basic / element > 0.7:
                            element = element * percent_update
                            user_engine.pk = None
                            user_engine.save()
                            user_engine = EnginePattern.objects.filter(user=user, basic_engine=engine_scient).last()
                            setattr(user_engine, attribute, element)
                            user_engine.save()
                user_engine = EnginePattern.objects.filter(user=user, basic_engine=engine_scient).last()
                price_increase(user_engine)
