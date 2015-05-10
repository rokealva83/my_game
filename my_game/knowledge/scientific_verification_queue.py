# -*- coding: utf-8 -*-

from django.utils import timezone
from datetime import datetime
from my_game.models import MyUser, User_scientic, Basic_building, Building_pattern
from my_game.models import Turn_scientic
import my_game.knowledge.scientic_func as scientic_func
from my_game.models import User_variables
import random


def check_scientific_verification_queue(request):
    user = int(request)
    time = timezone.now()
    time_update = MyUser.objects.filter(user_id=user).first().last_time_check
    turn_scientics = Turn_scientic.objects.filter(user=user)
    user_variables = User_variables.objects.filter(id=1).first()
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

    if delta_time > user_variables.time_check_new_technology:
        all_scientic = User_scientic.objects.filter(user=user).first()
        if all_scientic.all_scientic > 10:
            new_technology = 0.9 #random.random()

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

            new_device = random.random()
            if 0 < new_device < 1:
                scientic_func.device_open(user)

        last_time_update = time_update
        last_time_scan_scient = datetime(last_time_update.year, last_time_update.month, last_time_update.day, 0, 0, 0,
                                         0)
        MyUser.objects.filter(user_id=user).update(last_time_scan_scient=last_time_scan_scient)

    user_scientic = User_scientic.objects.filter(user=user).first()

    if int(user_scientic.all_scientic) > 50:
        building = Building_pattern.objects.filter(production_class=13).first()
        if building is None:
            building = Basic_building.objects.filter(production_class=13).first()
            building_pattern = Building_pattern(
                name=building.name,
                user=user,
                production_class=13,
                production_id=1,
                time_production=building.time_production,
                warehouse=building.warehouse,
                max_warehouse=building.max_warehouse,
                price_internal_currency=building.price_internal_currency,
                price_resource1=building.price_resource1,
                price_resource2=building.price_resource2,
                price_resource3=building.price_resource3,
                price_resource4=building.price_resource4,
                price_mineral1=building.price_mineral1,
                price_mineral2=building.price_mineral2,
                price_mineral3=building.price_mineral3,
                price_mineral4=building.price_mineral4,
                cost_expert_deployment=building.cost_expert_deployment,
                assembly_workpiece=building.assembly_workpiece,
                time_deployment=building.time_deployment,
                size=building.size,
                mass=building.mass,
                power_consumption=building.power_consumption,
                basic_id = building.id
            )
            building_pattern.save()
