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
from django.conf import settings
from django.conf.urls.static import static
from models import Galaxy, System, Planet, MyUser, User_city, Warehouse, Race, User_scientic, Basic_scientic, \
    Turn_scientic, Turn_production, Turn_building, Turn_assembly_pieces
from models import Basic_scientic, Turn_scientic, Basic_armor, Basic_engine, Basic_factory, Basic_generator, \
    Basic_hull, Basic_module, Basic_shell, Basic_shield, Basic_weapon
from models import Hull_pattern, Shell_pattern, Shield_pattern, Generator_pattern, Engine_pattern, \
    Armor_pattern, Module_pattern, Factory_pattern, Weapon_pattern, Factory_installed
from models import Warehouse_factory, Warehouse_element, Warehouse_ship
import function
from models import Project_ship, Element_ship, Ship
import Global_variables



def scien_up(*args):
    session_user = args[0]
    level_up = int(args[1])
    scientic = int(args[2])
    number_scientic = len(Turn_scientic.objects.filter(user=session_user))
    if number_scientic < 3:
        warehouse = Warehouse.objects.filter(user=session_user).first()

        scien = Basic_scientic.objects.get(scientic_id=scientic)
        time_studys = int(scien.time_study)
        if level_up == 1:
            time_study_turn = time_studys
            cost_study_resource1 = int(scien.cost_resource1)
            cost_study_resource2 = int(scien.cost_resource2)
            cost_study_resource3 = int(scien.cost_resource3)
            cost_study_resource4 = int(scien.cost_resource4)
            cost_study_mineral1 = int(scien.cost_mineral1)
            cost_study_mineral2 = int(scien.cost_mineral2)
            cost_study_mineral3 = int(scien.cost_mineral3)
            cost_study_mineral4 = int(scien.cost_mineral4)
        else:
            time_study_turn = int(time_studys * int(math.exp(level_up) / 5))
            cost_study_resource1 = int(scien.cost_resource1 * math.exp(level_up) / 5)
            cost_study_resource2 = int(scien.cost_resource2 * math.exp(level_up) / 5)
            cost_study_resource3 = int(scien.cost_resource3 * math.exp(level_up) / 5)
            cost_study_resource4 = int(scien.cost_resource4 * math.exp(level_up) / 5)
            cost_study_mineral1 = int(scien.cost_mineral1 * math.exp(level_up) / 5)
            cost_study_mineral2 = int(scien.cost_mineral2 * math.exp(level_up) / 5)
            cost_study_mineral3 = int(scien.cost_mineral3 * math.exp(level_up) / 5)
            cost_study_mineral4 = int(scien.cost_mineral4 * math.exp(level_up) / 5)

        if warehouse.resource1 >= cost_study_resource1 and warehouse.resource2 >= cost_study_resource2 and \
                        warehouse.resource3 >= cost_study_resource3 and warehouse.resource4 >= cost_study_resource4 and \
                        warehouse.mineral1 >= cost_study_mineral1 and warehouse.mineral2 >= cost_study_mineral2 and \
                        warehouse.mineral3 >= cost_study_mineral3 and warehouse.mineral4 >= cost_study_mineral4:
            new_resource1 = warehouse.resource1 - cost_study_resource1
            new_resource2 = warehouse.resource2 - cost_study_resource2
            new_resource3 = warehouse.resource3 - cost_study_resource3
            new_resource4 = warehouse.resource4 - cost_study_resource4
            new_mineral1 = warehouse.mineral1 - cost_study_mineral1
            new_mineral2 = warehouse.mineral2 - cost_study_mineral2
            new_mineral3 = warehouse.mineral3 - cost_study_mineral3
            new_mineral4 = warehouse.mineral4 - cost_study_mineral4
            warehouse = Warehouse.objects.filter(user=session_user).update(resource1=new_resource1, \
                                                                           resource2=new_resource2, \
                                                                           resource3=new_resource3, \
                                                                           resource4=new_resource4, \
                                                                           mineral1=new_mineral1, \
                                                                           mineral2=new_mineral2, \
                                                                           mineral3=new_mineral3, \
                                                                           mineral4=new_mineral4)

            turn_scientic = Turn_scientic.objects.filter(user=session_user).last()
            if turn_scientic:
                finish_time = turn_scientic.finish_time_science + timedelta(seconds=time_study_turn)
            else:
                finish_time = datetime.now() + timedelta(seconds=time_study_turn)

            if scientic == 1:
                turn_scientic = Turn_scientic(
                    user=session_user,
                    mathematics_up=level_up,
                    start_time_science=datetime.now(),
                    finish_time_science=finish_time,
                )
            if scientic == 2:
                turn_scientic = Turn_scientic(
                    user=session_user,
                    phisics_up=level_up,
                    start_time_science=datetime.now(),
                    finish_time_science=finish_time,
                )
            if scientic == 3:
                turn_scientic = Turn_scientic(
                    user=session_user,
                    biologic_chimics_up=level_up,
                    start_time_science=datetime.now(),
                    finish_time_science=finish_time,
                )
            if scientic == 4:
                turn_scientic = Turn_scientic(
                    user=session_user,
                    energetics_up=level_up,
                    start_time_science=datetime.now(),
                    finish_time_science=finish_time,
                )
            if scientic == 5:
                turn_scientic = Turn_scientic(
                    user=session_user,
                    radionics_up=level_up,
                    start_time_science=datetime.now(),
                    finish_time_science=finish_time,
                )
            if scientic == 6:
                turn_scientic = Turn_scientic(
                    user=session_user,
                    nanotech_up=level_up,
                    start_time_science=datetime.now(),
                    finish_time_science=finish_time,
                )
            if scientic == 7:
                turn_scientic = Turn_scientic(
                    user=session_user,
                    astronomy_up=level_up,
                    start_time_science=datetime.now(),
                    finish_time_science=finish_time,
                )
            if scientic == 8:
                turn_scientic = Turn_scientic(
                    user=session_user,
                    logistic_up=level_up,
                    start_time_science=datetime.now(),
                    finish_time_science=finish_time,
                )
            turn_scientic.save()
