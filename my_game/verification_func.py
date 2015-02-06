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
import scientic_func


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
                scientic_func.hull_upgrade(user)

            if 0.125 <= new_technology < 0.250:
                scientic_func.armor_upgrade(user)

            if 0.250 <= new_technology < 0.375:
                scientic_func.shield_upgrade(user)

            if 0.375 <= new_technology < 0.5:
                scientic_func.engine_upgrade(user)

            if 0.5 <= new_technology < 0.625:
                scientic_func.generator_upgrade(user)

            if 0.625 <= new_technology < 0.750:
                scientic_func.weapon_upgrade(user)

            if 0.750 <= new_technology < 0.875:
                scientic_func.shell_upgrade(user)

            if 0.875 <= new_technology <= 1:
                scientic_func.module_upgrade(user)


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
            else:
                user_city = User_city.objects.filter(user=user, id=turn_building.user_city).first()
                new_population = user_city.population - factory_pattern.cost_expert_deployment
                user_city = User_city.objects.filter(id=user_city.id).update(population=new_population)

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
                    warehouse = Warehouse_element.objects.filter(element_id = turn_production.element_id).update(amount = new_amount)
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
