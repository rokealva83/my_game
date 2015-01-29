# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.template import Context
import math
import random
import sys
import string
from datetime import datetime, timedelta, date, time as dt_time
import time
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.contrib.sessions.models import Session
from django.utils import timezone
from models import Galaxy, System, Planet
from models import MyUser, User_city, Race, User_scientic
from models import Warehouse
from models import Basic_scientic, Turn_scientic, Basic_armor, Basic_engine, Basic_factory, Basic_generator, \
    Basic_hull, Basic_module, Basic_shell, Basic_shield, Basic_weapon, Turn_building, Turn_assembly_pieces, \
    Turn_production
from models import Hull_pattern, Shell_pattern, Shield_pattern, Generator_pattern, Engine_pattern, \
    Armor_pattern, Module_pattern, Factory_pattern, Weapon_pattern, Factory_installed
from models import Warehouse_factory, Warehouse_element, Warehouse_ship, Warehouse


def check_all_queues(request):
    user = int(request)
    check_scientific_verification_queue(user)
    verification_phase_of_construction(user)
    now_date = timezone.now()
    time_update = MyUser.objects.filter(user_id=user).first().last_time_check
    elapsed_time_full = now_date - time_update
    elapsed_time_seconds = elapsed_time_full.seconds
    time_update = now_date
    if elapsed_time_seconds > 300:
        verification_of_resources(user, elapsed_time_seconds, time_update)
    check_assembly_line_workpieces(user)
    verification_stage_production(user)



def check_scientific_verification_queue(request):
    user = int(request)
    time = timezone.now()
    turn_scientics = Turn_scientic.objects.filter(user=user)
    if turn_scientics:
        for turn_scientic in turn_scientics:
            scin_id = turn_scientic.id
            time_start = turn_scientic.start_time_science
            delta_time = time - time_start
            new_delta = delta_time.seconds
            delta_time = turn_scientic.finish_time_science - turn_scientic.start_time_science
            delta = delta_time.seconds
            if new_delta > delta:
                scientic = User_scientic.objects.filter(user=user).first()
                all_scient = scientic.mathematics_up + scientic.phisics_up + scientic.biologic_chimics_up + \
                             scientic.energetics_up + scientic.radionics_up + scientic.nanotech_up + \
                             scientic.astronomy_up + scientic.logistic_up
                user_scientic = User_scientic.objects.filter(user=user).update(
                    mathematics_up=scientic.mathematics_up + turn_scientic.mathematics_up,
                    phisics_up=scientic.phisics_up + turn_scientic.phisics_up,
                    biologic_chimics_up=scientic.biologic_chimics_up + turn_scientic.biologic_chimics_up,
                    energetics_up=scientic.energetics_up + turn_scientic.energetics_up,
                    radionics_up=scientic.radionics_up + turn_scientic.radionics_up,
                    nanotech_up=scientic.nanotech_up + turn_scientic.nanotech_up,
                    astronomy_up=scientic.astronomy_up + turn_scientic.astronomy_up,
                    logistic_up=scientic.logistic_up + turn_scientic.logistic_up,
                )
                Turn_scientic.objects.filter(id=scin_id).delete()
                user_scientic = User_scientic.objects.filter(user=user).first()
                all_scient = user_scientic.mathematics_up + user_scientic.phisics_up + user_scientic.biologic_chimics_up + \
                             user_scientic.energetics_up + user_scientic.radionics_up + user_scientic.nanotech_up + \
                             user_scientic.astronomy_up + user_scientic.logistic_up
                user_scientic = User_scientic.objects.filter(user=user).update(all_scientic=all_scient)

    # the addition of new technology
    my_user = MyUser.objects.filter(user_id=user).first()
    table_scan_time = my_user.last_time_scan_scient
    delta = time - table_scan_time
    delta_time = delta.seconds

    if delta_time > 86400:
        all_scientic = User_scientic.objects.filter(user=user).first()
        if all_scientic.all_scientic > 10:
            new_technology = random.random()

            if 0 <= new_technology < 0.125:
                hull_upgrade(user)

            if 0.125 <= new_technology < 0.250:
                armor_upgrade(user)

            if 0.250 <= new_technology < 0.375:
                shield_upgrade(user)

            if 0.375 <= new_technology < 0.5:
                engine_upgrade(user)

            if 0.5 <= new_technology < 0.625:
                generator_upgrade(user)

            if 0.625 <= new_technology < 0.750:
                weapon_upgrade(user)

            if 0.750 <= new_technology < 0.875:
                shell_upgrade(user)

            if 0.875 <= new_technology <= 1:
                module_upgrade(user)


