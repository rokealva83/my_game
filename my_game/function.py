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
import verification_func
import Global_variables


def check_all_queues(request):
    user = int(request)
    verification_func.check_scientific_verification_queue(user)
    verification_func.verification_phase_of_construction(user)
    now_date = timezone.now()
    time_update = MyUser.objects.filter(user_id=user).first().last_time_check
    elapsed_time_full = now_date - time_update
    elapsed_time_seconds = elapsed_time_full.seconds
    time_update = now_date
    if elapsed_time_seconds > 300:
        verification_func.verification_of_resources(user, elapsed_time_seconds, time_update)
    verification_func.check_assembly_line_workpieces(user)
    verification_func.verification_stage_production(user)


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
        install_factory = Warehouse_factory.objects.filter(user = session_user, factory_id = pattern_id).first()
        new_amount = install_factory.amount - 1
        install_factory = Warehouse_factory.objects.filter(user = session_user, factory_id = pattern_id).update(amount = new_amount)
        if factory_pattern.production_class != 10:
            user_city = User_city.objects.filter(user=session_user, id = session_user_city).first()
            new_population = user_city.population - factory_pattern.cost_expert_deployment
            user_city = User_city.objects.filter(id=user_city.id).update(population=new_population)
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
    return (message)

