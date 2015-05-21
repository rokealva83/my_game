# -*- coding: utf-8 -*-

from django.utils import timezone
from my_game.models import MyUser, User_city
from my_game.models import Turn_building
from my_game.models import Factory_pattern, Factory_installed, Building_pattern, Building_installed
import my_game.verification_func as verification_func

#Проверки очереди развертывания
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
        #Проверка времени
        if new_delta > delta:
            verification_func.verification_of_resources(user)
            if turn_building.class_id != 13:
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
            else:
                factory_pattern = Building_pattern.objects.filter(id=turn_building.factory_id).first()
                factory_installed = Building_installed(
                    user=user,
                    user_city=user_city.id,
                    building_pattern_id=turn_building.factory_id,
                    name=factory_pattern.name,
                    time_deployment=factory_pattern.time_deployment,
                    production_class=factory_pattern.production_class,
                    production_id=factory_pattern.production_id,
                    time_production=factory_pattern.time_production,
                    warehouse=0,
                    max_warehouse=factory_pattern.max_warehouse,
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