def verification_phase_of_construction(request):
    user = int(request)
    my_user = MyUser.objects.filter(user_id=user).first()
    turn_buildings = Turn_building.objects.filter(user=user)
    time = timezone.now()
    for turn_building in turn_buildings:
        time_start = turn_building.start_time_deployment
        delta_time = time - time_start
        new_delta = delta_time.seconds
        delta_time = turn_building.finish_time_deployment - turn_building.start_time_deployment
        delta = delta_time.seconds
        user_city = User_city.objects.filter(user=user, id=turn_building.user_city).first()
        if new_delta > delta:
            elapsed_time = turn_building.finish_time_deployment - my_user.last_time_check
            elapsed_time_seconds = elapsed_time.seconds
            time_update = turn_building.finish_time_deployment
            verification_of_resources(user, elapsed_time_seconds, time_update)
            factory_pattern = Factory_pattern.objects.filter(id=turn_building.factory_id).first()

            factory_installed = Factory_installed(
                user=user,
                user_city=user_city.id,
                factory_pattern_id=turn_building.factory_id,
                name=factory_pattern.name,
                time_deployment=factory_pattern.time_deployment,
                production_class=factory_pattern.production_class,
                production_id=factory_pattern.production_id,
                time_production=factory_pattern.time_production,
                size=factory_pattern.size,
                mass=factory_pattern.mass,
                power_consumption=factory_pattern.power_consumption,
            )
            factory_installed.save()
            if factory_pattern.production_class == 12:
                new_power = user_city.power + factory_installed.power_consumption
                user_city = User_city.objects.filter(id=user_city.id).update(power=new_power)
            else:
                new_energy = user_city.use_energy + factory_installed.power_consumption
                user_city = User_city.objects.filter(id=user_city.id).update(use_energy=new_energy)

            if factory_pattern.production_class == 10:
                user_city = User_city.objects.filter(user=user, id=turn_building.user_city).first()
                new_max_population = user_city.max_population + 100 * factory_pattern.production_id
                user_city = User_city.objects.filter(id=user_city.id).update(max_population=new_max_population)
            turn_building = Turn_building.objects.filter(id=turn_building.id).delete()


def verification_of_resources(*args):
    arg = args
    user = arg[0]
    elapsed_time_seconds = arg[1]
    time_update = arg[2]
    tax = 0.01
    user_citys = User_city.objects.filter(user=user)
    for user_city in user_citys:
        city_id = user_city.id
        check_user_factory_resourse_city = Factory_installed.objects.filter(user=user, user_city=city_id,
                                                                            production_class=11)
        attributes = ['resource1', 'resource2', 'resource3', 'resource4', 'mineral1', 'mineral2', 'mineral3',
                      'mineral4']
        prod_id = 1
        warehouse = Warehouse.objects.filter(user=user, user_city=city_id).first()
        for attribute in attributes:
            check_factorys = check_user_factory_resourse_city.filter(production_id=prod_id)
            resourse = 0
            for check_factory in check_factorys:
                resourse = resourse + elapsed_time_seconds / check_factory.time_production
            new_resourse = getattr(warehouse, attribute) + resourse
            prod_id = prod_id + 1
            setattr(warehouse, attribute, new_resourse)
            warehouse.save()
        population = 0
        population_buildings = Factory_installed.objects.filter(user=user, user_city=city_id, production_class=10)
        for population_building in population_buildings:
            population = population + elapsed_time_seconds / population_building.time_production

        new_population = user_city.population + population
        if new_population > user_city.max_population:
            new_population = user_city.max_population
        user_city = User_city.objects.filter(id=city_id).update(population=new_population)

        check_all_user_factorys = Factory_installed.objects.filter(user=user, user_city=city_id)
        total_number_specialists = 0
        for check_all_user_factory in check_all_user_factorys:
            install_factory = Factory_pattern.objects.filter(id=check_all_user_factory.factory_pattern_id).first()
            total_number_specialists = total_number_specialists + install_factory.cost_expert_deployment
        increase_internal_currency = total_number_specialists * elapsed_time_seconds * tax
        new_internal_currency = MyUser.objects.get(user_id=user).internal_currency + increase_internal_currency
        money = MyUser.objects.filter(user_id=user).update(internal_currency=new_internal_currency)

    last_time_update = time_update
    last_time_scan_scient = datetime(last_time_update.year, last_time_update.month, last_time_update.day, 0, 0, 0,
                                     0)
    MyUser.objects.filter(user_id=user).update(last_time_check=last_time_update,
                                               last_time_scan_scient=last_time_scan_scient)


