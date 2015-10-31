# -*- coding: utf-8 -*-

from django.utils import timezone
from datetime import datetime
from my_game.models import MyUser, UserScientic, BasicBuilding, BuildingPattern
from my_game.models import TurnScientic
import my_game.knowledge.scientic_func as scientic_func
from my_game.models import UserVariables
import random


def check_scientific_verification_queue(request):
    user = request
    time = timezone.now()
    time_update = user.last_time_check
    turn_scientics = TurnScientic.objects.filter(user=user)
    user_variables = UserVariables.objects.filter(id=1).first()
    if turn_scientics:
        for turn_scientic in turn_scientics:
            scientic_id = turn_scientic.id
            time_start = turn_scientic.start_time_science
            delta_time = time - time_start
            new_delta = delta_time.seconds
            delta_time = turn_scientic.finish_time_science - turn_scientic.start_time_science
            delta = delta_time.seconds
            if new_delta > delta:
                scientic = UserScientic.objects.filter(user=user).first()
                all_scient = scientic.mathematics_up + scientic.phisics_up + scientic.biologic_chimics_up + \
                             scientic.energetics_up + scientic.radionics_up + scientic.nanotech_up + \
                             scientic.astronomy_up + scientic.logistic_up
                user_scientic = UserScientic.objects.filter(user=user).update(
                    mathematics_up=scientic.mathematics_up + turn_scientic.mathematics_up,
                    phisics_up=scientic.phisics_up + turn_scientic.phisics_up,
                    biologic_chimics_up=scientic.biologic_chimics_up + turn_scientic.biologic_chimics_up,
                    energetics_up=scientic.energetics_up + turn_scientic.energetics_up,
                    radionics_up=scientic.radionics_up + turn_scientic.radionics_up,
                    nanotech_up=scientic.nanotech_up + turn_scientic.nanotech_up,
                    astronomy_up=scientic.astronomy_up + turn_scientic.astronomy_up,
                    logistic_up=scientic.logistic_up + turn_scientic.logistic_up,
                )
                TurnScientic.objects.filter(id=scientic_id).delete()
                user_scientic = UserScientic.objects.filter(user=user).first()
                all_scient = user_scientic.mathematics_up + user_scientic.phisics_up + user_scientic.biologic_chimics_up + \
                             user_scientic.energetics_up + user_scientic.radionics_up + user_scientic.nanotech_up + \
                             user_scientic.astronomy_up + user_scientic.logistic_up
                user_scientic = UserScientic.objects.filter(user=user).update(all_scientic=all_scient)

    # the addition of new technology
    table_scan_time = user.last_time_scan_scient
    delta = time - table_scan_time
    delta_time = delta.seconds

    if delta_time > user_variables.time_check_new_technology:
        user_scientic = UserScientic.objects.filter(user=user).first()
        if user_scientic.all_scientic > 10:
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

            new_device = random.random()
            if 0 < new_device < 1:
                scientic_func.device_open(user)

        last_time_update = time_update
        last_time_scan_scient = datetime(last_time_update.year, last_time_update.month, last_time_update.day, 0, 0, 0,
                                         0)
        MyUser.objects.filter(user=user).update(last_time_scan_scient=last_time_scan_scient)

    user_scientic = UserScientic.objects.filter(user=user).first()

    if int(user_scientic.all_scientic) > 50:
        building = BuildingPattern.objects.filter(production_class=13).first()
        if building is None:
            building = BasicBuilding.objects.filter(production_class=13).first()
            building_pattern = BuildingPattern(
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
                building_size=building.size,
                building_mass=building.mass,
                power_consumption=building.power_consumption,
                basic_building=building
            )
            building_pattern.save()
