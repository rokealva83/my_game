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
    user_engine = EnginePattern.objects.filter(user=user, basic_pattern=engine_scient).last()
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
                basic_pattern=engine_scient,
                element_name=engine_scient.engine_name,
                engine_health=engine_scient.engine_health,
                system_power=engine_scient.system_power * race.engine_system,
                intersystem_power=engine_scient.intersystem_power * race.engine_intersystem,
                giper_power=engine_scient.giper_power * race.engine_giper,
                nullT_power=engine_scient.nullT_power * race.engine_null,
                engine_mass=engine_scient.engine_mass,
                engine_size=engine_scient.engine_size,
                power_consuption=engine_scient.power_consuption,
                price_internal_currency=engine_scient.price_internal_currency,
                price_nickel=engine_scient.price_nickel,
                price_iron=engine_scient.price_iron,
                price_cooper=engine_scient.price_cooper,
                price_aluminum=engine_scient.price_aluminum,
                price_veriarit=engine_scient.price_veriarit,
                price_inneilit=engine_scient.price_inneilit,
                price_renniit=engine_scient.price_renniit,
                price_cobalt=engine_scient.price_cobalt,
                price_construction_material=engine_scient.price_construction_material,
                price_chemical=engine_scient.price_chemical,
                price_high_strength_allov=engine_scient.price_high_strength_allov,
                price_nanoelement=engine_scient.price_nanoelement,
                price_microprocessor_element=engine_scient.price_microprocessor_element,
                price_fober_optic_element=engine_scient.price_fober_optic_element
            )
            engine_pattern.save()
            new_factory_pattern(user, 4, engine_scient.id)
            open_fuel(user, engine_scient, None)
    else:
        studied_engine = EnginePattern.objects.filter(user=user, basic_pattern=engine_scient, bought_template=0)
        len_studied_engine = len(studied_engine)
        if len_studied_engine < 3:
            user_engine = EnginePattern.objects.filter(user=user, basic_pattern=engine_scient).last()
            engine_attribute = ['engine_health', 'system_power', 'intersystem_power', 'giper_power', 'nullT_power',
                                'engine_mass', 'engine_size', 'power_consuption']
            trying = random.random()
            if 0.15 <= trying <= 0.3 or 0.7 <= trying <= 0.85:
                summary_percent_up = 0
                user_engine.pk = None
                user_engine.save()
                user_engine = EnginePattern.objects.filter(user=user, basic_pattern=engine_scient).last()
                for attribute in engine_attribute:
                    percent_update = 1.0 + random.randint(5, 20) / 100.0
                    element = getattr(user_engine, attribute)
                    element_basic = getattr(engine_scient, attribute)
                    if element_basic != 0:
                        if element / element_basic < 4.0:
                            if attribute == 'engine_mass' or attribute == 'engine_size' or (
                                        attribute == 'power_consuption'):
                                percent_update = 1 - random.randint(2, 5) / 100.0
                                element *= percent_update
                                setattr(user_engine, attribute, element)
                            else:
                                element *= percent_update
                                setattr(user_engine, attribute, element)
                        summary_percent_up += percent_update
                user_engine.save()
                price_increase(user_engine, (summary_percent_up / len(engine_attribute)))