def check_assembly_line_workpieces(request):
    user = int(request)
    my_user = MyUser.objects.filter(user_id=user).first()
    turn_assembly_piecess = Turn_assembly_pieces.objects.filter(user=user)
    time = timezone.now()
    for turn_assembly_pieces in turn_assembly_piecess:
        time_start = turn_assembly_pieces.start_time_assembly
        delta_time = time - time_start
        new_delta = delta_time.seconds
        delta_time = turn_assembly_pieces.finish_time_assembly - turn_assembly_pieces.start_time_assembly
        delta = delta_time.seconds
        user_city = User_city.objects.filter(user=user, id=turn_assembly_pieces.user_city).first()
        warehouse_factory = Warehouse_factory.objects.filter(factory_id=turn_assembly_pieces.pattern_id).first()
        if new_delta > delta:
            if warehouse_factory is not None:
                amount_assembly = turn_assembly_pieces.amount_assembly + warehouse_factory.amount
                warehouse_factory = Warehouse_factory.objects.filter(factory_id=turn_assembly_pieces.pattern_id).update(
                    amount=amount_assembly)
            else:
                factory_pattern = Factory_pattern.objects.filter(id=turn_assembly_pieces.pattern_id).first()
                new_factory = Warehouse_factory(
                    user=turn_assembly_pieces.user,
                    user_city=turn_assembly_pieces.user_city,
                    factory_id=turn_assembly_pieces.pattern_id,
                    production_class=factory_pattern.production_class,
                    production_id=factory_pattern.production_id,
                    time_production=factory_pattern.time_production,
                    amount=turn_assembly_pieces.amount_assembly,
                    size=factory_pattern.size,
                    mass=factory_pattern.mass,
                    power_consumption=factory_pattern.power_consumption
                )
                new_factory.save()
            end_turn_assembly_pieces = Turn_assembly_pieces.objects.filter(id=turn_assembly_pieces.id).delete()


def verification_stage_production(request):
    user = request
    user_citys = User_city.objects.filter(user = user)
    for user_city in user_citys:
        city_id = user_city.id
        turn_productions = Turn_production.objects.filter(user = user, user_city = user_city.id).order_by('start_time_production')
        for turn_production in turn_productions:
            time = timezone.now()
            time_start = turn_production.start_time_production
            delta_time = time - time_start
            new_delta = delta_time.seconds
            delta_time = turn_production.finish_time_production - turn_production.start_time_production
            delta = delta_time.seconds
            if new_delta > delta:
                work_factory = Factory_installed.objects.filter(id = turn_production.factory_id).first()
                warehouse = Warehouse_element.objects.filter(element_id = turn_production.element_id).first()
                if warehouse is not None:
                    new_amount = warehouse.amount + turn_production.amount_element
                    warehouse = Warehouse_element.objects.filter(hull_id = turn_production.element_id).update(amount = new_amount)
                else:
                    warehouse = Warehouse_element(
                        user = user,
                        user_city = user_city.id,
                        element_class = work_factory.production_class,
                        element_id = turn_production.element_id,
                        amount = turn_production.amount_element
                    )
                    warehouse.save()
                turn_production_delete = Turn_production.objects.filter(id = turn_production.id).delete()


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
                generators=hull_scient.generators,
                engines=hull_scient.engines,
                weapons=hull_scient.weapons,
                armor=hull_scient.armor,
                shield=hull_scient.shield,
                modules=hull_scient.modules,
                main_weapons=hull_scient.main_weapons,
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
        hull_atribute = ['health', 'generators', 'engines', 'weapons', 'armor', 'shield', 'modules', \
                         'main_weapons', 'hold_size', 'mass', 'size', 'power_consuption']
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


def rename_factory_pattern(*args):
    new_name = args[0]
    pattern_id = args[1]
    name_factory = Factory_pattern.objects.filter(id=pattern_id).update(name=new_name)
    message = 'Шаблон переименован'
    return (message)


