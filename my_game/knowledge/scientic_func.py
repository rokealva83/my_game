# -*- coding: utf-8 -*-

import random
from my_game.models import MyUser, UserScientic
from my_game.models import HullPattern, ShellPattern, ShieldPattern, GeneratorPattern, EnginePattern, \
    ArmorPattern, ModulePattern, FactoryPattern, WeaponPattern, FuelPattern, DevicePattern
from my_game.models import BasicArmor, BasicEngine, BasicFactory, BasicGenerator, \
    BasicHull, BasicModule, BasicShell, BasicShield, BasicWeapon, Race, BasicFuel, BasicDevice


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
            hull_atribute = ['hull_health', 'generator', 'engine', 'weapon', 'armor', 'shield', 'module', 'main_weapon',
                             'hold_size', 'hull_mass', 'hull_size', 'power_consuption']
            trying = random.random()
            if 0.15 <= trying <= 0.3 or 0.7 <= trying <= 0.85:
                number = random.randint(0, 11)
                atribute = hull_atribute[number]
                element = getattr(user_hull, atribute)
                element_basic = getattr(hull_scient, atribute)
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
                                setattr(user_hull, atribute, element)
                                user_hull.save()
                        if number == 0 or number == 8 or number == 10:
                            percent_update = 1 + random.randint(5, 10) / 100.0
                            if element != 0 and element_basic / element > 0.7:
                                element = element * percent_update
                                user_hull.pk = None
                                user_hull.save()
                                user_hull = HullPattern.objects.filter(user=user, basic_hull=hull_scient).last()
                                setattr(user_hull, atribute, element)
                                user_hull.save()
                        else:
                            if element != 0 and element / element_basic < 2:
                                element = element + 1
                                user_hull.pk = None
                                user_hull.save()
                                user_hull = HullPattern.objects.filter(user=user, basic_hull=hull_scient).last()
                                setattr(user_hull, atribute, element)
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
                                setattr(user_hull, atribute, element)
                                user_hull.save()
                        else:
                            if number == 0 or number == 8 or number == 10:
                                percent_update = 1 + random.randint(5, 10) / 100.0
                                if element_basic / element > 0.7:
                                    element = element * percent_update
                                    user_hull.pk = None
                                    user_hull.save()
                                    user_hull = HullPattern.objects.filter(user=user, basic_hull=hull_scient).last()
                                    setattr(user_hull, atribute, element)
                                    user_hull.save()
                            else:
                                if element / element_basic < 2:
                                    element = element + 1
                                    user_hull.pk = None
                                    user_hull.save()
                                    user_hull = HullPattern.objects.filter(user=user, basic_hull=hull_scient).last()
                                    setattr(user_hull, atribute, element)
                                    user_hull.save()
                user_hull = HullPattern.objects.filter(user=user, basic_hull=hull_scient).last()
                price_increase(user_hull)


