# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from my_game.models import UserCity, TurnBuildingBuilding, TurnBuildingFactory
from my_game.models import FactoryPattern, BuildingPattern
from my_game.models import WarehouseFactory, WarehouseBuilding
from my_game.models import UserVariables


# Развертывание заготоки
def install_factory_unit(*args):
    session_user = args[0]
    session_user_city = args[1]
    pattern_id = args[2]
    class_id = int(args[3])
    user_variables = UserVariables.objects.first()
    if class_id != 21:
        factory_pattern = FactoryPattern.objects.filter(id=pattern_id).first()
        warehouse_building = WarehouseFactory.objects.filter(user=session_user, user_city=session_user_city,
                                                             factory=factory_pattern).first()
        turn_building = TurnBuildingFactory.objects.filter(user=session_user, user_city=session_user_city).all()
        len_turn_building = len(turn_building)
    else:
        factory_pattern = BuildingPattern.objects.filter(id=pattern_id).first()
        warehouse_building = WarehouseBuilding.objects.filter(user=session_user, user_city=session_user_city,
                                                              building=factory_pattern).first()
        turn_building = TurnBuildingBuilding.objects.filter(user=session_user, user_city=session_user_city).all()
        len_turn_building = len(turn_building)

    if warehouse_building and len_turn_building < user_variables.max_turn_building_basic:
        free_energy = session_user_city.power - session_user_city.use_energy
        if factory_pattern.production_class == 12:
            power_consumption = 0
            free_energy = 100
        else:
            power_consumption = factory_pattern.power_consumption

        last_building = []
        if factory_pattern.cost_expert_deployment < session_user_city.population and free_energy > power_consumption:
            if len_turn_building >= 1:
                last_building = turn_building[len_turn_building - 1]
            if last_building:
                start_time = last_building.finish_time_deployment
            else:
                start_time = datetime.now()

            finish_time = start_time + timedelta(seconds=factory_pattern.time_deployment)
            if class_id != 21:
                turn_building = TurnBuildingFactory(
                    user=session_user,
                    user_city=session_user_city,
                    factory=factory_pattern,
                    class_id=class_id,
                    x=session_user_city.x,
                    y=session_user_city.y,
                    z=session_user_city.z,
                    start_time_deployment=start_time,
                    finish_time_deployment=finish_time,
                )
            else:
                turn_building = TurnBuildingBuilding(
                    user=session_user,
                    user_city=session_user_city,
                    factory=factory_pattern,
                    class_id=class_id,
                    x=session_user_city.x,
                    y=session_user_city.y,
                    z=session_user_city.z,
                    start_time_deployment=start_time,
                    finish_time_deployment=finish_time,
                )
            turn_building.save()
            if class_id != 21:
                new_amount = warehouse_building.amount - 1
                WarehouseFactory.objects.filter(user=session_user, user_city=session_user_city,
                                                factory=factory_pattern).update(amount=new_amount)
            else:
                new_amount = warehouse_building.amount - 1
                WarehouseBuilding.objects.filter(user=session_user, user_city=session_user_city,
                                                 building=factory_pattern).update(amount=new_amount)
            if factory_pattern.production_class != 10:
                new_population = session_user_city.population - factory_pattern.cost_expert_deployment
                UserCity.objects.filter(id=session_user_city.id).update(population=new_population)
            message = 'Развертывание начато'
        else:
            message = 'Не хватает инженеров или энергии'
    else:
        message = 'Очередь заполнена, нет заготовки на складе'
    return message