def upgrade_factory_pattern(*args):
    pattern_id = int(args[2])
    old_pattern = Factory_pattern.objects.filter(id=pattern_id).first()
    number = int(args[0])
    if old_pattern.production_class == 12:
        speed = 1
    else:
        speed = int(args[1])

    if speed == 1:
        koef_speed = 1
    else:
        koef_speed = int(speed) * 1.6

    if number == 1:
        koef_number = 1
    else:
        koef_number = int(number) * 1.6

    old_pattern = Factory_pattern.objects.filter(id=pattern_id).first()
    new_pattern = Factory_pattern(
        user=old_pattern.user,
        basic_id=old_pattern.basic_id,
        name=old_pattern.name,
        price_internal_currency=old_pattern.price_internal_currency * koef_speed * koef_number,
        price_resource1=old_pattern.price_resource1 * koef_speed * koef_number,
        price_resource2=old_pattern.price_resource2 * koef_speed * koef_number,
        price_resource3=old_pattern.price_resource3 * koef_speed * koef_number,
        price_resource4=old_pattern.price_resource4 * koef_speed * koef_number,
        price_mineral1=old_pattern.price_mineral1 * koef_speed * koef_number,
        price_mineral2=old_pattern.price_mineral2 * koef_speed * koef_number,
        price_mineral3=old_pattern.price_mineral3 * koef_speed * koef_number,
        price_mineral4=old_pattern.price_mineral4 * koef_speed * koef_number,
        cost_expert_deployment=old_pattern.cost_expert_deployment * koef_speed * koef_number,
        assembly_workpiece=old_pattern.assembly_workpiece * koef_speed * koef_number,
        time_deployment=old_pattern.time_deployment * koef_speed * koef_number,
        production_class=old_pattern.production_class,
        production_id=old_pattern.production_id,
        time_production=old_pattern.time_production / (speed * number),
        size=old_pattern.size * koef_speed * koef_number / 3,
        mass=old_pattern.mass * koef_speed * koef_number / 3,
        power_consumption=old_pattern.power_consumption * koef_speed * koef_number / 3,
    )
    new_pattern.save()
    new_pattern_id = new_pattern.pk
    if new_pattern.production_class == 12:
        old_pattern_power = old_pattern.power_consumption
        new_power_consumption = old_pattern_power * number
        new_pattern = Factory_pattern.objects.filter(id=new_pattern_id).update(power_consumption=new_power_consumption)
    message = 'Шаблон улучшен'
    return (message)


def delete_factory_pattern(*args):
    pattern_id = int(args[0])
    factory = Factory_installed.objects.filter(factory_pattern_id=pattern_id)
    if factory is not None:
        message = 'Шаблон не может быть удален'
    else:
        delete_pattern = Factory_pattern.objects.filter(id=pattern_id).delete()
        message = 'Шаблон удален'
    return (message)


def making_factory_unit(*args):
    session_user = int(args[0])
    session_user_city = int(args[1])
    amount_factory_unit = int(args[2])
    pattern_id = int(args[3])
    user = MyUser.objects.filter(user_id=session_user).first()
    warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).first()
    factory_pattern_making = Factory_pattern.objects.filter(id=pattern_id).first()
    turn_assembly_pieces = len(Turn_assembly_pieces.objects.filter(user=session_user, user_city=session_user_city))

    if turn_assembly_pieces < 3:
        if user.internal_currency >= factory_pattern_making.price_internal_currency and \
                        warehouse.resource1 >= factory_pattern_making.price_resource1 and \
                        warehouse.resource2 >= factory_pattern_making.price_resource2 and \
                        warehouse.resource3 >= factory_pattern_making.price_resource3 and \
                        warehouse.resource4 >= factory_pattern_making.price_resource4 and \
                        warehouse.mineral1 >= factory_pattern_making.price_mineral1 and \
                        warehouse.mineral2 >= factory_pattern_making.price_mineral2 and \
                        warehouse.mineral3 >= factory_pattern_making.price_mineral3 and \
                        warehouse.mineral4 >= factory_pattern_making.price_mineral4:

            new_internal_currency = user.internal_currency - factory_pattern_making.price_internal_currency
            new_resource1 = warehouse.resource1 - factory_pattern_making.price_resource1
            new_resource2 = warehouse.resource2 - factory_pattern_making.price_resource1
            new_resource3 = warehouse.resource3 - factory_pattern_making.price_resource1
            new_resource4 = warehouse.resource4 - factory_pattern_making.price_resource1
            new_mineral1 = warehouse.mineral1 - factory_pattern_making.price_mineral1
            new_mineral2 = warehouse.mineral2 - factory_pattern_making.price_mineral1
            new_mineral3 = warehouse.mineral3 - factory_pattern_making.price_mineral1
            new_mineral4 = warehouse.mineral4 - factory_pattern_making.price_mineral1

            warehouse = Warehouse.objects.filter(user=session_user).update(resource1=new_resource1, \
                                                                           resource2=new_resource2, \
                                                                           resource3=new_resource3, \
                                                                           resource4=new_resource4, \
                                                                           mineral1=new_mineral1, \
                                                                           mineral2=new_mineral2, \
                                                                           mineral3=new_mineral3, \
                                                                           mineral4=new_mineral4)
            user = MyUser.objects.filter(user_id=session_user).update(internal_currency=new_internal_currency)
            turn_assembly_piece = Turn_assembly_pieces.objects.filter(user=session_user,
                                                                      user_city=session_user_city).last()
            if turn_assembly_piece is not None:
                start_making = turn_assembly_piece.finish_time_assembly
            else:
                start_making = datetime.now()
            build_time = factory_pattern_making.assembly_workpiece * amount_factory_unit
            finish_making = start_making + timedelta(seconds=build_time)
            turn_assembly_pieces = Turn_assembly_pieces(
                user=session_user,
                user_city=session_user_city,
                pattern_id=pattern_id,
                start_time_assembly=start_making,
                finish_time_assembly=finish_making,
                amount_assembly=amount_factory_unit
            )
            turn_assembly_pieces.save()
            message = 'Производство заготовки начато'
        else:
            message = 'Нехватает ресурсов'
    else:
        message = 'Очередь заполнена'
    return (message)


