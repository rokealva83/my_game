# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from my_game.models import UserCity, TurnBuilding
from my_game.models import FactoryPattern, BuildingPattern
from my_game.models import WarehouseFactory, WarehouseBuilding


# Развертывание заготоки
def install_factory_unit(*args):
    session_user = args[0]
    session_user_city = args[1]
    pattern_id = args[2]
    class_id = int(args[3])
    warehouse_factory = None
    warehouse_building = None
    if class_id != 21:
        factory_pattern = FactoryPattern.objects.filter(id=pattern_id).first()
        warehouse_factory = WarehouseFactory.objects.filter(user=session_user, user_city=session_user_city,
                                                            factory=factory_pattern).first()
    else:
        factory_pattern = BuildingPattern.objects.filter(id=pattern_id).first()
        warehouse_building = WarehouseBuilding.objects.filter(user=session_user, user_city=session_user_city,
                                                              building=factory_pattern).first()
    if warehouse_building or warehouse_factory:
        free_energy = session_user_city.power - session_user_city.use_energy
        len_turn_building = len(TurnBuilding.objects.filter(user=session_user, user_city=session_user_city))
        if len_turn_building < 3:

            if factory_pattern.production_class == 12:
                power_consumption = 0
                free_energy = 100
            else:
                power_consumption = factory_pattern.power_consumption

            if factory_pattern.cost_expert_deployment < session_user_city.population and free_energy > power_consumption:
                last_building = TurnBuilding.objects.filter(user=session_user, user_city=session_user_city).last()
                if last_building is not None:
                    start_time = last_building.finish_time_deployment
                else:
                    start_time = datetime.now()

                finish_time = start_time + timedelta(seconds=factory_pattern.time_deployment)
                turn_building = TurnBuilding(
                    user=session_user,
                    user_city=session_user_city,
                    factory=pattern_id,
                    class_id=class_id,
                    x=session_user_city.x,
                    y=session_user_city.y,
                    z=session_user_city.z,
                    start_time_deployment=start_time,
                    finish_time_deployment=finish_time,
                )
                turn_building.save()
                if class_id != 21:
                    new_amount = warehouse_factory.amount - 1
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
                message = 'Нехватает инженеров или энергии'
        else:
            message = 'Очередь заполнена'
    else:
        message = 'Нет заготовки на складе'
    return message
