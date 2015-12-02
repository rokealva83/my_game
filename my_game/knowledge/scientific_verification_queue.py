# -*- coding: utf-8 -*-

from django.utils import timezone
from datetime import datetime
from my_game.models import MyUser, UserScientic, BasicBuilding, BuildingPattern
from my_game.models import TurnScientic
from my_game.models import UserVariables
import random
from my_game.knowledge.armor_upgrade import armor_upgrade
from my_game.knowledge.engine_upgrade import engine_upgrade
from my_game.knowledge.weapon_upgrade import weapon_upgrade
from my_game.knowledge.module_upgrade import module_upgrade
from my_game.knowledge.shell_upgrade import shell_upgrade
from my_game.knowledge.shield_upgrade import shield_upgrade
from my_game.knowledge.hull_upgrade import hull_upgrade
from my_game.knowledge.generator_upgrade import generator_upgrade
from my_game.knowledge.device_open import device_open



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
                UserScientic.objects.filter(user=user).update(
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
                science_users = UserScientic.objects.filter(user=user).first()
                all_scient = science_users.mathematics_up + science_users.phisics_up + \
                             science_users.biologic_chimics_up + science_users.energetics_up + \
                             science_users.radionics_up + science_users.nanotech_up + science_users.astronomy_up + \
                             science_users.logistic_up
                UserScientic.objects.filter(user=user).update(all_scientic=all_scient)
    # the addition of new technology
    table_scan_time = user.last_time_scan_scient
    delta = time - table_scan_time
    delta_time = delta.seconds
    if delta_time > user_variables.time_check_new_technology:
        science_users = UserScientic.objects.filter(user=user).first()
        if science_users.all_scientic > user_variables.min_scientic_level:
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
            new_device = random.random()
            if 0 < new_device < 1:
                device_open(user)
        last_time_update = time_update
        last_time_scan_scient = datetime(last_time_update.year, last_time_update.month, last_time_update.day, 0, 0, 0,
                                         0)
        MyUser.objects.filter(id=user.id).update(last_time_scan_scient=last_time_scan_scient)
    science_users = UserScientic.objects.filter(user=user).first()
    if int(science_users.all_scientic) > 100:
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
                price_nickel=building.price_nickel,
                price_iron=building.price_iron,
                price_cooper=building.price_cooper,
                price_aluminum=building.price_aluminum,
                price_veriarit=building.price_veriarit,
                price_inneilit=building.price_inneilit,
                price_renniit=building.price_renniit,
                price_cobalt=building.price_cobalt,
                price_construction_material=building.price_construction_material,
                price_chemical=building.price_chemical,
                price_high_strength_allov=building.price_high_strength_allov,
                price_nanoelement=building.price_nanoelement,
                price_microprocessor_element=building.price_microprocessor_element,
                price_fober_optic_element=building.price_fober_optic_element,
                cost_expert_deployment=building.cost_expert_deployment,
                assembly_workpiece=building.assembly_workpiece,
                time_deployment=building.time_deployment,
                building_size=building.size,
                building_mass=building.mass,
                power_consumption=building.power_consumption,
                basic_building=building
            )
            building_pattern.save()