def install_factory_unit(*args):
    session_user = args[0]
    session_user_city = args[1]
    pattern_id = args[2]
    user_city = User_city.objects.filter(id=session_user_city).first()
    factory_pattern = Factory_pattern.objects.filter(id=pattern_id).first()
    free_energy = user_city.power - user_city.use_energy
    len_turn_building = len(Turn_building.objects.filter(user=session_user, user_city=session_user_city))
    if len_turn_building < 3:
        power_consumption = factory_pattern.power_consumption
        if factory_pattern.cost_expert_deployment < user_city.population and free_energy > power_consumption:
            last_building = Turn_building.objects.filter(user=session_user, user_city=session_user_city).last()
            if last_building is not None:
                start_time = last_building.finish_time_deployment
            else:
                start_time = datetime.now()

            finish_time = start_time + timedelta(seconds=factory_pattern.time_deployment)
            turn_building = Turn_building(
                user=session_user,
                user_city=session_user_city,
                factory_id=pattern_id,
                x=user_city.x,
                y=user_city.y,
                z=user_city.z,
                start_time_deployment=start_time,
                finish_time_deployment=finish_time,
            )
        turn_building.save()
        new_warehouse_factory = Warehouse_factory.objects.filter(factory_id=pattern_id).first()
        message = 'Развертывание начато'
    else:
        message = 'Очередь заполнена'
    return (message)


def rename_element_pattern(*args):
    session_user = args[0]
    session_user_city = args[1]
    pattern_id = args[2]
    element_id = args[3]
    new_name = args[4]
    factory = Factory_installed.objects.filter(id=pattern_id).first()
    production_class = factory.production_class
    if production_class == 1:
        new_name = Hull_pattern.objects.filter(id=element_id).update(name=new_name)
    if production_class == 2:
        new_name = Armor_pattern.objects.filter(id=element_id).update(name=new_name)
    if production_class == 3:
        new_name = Shield_pattern.objects.filter(id=element_id).update(name=new_name)
    if production_class == 4:
        new_name = Engine_pattern.objects.filter(id=element_id).update(name=new_name)
    if production_class == 5:
        new_name = Generator_pattern.objects.filter(id=element_id).update(name=new_name)
    if production_class == 6:
        new_name = Weapon_pattern.objects.filter(id=element_id).update(name=new_name)
    if production_class == 7:
        new_name = Shell_pattern.objects.filter(id=element_id).update(name=new_name)
    if production_class == 8:
        new_name = Module_pattern.objects.filter(id=element_id).update(name=new_name)
        # if production_class == 9:
    # new_name = Device_pattern.objects.filter(id = element_id).update(name = new_name)
    message = 'Модуль переименован'
    return (message)