def armor_upgrade(request):
    user = request
    basic_armor = BasicArmor.objects.all()
    number_armor = len(basic_armor) - 1
    number_armor_scient = random.randint(0, number_armor)
    armor_scient = basic_armor[number_armor_scient]
    user_armor = ArmorPattern.objects.filter(user=user, basic_armor=armor_scient).last()
    if user_armor is None:
        koef = element_open(user, armor_scient)

        if koef < 0:
            koef = 0.00001

        upper_scope = 0.33 * koef
        new_armor = random.random()
        race = user.race.id
        race_koef = Race.objects.filter(id=race).first()
        if 0 < new_armor < upper_scope:
            armor_pattern = ArmorPattern(
                user=user,
                basic_armor=armor_scient,
                armor_name=armor_scient.armor_name,
                armor_health=armor_scient.armor_health,
                value_energy_resistance=armor_scient.value_energy_resistance * race_koef.armor,
                value_phisical_resistance=armor_scient.value_phisical_resistance * race_koef.armor,
                armor_regeneration=armor_scient.armor_regeneration * race_koef.armor,
                armor_power=armor_scient.armor_power,
                armor_mass=armor_scient.armor_mass,
                price_internal_currency=armor_scient.price_internal_currency,
                price_resource1=armor_scient.price_resource1,
                price_resource2=armor_scient.price_resource2,
                price_resource3=armor_scient.price_resource3,
                price_resource4=armor_scient.price_resource4,
                price_mineral1=armor_scient.price_mineral1,
                price_mineral2=armor_scient.price_mineral2,
                price_mineral3=armor_scient.price_mineral3,
                price_mineral4=armor_scient.price_mineral4,
            )
            armor_pattern.save()
            new_factory_pattern(user, 2, armor_scient.id)
    else:
        studied_armor = ArmorPattern.objects.filter(user=user, basic_armor=armor_scient, bought_template=0)
        len_studied_armor = len(studied_armor)
        if len_studied_armor < 2:
            user_armor = ArmorPattern.objects.filter(user=user, basic_armor=armor_scient).last()
            armor_atribute = ['armor_health', 'value_energy_resistance', 'value_phisical_resistance',
                              'armor_regeneration', 'armor_power', 'armor_mass']
            trying = random.random()
            percent_update = 1 + random.randint(5, 10) / 100.0

            if 0.15 <= trying <= 0.3 or 0.7 <= trying <= 0.85:
                number = random.randint(0, 5)
                atribute = armor_atribute[number]
                element = getattr(user_armor, atribute)
                element_basic = getattr(armor_scient, atribute)

                if element != 0:
                    if number == 5:
                        if element / element_basic > 0.7:
                            percent_update = 1 - random.randint(5, 10) / 100.0
                            element = element * percent_update
                            user_armor.pk = None
                            user_armor.save()
                            user_armor = ArmorPattern.objects.filter(user=user, basic_armor=armor_scient).last()
                            setattr(user_armor, atribute, element)
                            user_armor.save()
                    else:
                        ell = element_basic / element
                        if element_basic / element > 0.7:
                            element = element * percent_update
                            user_armor.pk = None
                            user_armor.save()
                            user_armor = ArmorPattern.objects.filter(user=user, basic_armor=armor_scient).last()
                            setattr(user_armor, atribute, element)
                            user_armor.save()
                user_armor = ArmorPattern.objects.filter(user=user, basic_armor=armor_scient).last()
                price_increase(user_armor)


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
        race = user.race.id
        race_koef = Race.objects.filter(id=race).first()
        if 0 < new_shield < upper_scope:
            shield_pattern = ShieldPattern(
                user=user,
                basic_shield=shield_scient,
                shield_name=shield_scient.shield_name,
                shield_health=shield_scient.shield_health,
                value_energy_resistance=shield_scient.value_energy_resistance * race_koef.shield,
                value_phisical_resistance=shield_scient.value_phisical_resistance * race_koef.shield,
                shield_regeneration=shield_scient.shield_regeneration * race_koef.shield,
                number_of_emitter=shield_scient.number_of_emitter,
                shield_mass=shield_scient.shield_mass,
                shield_size=shield_scient.shield_size,
                power_consuption=shield_scient.power_consuption,
                price_internal_currency=shield_scient.price_internal_currency,
                price_resource1=shield_scient.price_resource1,
                price_resource2=shield_scient.price_resource2,
                price_resource3=shield_scient.price_resource3,
                price_resource4=shield_scient.price_resource4,
                price_mineral1=shield_scient.price_mineral1,
                price_mineral2=shield_scient.price_mineral2,
                price_mineral3=shield_scient.price_mineral3,
                price_mineral4=shield_scient.price_mineral4,
            )
            shield_pattern.save()
            new_factory_pattern(user, 3, shield_scient.id)
    else:
        studied_shield = ShieldPattern.objects.filter(user=user, basic_shield=shield_scient, bought_template=0)
        len_studied_shield = len(studied_shield)
        if len_studied_shield < 2:
            shield_atribute = ['shield_health', 'value_energy_resistance', 'value_phisical_resistance',
                               'shield_regeneration', 'number_of_emitter', 'shield_mass', 'shield_size',
                               'power_consuption']
            trying = random.random()
            percent_update = 1 + random.randint(5, 10) / 100.0
            if 0.15 <= trying <= 0.3 or 0.7 <= trying <= 0.85:
                number = random.randint(0, 7)
                atribute = shield_atribute[number]
                element = getattr(user_shield, atribute)
                element_basic = getattr(shield_scient, atribute)
                last_element = getattr(user_shield, atribute)
                if element != 0:
                    if number == 5 or number == 7:
                        if element / element_basic > 0.7:
                            percent_update = 1.0 - random.randint(5, 10) / 100.0
                            element = element * percent_update
                            user_shield.pk = None
                            user_shield.save()
                            user_shield = ShieldPattern.objects.filter(user=user, basic_shield=shield_scient).last()
                            setattr(user_shield, atribute, element)
                            user_shield.save()
                    else:
                        if number == 4:
                            if element_basic / element > 0.5:
                                element = element + 1
                                user_shield.pk = None
                                user_shield.save()
                                user_shield = ShieldPattern.objects.filter(user=user, basic_shield=shield_scient).last()
                                setattr(user_shield, atribute, element)
                                user_shield.save()
                        else:
                            if element_basic / element > 0.7:
                                element = element * percent_update
                                user_shield.pk = None
                                user_shield.save()
                                user_shield = ShieldPattern.objects.filter(user=user, basic_shield=shield_scient).last()
                                setattr(user_shield, atribute, element)
                                user_shield.save()
                user_shield = ShieldPattern.objects.filter(user=user, basic_shield=shield_scient).last()
                price_increase(user_shield)


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
        race = user.race.id
        race_koef = Race.objects.filter(id=race).first()
        if 0 < new_engine < upper_scope:
            engine_pattern = EnginePattern(
                user=user,
                basic_engine=engine_scient,
                engine_name=engine_scient.engine_name,
                engine_health=engine_scient.engine_health,
                system_power=engine_scient.system_power * race_koef.engine_system,
                intersystem_power=engine_scient.intersystem_power * race_koef.engine_intersystem,
                giper_power=engine_scient.giper_power * race_koef.engine_giper,
                nullT_power=engine_scient.nullT_power * race_koef.engine_null,
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
            engine_atribute = ['engine_health', 'system_power', 'intersystem_power', 'giper_power', 'nullT_power',
                               'engine_mass', 'engine_size', 'power_consuption']
            trying = random.random()
            percent_update = 1 + random.randint(5, 10) / 100.0
            if 0.15 <= trying <= 0.3 or 0.7 <= trying <= 0.85:
                number = random.randint(1, 7)
                atribute = engine_atribute[number]
                element = getattr(user_engine, atribute)
                last_element = getattr(user_engine, atribute)
                element_basic = getattr(engine_scient, atribute)
                if element != 0:
                    if number == 5 or number == 6 or number == 7:
                        if element / element_basic > 0.7:
                            percent_update = 1 - random.randint(5, 10) / 100.0
                            element = element * percent_update
                            user_engine.pk = None
                            user_engine.save()
                            user_engine = EnginePattern.objects.filter(user=user, basic_engine=engine_scient).last()
                            setattr(user_engine, atribute, element)
                            user_engine.save()
                    else:
                        if element_basic / element > 0.7:
                            element = element * percent_update
                            user_engine.pk = None
                            user_engine.save()
                            user_engine = EnginePattern.objects.filter(user=user, basic_engine=engine_scient).last()
                            setattr(user_engine, atribute, element)
                            user_engine.save()
                user_engine = EnginePattern.objects.filter(user=user, basic_engine=engine_scient).last()
                price_increase(user_engine)


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
        race = user.race.id
        race_koef = Race.objects.filter(id=race).first()
        if 0 < new_generator < upper_scope:
            generator_pattern = GeneratorPattern(
                user=user,
                basic_generator=generator_scient,
                generator_name=generator_scient.generator_name,
                generator_health=generator_scient.generator_health,
                produced_energy=generator_scient.produced_energy * race_koef.generator,
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
            generator_atribute = ['generator_health', 'produced_energy', 'fuel_necessary', 'generator_mass',
                                  'generator_size']
            trying = random.random()
            percent_update = 1 + random.randint(5, 10) / 100.0
            if 0.15 <= trying <= 0.3 or 0.7 <= trying <= 0.85:
                number = random.randint(0, 4)
                atribute = generator_atribute[number]
                element = getattr(user_generator, atribute)
                last_element = getattr(user_generator, atribute)
                element_basic = getattr(generator_scient, atribute)
                if element != 0:
                    if number == 2 or number == 3 or number == 4:
                        if element / element_basic > 0.7:
                            percent_update = 1 - random.randint(5, 10) / 100.0
                            element = element * percent_update
                            user_generator.pk = None
                            user_generator.save()
                            user_generator = GeneratorPattern.objects.filter(user=user,
                                                                             basic_generator=generator_scient).last()
                            setattr(user_generator, atribute, element)
                            user_generator.save()
                    else:
                        if element_basic / element > 0.7:
                            element = element * percent_update
                            user_generator.pk = None
                            user_generator.save()
                            user_generator = GeneratorPattern.objects.filter(user=user,
                                                                             basic_generator=generator_scient).last()
                            setattr(user_generator, atribute, element)
                            user_generator.save()

                user_generator = GeneratorPattern.objects.filter(user=user, basic_generator=generator_scient).last()
                price_increase(user_generator)


def weapon_upgrade(request):
    user = request
    basic_weapon = BasicWeapon.objects.all()
    number_weapon = len(basic_weapon) - 1
    number_weapon_scient = random.randint(0, number_weapon)
    weapon_scient = basic_weapon[number_weapon_scient]
    user_weapon = WeaponPattern.objects.filter(user=user, basic_weapon=weapon_scient).last()
    if user_weapon is None:
        koef = element_open(user, weapon_scient)
        if koef < 0:
            koef = 0.00001

        upper_scope = 0.33 * koef
        new_weapon = random.random()
        race = user.race.id
        race_koef = Race.objects.filter(id=race).first()
        weapon_class = weapon_scient.weapon_class
        if weapon_class == 1:
            weapon = race_koef.weapon_attack
        else:
            weapon = race_koef.weapon_defense
        if 0 < new_weapon < upper_scope:
            weapon_pattern = WeaponPattern(
                user=user,
                basic_weapon=weapon_scient,
                weapon_name=weapon_scient.weapon_name,
                weapon_health=weapon_scient.weapon_health,
                weapon_energy_damage=weapon_scient.weapon_energy_damage * weapon,
                weapon_regenerations=weapon_scient.weapon_regenerations * weapon,
                number_of_bursts=weapon_scient.number_of_bursts * weapon,
                weapon_range=weapon_scient.weapon_range * weapon,
                weapon_accuracy=weapon_scient.weapon_accuracy * weapon,
                weapon_ass=weapon_scient.weapon_mass,
                weapon_size=weapon_scient.weapon_size,
                power_consuption=weapon_scient.power_consuption,
                weapon_class=weapon_scient.weapon_class,
                price_internal_currency=weapon_scient.price_internal_currency,
                price_resource1=weapon_scient.price_resource1,
                price_resource2=weapon_scient.price_resource2,
                price_resource3=weapon_scient.price_resource3,
                price_resource4=weapon_scient.price_resource4,
                price_mineral1=weapon_scient.price_mineral1,
                price_mineral2=weapon_scient.price_mineral2,
                price_mineral3=weapon_scient.price_mineral3,
                price_mineral4=weapon_scient.price_mineral4,
            )
            weapon_pattern.save()
            new_factory_pattern(user, 6, weapon_scient.id)

    else:
        studied_weapon = WeaponPattern.objects.filter(user=user, basic_weapon=weapon_scient, bought_template=0)
        len_studied_weapon = len(studied_weapon)
        if len_studied_weapon < 2:
            user_weapon = WeaponPattern.objects.filter(user=user, basic_weapon=weapon_scient).last()
            weapon_atribute = ['health', 'energy_damage', 'regenerations', 'number_of_bursts', 'range', 'accuracy',
                               'mass', 'size', 'power_consuption']
            trying = random.random()
            percent_update = 1 + random.randint(5, 10) / 100.0
            if 0.15 <= trying <= 0.3 or 0.7 <= trying <= 0.85:
                number = random.randint(0, 8)
                atribute = weapon_atribute[number]
                element = getattr(user_weapon, atribute)
                last_element = getattr(user_weapon, atribute)
                element_basic = getattr(weapon_scient, atribute)
                if element != 0:
                    if number == 6 or number == 7 or number == 8:
                        if element / element_basic > 0.7:
                            percent_update = 1 - random.randint(5, 10) / 100.0
                            element = element * percent_update
                            user_weapon.pk = None
                            user_weapon.save()
                            user_weapon = WeaponPattern.objects.filter(user=user, basic_weapon=weapon_scient).last()
                            setattr(user_weapon, atribute, element)
                            user_weapon.save()
                    else:
                        if number == 3 and element / element_basic < 2:
                            element = element + 1
                            user_weapon.pk = None
                            user_weapon.save()
                            user_weapon = WeaponPattern.objects.filter(user=user, basic_weapon=weapon_scient).last()
                            setattr(user_weapon, atribute, element)
                            user_weapon.save()
                        else:
                            if number == 5:
                                if element_basic / element > 0.75:
                                    element = element * percent_update
                                    user_weapon.pk = None
                                    user_weapon.save()
                                    user_weapon = WeaponPattern.objects.filter(user=user,
                                                                            basic_weapon=weapon_scient).last()
                                    setattr(user_weapon, atribute, element)
                                    user_weapon.save()
                            else:
                                if element_basic / element > 0.7:
                                    element = element * percent_update
                                    user_weapon.pk = None
                                    user_weapon.save()
                                    user_weapon = WeaponPattern.objects.filter(user=user,
                                                                            basic_weapon=weapon_scient).last()
                                    setattr(user_weapon, atribute, element)
                                    user_weapon.save()
                user_weapon = WeaponPattern.objects.filter(user=user, basic_weapon=weapon_scient).last()
                price_increase(user_weapon)


def shell_upgrade(request):
    user = request
    basic_shell = BasicShell.objects.all()
    number_shell = len(basic_shell) - 1
    number_shell_scient = random.randint(0, number_shell)
    shell_scient = basic_shell[number_shell_scient]
    user_shell = ShellPattern.objects.filter(user=user, basic_shell=shell_scient).last()
    if user_shell is None:
        koef = element_open(user, shell_scient)

        if koef < 0:
            koef = 0.00001

        upper_scope = 0.33 * koef
        new_shell = random.random()
        if 0 < new_shell < upper_scope:
            shell_pattern = ShellPattern(
                user=user,
                basic_shell=shell_scient,
                shell_name=shell_scient.shell_name,
                shell_phisical_damage=shell_scient.shell_phisical_damage,
                shell_speed=shell_scient.shell_speed,
                shell_mass=shell_scient.shell_mass,
                shell_size=shell_scient.shell_size,
                price_internal_currency=shell_scient.price_internal_currency,
                price_resource1=shell_scient.price_resource1,
                price_resource2=shell_scient.price_resource2,
                price_resource3=shell_scient.price_resource3,
                price_resource4=shell_scient.price_resource4,
                price_mineral1=shell_scient.price_mineral1,
                price_mineral2=shell_scient.price_mineral2,
                price_mineral3=shell_scient.price_mineral3,
                price_mineral4=shell_scient.price_mineral4,
            )
            shell_pattern.save()
            new_factory_pattern(user, 7, shell_scient.id)
    else:
        studied_shell = ShellPattern.objects.filter(user=user, basic_shell=shell_scient, bought_template=0)
        len_studied_shell = len(studied_shell)
        if len_studied_shell < 2:
            shell_atribute = ['shell_phisical_damage', 'shell_speed', 'shell_mass', 'shell_size']
            trying = random.random()
            percent_update = 1 + random.randint(5, 10) / 100.0
            if 0.15 <= trying <= 0.3 or 0.7 <= trying <= 0.85:
                number = random.randint(0, 3)
                atribute = shell_atribute[number]
                element = getattr(user_shell, atribute)
                last_element = getattr(user_shell, atribute)
                element_basic = getattr(shell_scient, atribute)
                if element != 0:
                    if number == 2 or number == 3:
                        if element / element_basic > 0.7:
                            percent_update = 1 - random.randint(5, 10) / 100.0
                            element = element * percent_update
                            user_shell.pk = None
                            user_shell.save()
                            user_shell = ShellPattern.objects.filter(user=user, basic_shell=shell_scient).last()
                            setattr(user_shell, atribute, element)
                            user_shell.save()
                    else:
                        if element_basic / element > 0.7:
                            element = element * percent_update
                            user_shell.pk = None
                            user_shell.save()
                            user_shell = ShellPattern.objects.filter(user=user, basic_shell=shell_scient).last()
                            setattr(user_shell, atribute, element)
                            user_shell.save()
                user_shell = ShellPattern.objects.filter(user=user, basic_shell=shell_scient).last()
                price_increase(user_shell)


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
        race = user.race.id
        race_koef = Race.objects.filter(id=race).first()
        module_class = module_scient.module_class
        if module_class == 1:
            module = race_koef.exploration
        else:
            if module_class == 2:
                module = race_koef.disguse
            else:
                module = race_koef.auximilary
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
            module_atribute = ['module_health', 'param1', 'param2', 'param3', 'module_mass', 'module_size', 'power_consuption']
            trying = random.random()
            percent_update = 1 + random.randint(5, 10) / 100.0
            if 0.15 <= trying <= 0.3 or 0.7 <= trying <= 0.85:
                number = random.randint(0, 6)
                atribute = module_atribute[number]
                element = getattr(user_module, atribute)
                last_element = getattr(user_module, atribute)
                element_basic = getattr(module_scient, atribute)
                if element != 0:
                    if number == 4 or number == 5 or number == 6:
                        if element / element_basic > 0.7:
                            percent_update = 1 - random.randint(5, 10) / 100.0
                            element = element * percent_update
                            user_module.pk = None
                            user_module.save()
                            user_module = ModulePattern.objects.filter(user=user, basic_module=module_scient).last()
                            setattr(user_module, atribute, element)
                            user_module.save()
                    else:
                        if element_basic / element > 0.7:
                            element = element * percent_update
                            user_module.pk = None
                            user_module.save()
                            user_module = ModulePattern.objects.filter(user=user, basic_module=module_scient).last()
                            setattr(user_module, atribute, element)
                            user_module.save()
                user_module = ModulePattern.objects.filter(user=user, basic_module=module_scient).last()
                price_increase(user_module)


def device_open(request):
    user = request
    basic_device = BasicDevice.objects.all()
    number_device = len(basic_device) - 1
    number_device_scient = random.randint(0, number_device)
    device_scient = basic_device[number_device_scient]
    user_device = DevicePattern.objects.filter(user=user, basic_device=device_scient).last()
    if user_device is None:
        koef = element_open(user, device_scient)
        if koef < 0:
            koef = 0.00001

        upper_scope = 1  # 0.33 * koef
        new_device = random.random()

        if 0 < new_device < upper_scope:
            device_pattern = DevicePattern(
                user=user,
                basic_device=device_scient,
                device_name=device_scient.device_name,
                device_health=device_scient.device_health,
                param1=device_scient.param1,
                param2=device_scient.param2,
                param3=device_scient.param3,
                device_mass=device_scient.device_mass,
                device_size=device_scient.device_size,
                power_consuption=device_scient.power_consuption,
                device_class=device_scient.device_class,
                price_internal_currency=device_scient.price_internal_currency,
                price_resource1=device_scient.price_resource1,
                price_resource2=device_scient.price_resource2,
                price_resource3=device_scient.price_resource3,
                price_resource4=device_scient.price_resource4,
                price_mineral1=device_scient.price_mineral1,
                price_mineral2=device_scient.price_mineral2,
                price_mineral3=device_scient.price_mineral3,
                price_mineral4=device_scient.price_mineral4,
            )
            device_pattern.save()
            new_factory_pattern(user, 9, device_scient.id)


def element_open(*args):
    user = args[0]
    element_scient = args[1]
    all_base = int(element_scient.min_all_scientic)
    scin_user = UserScientic.objects.filter(user=user).first()
    all_user = int(scin_user.all_scientic)
    if all_base < all_user:
        koef_all = (all_user - all_base) / 100.0
    else:
        koef_all = -(all_base - all_user) / 100.0

    math_base = int(element_scient.min_math)
    math_user = int(scin_user.mathematics_up)
    if math_base != 0:
        if math_base < math_user:
            koef_math = (math_user - math_base) / 100.0
        else:
            koef_math = (math_user - math_base) / 100.0
    else:
        koef_math = 0

    phis_base = int(element_scient.min_phis)
    phis_user = int(scin_user.phisics_up)
    if phis_base != 0:
        if phis_base < phis_user:
            koef_phis = (phis_user - phis_base) / 100.0
        else:
            koef_phis = (phis_user - phis_base) / 100.0
    else:
        koef_phis = 0

    biol_base = int(element_scient.min_biol)
    biol_user = int(scin_user.biologic_chimics_up)
    if biol_base != 0:
        if biol_base < biol_user:
            koef_biol = (biol_user - biol_base) / 100.0
        else:
            koef_biol = -(biol_base - biol_user) / 100.0
    else:
        koef_biol = 0

    energy_base = int(element_scient.min_energy)
    energy_user = int(scin_user.energetics_up)
    if energy_base != 0:
        if energy_base < energy_user:
            koef_energy = (energy_user - energy_base) / 100.0
        else:
            koef_energy = (energy_user - energy_base) / 100.0
    else:
        koef_energy = 0

    radio_base = int(element_scient.min_radio)
    radio_user = int(scin_user.radionics_up)
    if radio_base != 0:
        if radio_base < radio_user:
            koef_radio = (radio_user - radio_base) / 100.0
        else:
            koef_radio = (radio_user - radio_base) / 100.0
    else:
        koef_radio = 0

    nano_base = int(element_scient.min_nanotech)
    nano_user = int(scin_user.nanotech_up)
    if nano_base != 0:
        if nano_base < nano_user:
            koef_nanotech = (nano_user - nano_base) / 100.0
        else:
            koef_nanotech = -(nano_base - nano_user) / 100.0
    else:
        koef_nanotech = 0

    astro_base = int(element_scient.min_astronomy)
    astro_user = int(scin_user.astronomy_up)
    if astro_base != 0:
        if astro_base < astro_user:
            koef_astronomy = (astro_user - astro_base) / 100.0
        else:
            koef_astronomy = -(astro_base - astro_user) / 100.0
    else:
        koef_astronomy = 0

    logist_base = int(element_scient.min_logist)
    logist_user = int(scin_user.logistic_up)
    if logist_base != 0:
        if logist_base < logist_user:
            koef_logist = (logist_user - logist_base) / 100.0
        else:
            koef_logist = -(logist_base - logist_user) / 100.0
    else:
        koef_logist = 0

    lucky = user.user_luckyness
    koef = (1 + (
        koef_all + koef_math + koef_phis + koef_biol + koef_energy + koef_radio + koef_nanotech + koef_astronomy + koef_logist)) * (
               1 + lucky / 100.0)
    return (koef)


def price_increase(*args):
    pattern = args[0]
    koef_up = 1.10
    price_internal_currency = pattern.price_internal_currency * koef_up
    price_resource1 = pattern.price_resource1 * koef_up
    price_resource2 = pattern.price_resource2 * koef_up
    price_resource3 = pattern.price_resource3 * koef_up
    price_resource4 = pattern.price_resource4 * koef_up
    price_mineral1 = pattern.price_mineral1 * koef_up
    price_mineral2 = pattern.price_mineral2 * koef_up
    price_mineral3 = pattern.price_mineral3 * koef_up
    price_mineral4 = pattern.price_mineral4 * koef_up
    setattr(pattern, "price_internal_currency", price_internal_currency)
    setattr(pattern, 'price_resource1', price_resource1)
    setattr(pattern, 'price_resource2', price_resource2)
    setattr(pattern, 'price_resource3', price_resource3)
    setattr(pattern, 'price_resource4', price_resource4)
    setattr(pattern, 'price_mineral1', price_mineral1)
    setattr(pattern, 'price_mineral2', price_mineral2)
    setattr(pattern, 'price_mineral3', price_mineral3)
    setattr(pattern, 'price_mineral4', price_mineral4)
    pattern.save()


def new_factory_pattern(*args):
    new_factory_patt = args
    user = new_factory_patt[0]
    prod_class = int(new_factory_patt[1])
    prod_id = new_factory_patt[2]
    new_factory = BasicFactory.objects.filter(production_class=prod_class, production_id=prod_id).first()
    user_factory = FactoryPattern(
        user=user,
        basic_factory=new_factory,
        factory_name=new_factory.factory_name,
        price_internal_currency=new_factory.price_internal_currency,
        price_resource1=new_factory.price_resource1,
        price_resource2=new_factory.price_resource2,
        price_resource3=new_factory.price_resource3,
        price_resource4=new_factory.price_resource4,
        price_mineral1=new_factory.price_mineral1,
        price_mineral2=new_factory.price_mineral2,
        price_mineral3=new_factory.price_mineral3,
        price_mineral4=new_factory.price_mineral4,
        cost_expert_deployment=new_factory.cost_expert_deployment,
        assembly_workpiece=new_factory.assembly_workpiece,
        time_deployment=new_factory.time_deployment,
        production_class=new_factory.production_class,
        production_id=new_factory.production_id,
        time_production=new_factory.time_production,
        factory_size=new_factory.factory_size,
        factory_mass=new_factory.factory_mass,
        power_consumption=new_factory.power_consumption
    )
    user_factory.save()
    return ()


def open_fuel(*args):
    user = args[0]
    system = args[1]
    inter = args[2]

    fuel_class = 0

    if system != 0 and inter != 0:
        fuel_class = 3
    elif system != 0 and inter == 0:
        fuel_class = 1
    elif system == 0 and inter != 0:
        fuel_class = 2

    fuel_pattern = FuelPattern.objects.filter(user=user, fuel_class=fuel_class).first()
    if fuel_pattern is None:
        basic_fuel = BasicFuel.objects.filter(fuel_class=fuel_class).first()
        fuel_pattern = FuelPattern(
            user=user,
            fuel_name=basic_fuel.fuel_name,
            basic_fuel=basic_fuel,
            fuel_mass=basic_fuel.fuel_mass,
            fuel_size=basic_fuel.fuel_size,
            fuel_efficiency=basic_fuel.fuel_efficiency,
            fuel_class=basic_fuel.fuel_class,
            fuel_id=basic_fuel.fuel_id,
            price_internal_currency=basic_fuel.price_internal_currency,
            price_resource1=basic_fuel.price_resource1,
            price_resource2=basic_fuel.price_resource2,
            price_resource3=basic_fuel.price_resource3,
            price_resource4=basic_fuel.price_resource4,
            price_mineral1=basic_fuel.price_mineral1,
            price_mineral2=basic_fuel.price_mineral2,
            price_mineral3=basic_fuel.price_mineral3,
            price_mineral4=basic_fuel.price_mineral4,
        )
        new_factory_pattern(user, 14, fuel_pattern)
