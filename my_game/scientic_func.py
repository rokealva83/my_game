# -*- coding: utf-8 -*-

import math
import random
from datetime import datetime

from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from models import Galaxy, System, Planet, MyUser, User_city, Warehouse, User_scientic, Turn_production, Turn_building, \
    Turn_assembly_pieces
from models import Basic_scientic, Turn_scientic, Basic_factory
from models import Hull_pattern, Shell_pattern, Shield_pattern, Generator_pattern, Engine_pattern, \
    Armor_pattern, Module_pattern, Factory_pattern, Weapon_pattern, Factory_installed
from models import Warehouse_factory, Warehouse_element
import function
import scientic_work
import scientic_func
from models import User_variables
from models import Project_ship, Element_ship
from models import Basic_scientic, Turn_scientic, Basic_armor, Basic_engine, Basic_factory, Basic_generator, \
    Basic_hull, Basic_module, Basic_shell, Basic_shield, Basic_weapon, Turn_building, Turn_assembly_pieces, \
    Turn_production, Race


def hull_upgrade(request):
    user = request
    b_hull = Basic_hull.objects.all()
    number_hull = len(b_hull) - 1
    number_hull_scient = random.randint(0, number_hull)
    hull_scient = b_hull[number_hull_scient]
    u_hull = Hull_pattern.objects.filter(user=user, basic_id=hull_scient.id).last()
    if u_hull is None:
        koef = element_open(user, hull_scient)

        if koef < 0:
            koef = 0.00001

        upper_scope = 0.33 * koef
        new_hull = random.random()
        if 0 < new_hull < upper_scope:
            hull_pattern = Hull_pattern(
                user=user,
                basic_id=hull_scient.id,
                health=hull_scient.health,
                generator=hull_scient.generator,
                engine=hull_scient.engine,
                weapon=hull_scient.weapon,
                armor=hull_scient.armor,
                shield=hull_scient.shield,
                module=hull_scient.module,
                main_weapon=hull_scient.main_weapon,
                hold_size=hull_scient.hold_size,
                mass=hull_scient.mass,
                size=hull_scient.size,
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
        u_hull = Hull_pattern.objects.filter(user=user, basic_id=hull_scient.id).last()
        hull_atribute = ['health', 'generator', 'engine', 'weapon', 'armor', 'shield', 'module', \
                         'main_weapon', 'hold_size', 'mass', 'size', 'power_consuption']
        trying = random.random()
        if 0.15 <= trying <= 0.3 or 0.7 <= trying <= 0.85:
            number = random.randint(0, 11)
            atribute = hull_atribute[number]
            element = getattr(u_hull, atribute)
            element_basic = getattr(hull_scient, atribute)
            if u_hull.basic_id == 1:
                if number == 5 and element == 0:
                    element = 1
                else:
                    if number == 9 or number == 11:
                        percent_update = 1 - random.randint(5, 10) / 100.0
                        if element / element_basic > 0.7:
                            element = element * percent_update
                            u_hull.pk = None
                            u_hull.save()
                            u_hull = Hull_pattern.objects.filter(user=user, basic_id=hull_scient.id).last()
                            setattr(u_hull, atribute, element)
                            u_hull.save()
                    if number == 0 or number == 8 or number == 10:
                        percent_update = 1 + random.randint(5, 10) / 100.0
                        if element != 0 and element_basic / element > 0.7:
                            element = element * percent_update
                            u_hull.pk = None
                            u_hull.save()
                            u_hull = Hull_pattern.objects.filter(user=user, basic_id=hull_scient.id).last()
                            setattr(u_hull, atribute, element)
                            u_hull.save()
                    else:
                        if element != 0 and element / element_basic < 2:
                            element = element + 1
                            u_hull.pk = None
                            u_hull.save()
                            u_hull = Hull_pattern.objects.filter(user=user, basic_id=hull_scient.id).last()
                            setattr(u_hull, atribute, element)
                            u_hull.save()
            else:
                if element != 0:
                    if number == 9 or number == 11:
                        percent_update = 1 - random.randint(5, 10) / 100.0
                        if element / element_basic > 0.7:
                            element = element * percent_update
                            u_hull.pk = None
                            u_hull.save()
                            u_hull = Hull_pattern.objects.filter(user=user, basic_id=hull_scient.id).last()
                            setattr(u_hull, atribute, element)
                            u_hull.save()
                    else:
                        if number == 0 or number == 8 or number == 10:
                            percent_update = 1 + random.randint(5, 10) / 100.0
                            if element_basic / element > 0.7:
                                element = element * percent_update
                                u_hull.pk = None
                                u_hull.save()
                                u_hull = Hull_pattern.objects.filter(user=user, basic_id=hull_scient.id).last()
                                setattr(u_hull, atribute, element)
                                u_hull.save()
                        else:
                            if element / element_basic < 2:
                                element = element + 1
                                u_hull.pk = None
                                u_hull.save()
                                u_hull = Hull_pattern.objects.filter(user=user, basic_id=hull_scient.id).last()
                                setattr(u_hull, atribute, element)
                                u_hull.save()
            u_hull = Hull_pattern.objects.filter(user=user, basic_id=hull_scient.id).last()
            price_increase(u_hull)


def armor_upgrade(request):
    user = request
    b_armor = Basic_armor.objects.all()
    number_armor = len(b_armor) - 1
    number_armor_scient = random.randint(0, number_armor)
    armor_scient = b_armor[number_armor_scient]
    u_armor = Armor_pattern.objects.filter(user=user, basic_id=armor_scient.id).last()
    if u_armor is None:
        koef = element_open(user, armor_scient)

        if koef < 0:
            koef = 0.00001

        upper_scope = 0.33 * koef
        new_armor = random.random()
        user_race = MyUser.objects.filter(user_id=user).first()
        race = user_race.race_id
        race_koef = Race.objects.filter(id=race).first()
        if 0 < new_armor < upper_scope:
            armor_pattern = Armor_pattern(
                user=user,
                basic_id=armor_scient.id,
                health=armor_scient.health,
                value_energy_resistance=armor_scient.value_energy_resistance * race_koef.armor,
                value_phisical_resistance=armor_scient.value_phisical_resistance * race_koef.armor,
                regeneration=armor_scient.regeneration * race_koef.armor,
                power=armor_scient.power,
                mass=armor_scient.mass,
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
        u_armor = Armor_pattern.objects.filter(user=user, basic_id=armor_scient.id).last()
        armor_atribute = ['health', 'value_energy_resistance', 'value_phisical_resistance', 'regeneration', 'power',
                          'mass']
        trying = random.random()
        percent_update = 1 + random.randint(5, 10) / 100.0

        if 0.15 <= trying <= 0.3 or 0.7 <= trying <= 0.85:
            number = random.randint(0, 5)
            atribute = armor_atribute[number]
            element = getattr(u_armor, atribute)
            element_basic = getattr(armor_scient, atribute)

            if element != 0:
                if number == 5:
                    if element / element_basic > 0.7:
                        percent_update = 1 - random.randint(5, 10) / 100.0
                        element = element * percent_update
                        u_armor.pk = None
                        u_armor.save()
                        u_armor = Armor_pattern.objects.filter(user=user, basic_id=armor_scient.id).last()
                        setattr(u_armor, atribute, element)
                        u_armor.save()
                else:
                    ell = element_basic / element
                    if element_basic / element > 0.7:
                        element = element * percent_update
                        u_armor.pk = None
                        u_armor.save()
                        u_armor = Armor_pattern.objects.filter(user=user, basic_id=armor_scient.id).last()
                        setattr(u_armor, atribute, element)
                        u_armor.save()
            u_armor = Armor_pattern.objects.filter(user=user, basic_id=armor_scient.id).last()
            price_increase(u_armor)


def shield_upgrade(request):
    user = request
    b_shield = Basic_shield.objects.all()
    number_shield = len(b_shield) - 1
    number_shield_scient = random.randint(0, number_shield)
    shield_scient = b_shield[number_shield_scient]
    u_shield = Shield_pattern.objects.filter(user=user, basic_id=shield_scient.id).last()
    if u_shield is None:
        koef = element_open(user, shield_scient)

        if koef < 0:
            koef = 0.00001

        upper_scope = 0.33 * koef
        new_shield = random.random()
        user_race = MyUser.objects.filter(user_id=user).first()
        race = user_race.race_id
        race_koef = Race.objects.filter(id=race).first()
        if 0 < new_shield < upper_scope:
            shield_pattern = Shield_pattern(
                user=user,
                basic_id=shield_scient.id,
                health=shield_scient.health,
                value_energy_resistance=shield_scient.value_energy_resistance * race_koef.shield,
                value_phisical_resistance=shield_scient.value_phisical_resistance * race_koef.shield,
                regeneration=shield_scient.regeneration * race_koef.shield,
                number_of_emitter=shield_scient.number_of_emitter,
                mass=shield_scient.mass,
                size=shield_scient.size,
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
        shield_atribute = ['health', 'value_energy_resistance', 'value_phisical_resistance', 'regeneration', \
                           'number_of_emitter', 'mass', 'size', 'power_consuption']
        trying = random.random()
        percent_update = 1 + random.randint(5, 10) / 100.0
        if 0.15 <= trying <= 0.3 or 0.7 <= trying <= 0.85:
            number = random.randint(0, 7)
            atribute = shield_atribute[number]
            element = getattr(u_shield, atribute)
            element_basic = getattr(shield_scient, atribute)
            last_element = getattr(u_shield, atribute)
            if element != 0:
                if number == 5 or number == 7:
                    if element / element_basic > 0.7:
                        percent_update = 1.0 - random.randint(5, 10) / 100.0
                        element = element * percent_update
                        u_shield.pk = None
                        u_shield.save()
                        u_shield = Shield_pattern.objects.filter(user=user, basic_id=shield_scient.id).last()
                        setattr(u_shield, atribute, element)
                        u_shield.save()
                else:
                    if number == 4:
                        if element_basic / element > 0.5:
                            element = element + 1
                            u_shield.pk = None
                            u_shield.save()
                            u_shield = Shield_pattern.objects.filter(user=user, basic_id=shield_scient.id).last()
                            setattr(u_shield, atribute, element)
                            u_shield.save()
                    else:
                        if element_basic / element > 0.7:
                            element = element * percent_update
                            u_shield.pk = None
                            u_shield.save()
                            u_shield = Shield_pattern.objects.filter(user=user, basic_id=shield_scient.id).last()
                            setattr(u_shield, atribute, element)
                            u_shield.save()
            u_shield = Shield_pattern.objects.filter(user=user, basic_id=shield_scient.id).last()
            price_increase(u_shield)


def engine_upgrade(request):
    user = request
    b_engine = Basic_engine.objects.all()
    number_engine = len(b_engine) - 1
    number_engine_scient = random.randint(0, number_engine)
    engine_scient = b_engine[number_engine_scient]
    u_engine = Engine_pattern.objects.filter(user=user, basic_id=engine_scient.id).last()
    if u_engine is None:
        koef = element_open(user, engine_scient)

        if koef < 0:
            koef = 0.00001

        upper_scope = 0.33 * koef
        new_engine = random.random()
        user_race = MyUser.objects.filter(user_id=user).first()
        race = user_race.race_id
        race_koef = Race.objects.filter(id=race).first()
        if 0 < new_engine < upper_scope:
            engine_pattern = Engine_pattern(
                user=user,
                basic_id=engine_scient.id,
                health=engine_scient.health,
                system_power=engine_scient.system_power * race_koef.engine_system,
                intersystem_power=engine_scient.intersystem_power * race_koef.engine_intersystem,
                giper_power=engine_scient.giper_power * race_koef.engine_giper,
                nullT_power=engine_scient.nullT_power * race_koef.engine_null,
                mass=engine_scient.mass,
                size=engine_scient.size,
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
    else:
        u_engine = Engine_pattern.objects.filter(user=user, basic_id=engine_scient.id).last()
        engine_atribute = ['health', 'system_power', 'intersystem_power', 'giper_power', \
                           'nullT_power', 'mass', 'size', 'power_consuption']
        trying = random.random()
        percent_update = 1 + random.randint(5, 10) / 100.0
        if 0.15 <= trying <= 0.3 or 0.7 <= trying <= 0.85:
            number = random.randint(1, 7)
            atribute = engine_atribute[number]
            element = getattr(u_engine, atribute)
            last_element = getattr(u_engine, atribute)
            element_basic = getattr(engine_scient, atribute)
            if element != 0:
                if number == 5 or number == 6 or number == 7:
                    if element / element_basic > 0.7:
                        percent_update = 1 - random.randint(5, 10) / 100.0
                        element = element * percent_update
                        u_engine.pk = None
                        u_engine.save()
                        u_engine = Engine_pattern.objects.filter(user=user, basic_id=engine_scient.id).last()
                        setattr(u_engine, atribute, element)
                        u_engine.save()
                else:
                    if element_basic / element > 0.7:
                        element = element * percent_update
                        u_engine.pk = None
                        u_engine.save()
                        u_engine = Engine_pattern.objects.filter(user=user, basic_id=engine_scient.id).last()
                        setattr(u_engine, atribute, element)
                        u_engine.save()
            u_engine = Engine_pattern.objects.filter(user=user, basic_id=engine_scient.id).last()
            price_increase(u_engine)


def generator_upgrade(request):
    user = request
    b_generator = Basic_generator.objects.all()
    number_generator = len(b_generator) - 1
    number_generator_scient = random.randint(0, number_generator)
    generator_scient = b_generator[number_generator_scient]
    u_generator = Generator_pattern.objects.filter(user=user, basic_id=generator_scient.id).last()
    if u_generator is None:
        koef = element_open(user, generator_scient)

        if koef < 0:
            koef = 0.00001

        upper_scope = 0.33 * koef
        new_generator = random.random()
        user_race = MyUser.objects.filter(user_id=user).first()
        race = user_race.race_id
        race_koef = Race.objects.filter(id=race).first()
        if 0 < new_generator < upper_scope:
            generator_pattern = Generator_pattern(
                user=user,
                basic_id=generator_scient.id,
                health=generator_scient.health,
                produced_energy=generator_scient.produced_energy * race_koef.generator,
                fuel_necessary=generator_scient.fuel_necessary,
                mass=generator_scient.mass,
                size=generator_scient.size,
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
        generator_atribute = ['health', 'produced_energy', 'fuel_necessary', 'mass', 'size']
        trying = random.random()
        percent_update = 1 + random.randint(5, 10) / 100.0
        if 0.15 <= trying <= 0.3 or 0.7 <= trying <= 0.85:
            number = random.randint(0, 4)
            atribute = generator_atribute[number]
            element = getattr(u_generator, atribute)
            last_element = getattr(u_generator, atribute)
            element_basic = getattr(generator_scient, atribute)
            if element != 0:
                if number == 2 or number == 3 or number == 4:
                    if element / element_basic > 0.7:
                        percent_update = 1 - random.randint(5, 10) / 100.0
                        element = element * percent_update
                        u_generator.pk = None
                        u_generator.save()
                        u_generator = Generator_pattern.objects.filter(user=user, basic_id=generator_scient.id).last()
                        setattr(u_generator, atribute, element)
                        u_generator.save()
                else:
                    if element_basic / element > 0.7:
                        element = element * percent_update
                        u_generator.pk = None
                        u_generator.save()
                        u_generator = Generator_pattern.objects.filter(user=user, basic_id=generator_scient.id).last()
                        setattr(u_generator, atribute, element)
                        u_generator.save()

            u_generator = Generator_pattern.objects.filter(user=user, basic_id=generator_scient.id).last()
            price_increase(u_generator)


def weapon_upgrade(request):
    user = request
    b_weapon = Basic_weapon.objects.all()
    number_weapon = len(b_weapon) - 1
    number_weapon_scient = random.randint(0, number_weapon)
    weapon_scient = b_weapon[number_weapon_scient]
    u_weapon = Weapon_pattern.objects.filter(user=user, basic_id=weapon_scient.id).last()
    if u_weapon is None:
        koef = element_open(user, weapon_scient)
        if koef < 0:
            koef = 0.00001

        upper_scope = 0.33 * koef
        new_weapon = random.random()
        user_race = MyUser.objects.filter(user_id=user).first()
        race = user_race.race_id
        race_koef = Race.objects.filter(id=race).first()
        weapon_class = weapon_scient.weapon_class
        if weapon_class == 1:
            weapon = race_koef.weapon_attack
        else:
            weapon = race_koef.weapon_defense
        if 0 < new_weapon < upper_scope:
            weapon_pattern = Weapon_pattern(
                user=user,
                basic_id=weapon_scient.id,
                health=weapon_scient.health,
                energy_damage=weapon_scient.energy_damage * weapon,
                regenerations=weapon_scient.regenerations * weapon,
                number_of_bursts=weapon_scient.number_of_bursts * weapon,
                range=weapon_scient.range * weapon,
                accuracy=weapon_scient.accuracy * weapon,
                mass=weapon_scient.mass,
                size=weapon_scient.size,
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
        u_weapon = Weapon_pattern.objects.filter(user=user, basic_id=weapon_scient.id).last()
        weapon_atribute = ['health', 'energy_damage', 'regenerations', 'number_of_bursts', \
                           'range', 'accuracy', 'mass', 'size', 'power_consuption']
        trying = random.random()
        percent_update = 1 + random.randint(5, 10) / 100.0
        if 0.15 <= trying <= 0.3 or 0.7 <= trying <= 0.85:
            number = random.randint(0, 8)
            atribute = weapon_atribute[number]
            element = getattr(u_weapon, atribute)
            last_element = getattr(u_weapon, atribute)
            element_basic = getattr(weapon_scient, atribute)
            if element != 0:
                if number == 6 or number == 7 or number == 8:
                    if element / element_basic > 0.7:
                        percent_update = 1 - random.randint(5, 10) / 100.0
                        element = element * percent_update
                        u_weapon.pk = None
                        u_weapon.save()
                        u_weapon = Weapon_pattern.objects.filter(user=user, basic_id=weapon_scient.id).last()
                        setattr(u_weapon, atribute, element)
                        u_weapon.save()
                else:
                    if number == 3 and element / element_basic < 2:
                        element = element + 1
                        u_weapon.pk = None
                        u_weapon.save()
                        u_weapon = Weapon_pattern.objects.filter(user=user, basic_id=weapon_scient.id).last()
                        setattr(u_weapon, atribute, element)
                        u_weapon.save()
                    else:
                        if number == 5:
                            if element_basic / element > 0.75:
                                element = element * percent_update
                                u_weapon.pk = None
                                u_weapon.save()
                                u_weapon = Weapon_pattern.objects.filter(user=user, basic_id=weapon_scient.id).last()
                                setattr(u_weapon, atribute, element)
                                u_weapon.save()
                        else:
                            if element_basic / element > 0.7:
                                element = element * percent_update
                                u_weapon.pk = None
                                u_weapon.save()
                                u_weapon = Weapon_pattern.objects.filter(user=user, basic_id=weapon_scient.id).last()
                                setattr(u_weapon, atribute, element)
                                u_weapon.save()
            u_weapon = Weapon_pattern.objects.filter(user=user, basic_id=weapon_scient.id).last()
            price_increase(u_weapon)


def shell_upgrade(request):
    user = request
    b_shell = Basic_shell.objects.all()
    number_shell = len(b_shell) - 1
    number_shell_scient = random.randint(0, number_shell)
    shell_scient = b_shell[number_shell_scient]
    u_shell = Shell_pattern.objects.filter(user=user, basic_id=shell_scient.id).last()
    if u_shell is None:
        koef = element_open(user, shell_scient)

        if koef < 0:
            koef = 0.00001

        upper_scope = 0.33 * koef
        new_shell = random.random()
        if 0 < new_shell < upper_scope:
            shell_pattern = Shell_pattern(
                user=user,
                basic_id=shell_scient.id,
                phisical_damage=shell_scient.phisical_damage,
                speed=shell_scient.speed,
                mass=shell_scient.mass,
                size=shell_scient.size,
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
        shell_atribute = ['phisical_damage', 'speed', 'mass', 'size']
        trying = random.random()
        percent_update = 1 + random.randint(5, 10) / 100.0
        if 0.15 <= trying <= 0.3 or 0.7 <= trying <= 0.85:
            number = random.randint(0, 3)
            atribute = shell_atribute[number]
            element = getattr(u_shell, atribute)
            last_element = getattr(u_shell, atribute)
            element_basic = getattr(shell_scient, atribute)
            if element != 0:
                if number == 2 or number == 3:
                    if element / element_basic > 0.7:
                        percent_update = 1 - random.randint(5, 10) / 100.0
                        element = element * percent_update
                        u_shell.pk = None
                        u_shell.save()
                        u_shell = Shell_pattern.objects.filter(user=user, basic_id=shell_scient.id).last()
                        setattr(u_shell, atribute, element)
                        u_shell.save()
                else:
                    if element_basic / element > 0.7:
                        element = element * percent_update
                        u_shell.pk = None
                        u_shell.save()
                        u_shell = Shell_pattern.objects.filter(user=user, basic_id=shell_scient.id).last()
                        setattr(u_shell, atribute, element)
                        u_shell.save()
            u_shell = Shell_pattern.objects.filter(user=user, basic_id=shell_scient.id).last()
            price_increase(u_shell)


def module_upgrade(request):
    user = request
    b_module = Basic_module.objects.all()
    number_module = len(b_module) - 1
    number_module_scient = random.randint(0, number_module)
    module_scient = b_module[number_module_scient]
    u_module = Module_pattern.objects.filter(user=user, basic_id=module_scient.id).last()
    if u_module is None:
        koef = element_open(user, module_scient)

        if koef < 0:
            koef = 0.00001

        upper_scope = 0.33 * koef
        new_module = random.random()
        user_race = MyUser.objects.filter(user_id=user).first()
        race = user_race.race_id
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
            module_pattern = Module_pattern(
                user=user,
                basic_id=module_scient.id,
                health=module_scient.health,
                param1=module_scient.param1 * module,
                param2=module_scient.param2 * module,
                param3=module_scient.param3 * module,
                mass=module_scient.mass,
                size=module_scient.size,
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
        module_atribute = ['health', 'param1', 'param2', 'param3', 'mass', 'size', 'power_consuption']
        trying = random.random()
        percent_update = 1 + random.randint(5, 10) / 100.0
        if 0.15 <= trying <= 0.3 or 0.7 <= trying <= 0.85:
            number = random.randint(0, 6)
            atribute = module_atribute[number]
            element = getattr(u_module, atribute)
            last_element = getattr(u_module, atribute)
            element_basic = getattr(module_scient, atribute)
            if element != 0:
                if number == 4 or number == 5 or number == 6:
                    if element / element_basic > 0.7:
                        percent_update = 1 - random.randint(5, 10) / 100.0
                        element = element * percent_update
                        u_module.pk = None
                        u_module.save()
                        u_module = Module_pattern.objects.filter(user=user, basic_id=module_scient.id).last()
                        setattr(u_module, atribute, element)
                        u_module.save()
                else:
                    if element_basic / element > 0.7:
                        element = element * percent_update
                        u_module.pk = None
                        u_module.save()
                        u_module = Module_pattern.objects.filter(user=user, basic_id=module_scient.id).last()
                        setattr(u_module, atribute, element)
                        u_module.save()
            u_module = Module_pattern.objects.filter(user=user, basic_id=module_scient.id).last()
            price_increase(u_module)


def element_open(*args):
    user = args[0]
    element_scient = args[1]
    all_base = int(element_scient.min_all_scientic)
    scin_user = User_scientic.objects.filter(user=user).first()
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

    luckyness = MyUser.objects.filter(user_id=user).first()
    lucky = luckyness.user_luckyness
    koef = (1 + (koef_all + koef_math + koef_phis + koef_biol + koef_energy + koef_radio + \
                 koef_nanotech + koef_astronomy + koef_logist)) * (1 + lucky / 100.0)
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
    user = int(new_factory_patt[0])
    prod_class = int(new_factory_patt[1])
    prod_id = int(new_factory_patt[2])
    new_factory = Basic_factory.objects.filter(production_class=prod_class, production_id=prod_id).first()
    user_factory = Factory_pattern(
        user=user,
        basic_id=new_factory.id,
        name=new_factory.name,
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
        size=new_factory.size,
        mass=new_factory.mass,
    )
    user_factory.save()
    return ()