def production_module(*args):
    session_user = args[0]
    session_user_city = args[1]
    factory_id = args[2]
    element_id = args[3]
    amount_element = args[4]

    user = MyUser.objects.filter(user_id=session_user).first()
    warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).first()
    factory_worker = Factory_installed.objects.filter(id=factory_id).first()
    len_turn_production = len(Turn_production.objects.filter(user=session_user, user_city=session_user_city, \
                                                             factory_id=factory_worker.id))
    if len_turn_production < 1:
        if factory_worker.production_class == 1:
            module_which_produces = Hull_pattern.objects.filter(id=element_id).first()
        if factory_worker.production_class == 2:
            module_which_produces = Armor_pattern.objects.filter(id=element_id).first()
        if factory_worker.production_class == 3:
            module_which_produces = Shield_pattern.objects.filter(id=element_id).first()
        if factory_worker.production_class == 4:
            module_which_produces = Engine_pattern.objects.filter(id=element_id).first()
        if factory_worker.production_class == 5:
            module_which_produces = Generator_pattern.objects.filter(id=element_id).first()
        if factory_worker.production_class == 6:
            module_which_produces = Weapon_pattern.objects.filter(id=element_id).first()
        if factory_worker.production_class == 7:
            module_which_produces = Shell_pattern.objects.filter(id=element_id).first()
        if factory_worker.production_class == 8:
            module_which_produces = Module_pattern.objects.filter(id=element_id).first()
#        if factory_worker.production_class == 9:
#            module_which_produces = Device_pattern.objects.filter(id=element_id).first()



        if user.internal_currency >= module_which_produces.price_internal_currency * int(amount_element) and \
                        warehouse.resource1 >= module_which_produces.price_resource1 * int(amount_element) and \
                        warehouse.resource2 >= module_which_produces.price_resource2 * int(amount_element) and \
                        warehouse.resource3 >= module_which_produces.price_resource3 * int(amount_element) and \
                        warehouse.resource4 >= module_which_produces.price_resource4 * int(amount_element) and \
                        warehouse.mineral1 >= module_which_produces.price_mineral1 * int(amount_element) and \
                        warehouse.mineral2 >= module_which_produces.price_mineral2 * int(amount_element) and \
                        warehouse.mineral3 >= module_which_produces.price_mineral3 * int(amount_element) and \
                        warehouse.mineral4 >= module_which_produces.price_mineral4 * int(amount_element):

            new_internal_currency = user.internal_currency - module_which_produces.price_internal_currency * int(amount_element)
            new_resource1 = warehouse.resource1 - module_which_produces.price_resource1 * int(amount_element)
            new_resource2 = warehouse.resource2 - module_which_produces.price_resource1 * int(amount_element)
            new_resource3 = warehouse.resource3 - module_which_produces.price_resource1 * int(amount_element)
            new_resource4 = warehouse.resource4 - module_which_produces.price_resource1 * int(amount_element)
            new_mineral1 = warehouse.mineral1 - module_which_produces.price_mineral1 * int(amount_element)
            new_mineral2 = warehouse.mineral2 - module_which_produces.price_mineral1 * int(amount_element)
            new_mineral3 = warehouse.mineral3 - module_which_produces.price_mineral1 * int(amount_element)
            new_mineral4 = warehouse.mineral4 - module_which_produces.price_mineral1 *int(amount_element)

            warehouse = Warehouse.objects.filter(user=session_user).update(resource1=new_resource1, \
                                                                           resource2=new_resource2, \
                                                                           resource3=new_resource3, \
                                                                           resource4=new_resource4, \
                                                                           mineral1=new_mineral1, \
                                                                           mineral2=new_mineral2, \
                                                                           mineral3=new_mineral3, \
                                                                           mineral4=new_mineral4)
            user = MyUser.objects.filter(user_id=session_user).update(internal_currency=new_internal_currency)
            turn_productions = Turn_production.objects.filter(user=session_user, user_city=session_user_city,
                                                              factory_id=factory_id).last()
            if turn_productions is not None:
                start_making = turn_productions.finish_time_production
            else:
                start_making = datetime.now()
            build_time = factory_worker.time_production * int(amount_element)
            finish_making = start_making + timedelta(seconds=build_time)
            turn_production = Turn_production(
                user=session_user,
                user_city=session_user_city,
                factory_id=factory_id,
                element_id=element_id,
                start_time_production=start_making,
                finish_time_production=finish_making,
                amount_element=amount_element
            )
            turn_production.save()
            message = 'Производство начато'
        else:
            message = 'Нехватает ресурсов'
    else:
        message = 'Очередь завода занята'


