# -*- coding: utf-8 -*-

from django.utils import timezone
from my_game.models import UserCity
from my_game.models import TurnBuilding
from my_game.models import FactoryPattern, FactoryInstalled, BuildingPattern, BuildingInstalled, WarehouseFactoryResource
import my_game.verification_func as verification_func


# Проверки очереди развертывания
def verification_phase_of_construction(request):
    user = request
    turn_buildings = TurnBuilding.objects.filter(user=user)
    time = timezone.now()
    for turn_building in turn_buildings:
        time_start = turn_building.start_time_deployment
        delta_time = time - time_start
        new_delta = delta_time.seconds
        delta_time = turn_building.finish_time_deployment - turn_building.start_time_deployment
        delta = delta_time.seconds
        user_city = turn_building.user_city
        # Проверка времени
        if new_delta > delta:
            verification_func.verification_of_resources(user)
            if turn_building.class_id != 21:
                warehouse_factory_resource = WarehouseFactoryResource(
                )
                warehouse_factory_resource.save()
                factory_pattern = FactoryPattern.objects.filter(id=turn_building.factory).first()
                factory_installed = FactoryInstalled(
                    user=user,
                    user_city=user_city,
                    factory_pattern=factory_pattern,
                    factory_warehouse=warehouse_factory_resource,
                    production_class=factory_pattern.production_class,
                    production_id=factory_pattern.production_id
                )
                factory_installed.save()
                power_consumption = factory_installed.factory_pattern.power_consumption
            else:
                factory_pattern = BuildingPattern.objects.filter(id=turn_building.factory).first()
                factory_installed = BuildingInstalled(
                    user=user,
                    user_city=user_city,
                    building_pattern=factory_pattern,
                    production_class=factory_pattern.production_class,
                    production_id=factory_pattern.production_id
                )
                factory_installed.save()
                power_consumption = factory_installed.building_pattern.power_consumption
            if factory_pattern.production_class == 12:
                new_power = user_city.power + power_consumption
                UserCity.objects.filter(id=user_city.id).update(power=new_power)
            else:
                new_energy = user_city.use_energy + power_consumption
                UserCity.objects.filter(id=user_city.id).update(use_energy=new_energy)

            if factory_pattern.production_class == 10:
                new_max_population = user_city.max_population + 100 * factory_pattern.production_id
                UserCity.objects.filter(id=user_city.id).update(max_population=new_max_population)

            TurnBuilding.objects.filter(id=turn_building.id).delete()
