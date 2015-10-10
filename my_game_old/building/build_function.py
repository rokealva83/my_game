# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from my_game.models import MyUser, UserCity, Warehouse, TurnBuilding, TurnAssemblyPieces
from my_game.models import FactoryPattern, FactoryInstalled, BuildingPattern
from my_game.models import WarehouseFactory

#Переименовани шаблона фибрики
def rename_factory_pattern(*args):
    new_name = args[0]
    pattern_id = args[1]
    class_id = args[2]
    if class_id != 13:
        name_factory = FactoryPattern.objects.filter(id=pattern_id).update(name=new_name)
    else:
        name_factory = BuildingPattern.objects.filter(id=pattern_id).update(name=new_name)
    message = 'Шаблон переименован'
    return message

# Улучшение шаблона
def upgrade_factory_pattern(*args):
    pattern_id = int(args[2])
    class_id = int(args[3])
    if class_id != 13:
        old_pattern = FactoryPattern.objects.filter(id=pattern_id).first()
    else:
        old_pattern = BuildingPattern.objects.filter(id=pattern_id).first()
    number = int(args[0])
    if old_pattern.production_class == 12 or old_pattern.production_class == 14:
        speed = 1
    else:
        speed = int(args[1])

    if speed == 1:
        koef_speed = 1
    else:
        koef_speed = int(speed) * 1.6

    if number == 1:
        koef_number = 1
    elif old_pattern.production_class == 13:
        koef_number = int(number)
    else:
        koef_number = int(number) * 1.6

    if class_id != 13:
        new_pattern = FactoryPattern(
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
    else:
        new_pattern = BuildingPattern(

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
            time_production=old_pattern.time_production / speed,
            size=old_pattern.size * koef_speed * koef_number / 3,
            mass=old_pattern.mass * koef_speed * koef_number / 3,
            power_consumption=old_pattern.power_consumption * koef_speed * koef_number / 3,
            max_warehouse=old_pattern.max_warehouse * koef_number,
            warehouse=old_pattern.warehouse * koef_number,
        )
        new_pattern.save()
        new_pattern_id = new_pattern.pk

    if new_pattern.production_class == 12:
        old_pattern_power = old_pattern.power_consumption
        new_power_consumption = old_pattern_power * number
        new_pattern = FactoryPattern.objects.filter(id=new_pattern_id).update(power_consumption=new_power_consumption)
    message = 'Шаблон улучшен'
    return message

# Удаление шаблона
def delete_factory_pattern(*args):
    pattern_id = int(args[0])
    class_id = int(args[1])
    factory = FactoryInstalled.objects.filter(factory_pattern_id=pattern_id).first()
    if factory is not None:
        message = 'Шаблон не может быть удален'
    else:
        if class_id != 13:
            delete_pattern = FactoryPattern.objects.filter(id=pattern_id).delete()
        else:
            delete_pattern = BuildingPattern.objects.filter(id=pattern_id).delete()

        message = 'Шаблон удален'
    return message

#Создание из шаблона заготовки
def making_factory_unit(*args):
    session_user = int(args[0])
    session_user_city = int(args[1])
    amount_factory_unit = int(args[2])
    pattern_id = int(args[3])
    class_id = int(args[4])

    resource1 = 0
    resource2 = 0
    resource3 = 0
    resource4 = 0
    mineral1 = 0
    mineral2 = 0
    mineral3 = 0
    mineral4 = 0

    user = MyUser.objects.filter(user_id=session_user).first()
    warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('id_resource')
    if class_id != 13:
        factory_pattern_making = FactoryPattern.objects.filter(id=pattern_id).first()
    else:
        factory_pattern_making = BuildingPattern.objects.filter(id=pattern_id).first()
    turn_assembly_pieces = len(TurnAssemblyPieces.objects.filter(user=session_user, user_city=session_user_city))

    if turn_assembly_pieces < 3:
        #Проверка наличия ресурсов
        for warehouse in warehouses:
            if warehouse.id_resource == 1:
                resource1 = warehouse.amount
            elif warehouse.id_resource == 2:
                resource2 = warehouse.amount
            elif warehouse.id_resource == 3:
                resource3 = warehouse.amount
            elif warehouse.id_resource == 4:
                resource4 = warehouse.amount
            elif warehouse.id_resource == 5:
                mineral1 = warehouse.amount
            elif warehouse.id_resource == 6:
                mineral2 = warehouse.amount
            elif warehouse.id_resource == 7:
                mineral3 = warehouse.amount
            elif warehouse.id_resource == 8:
                mineral4 = warehouse.amount

        if user.internal_currency >= factory_pattern_making.price_internal_currency and \
                        resource1 >= factory_pattern_making.price_resource1 and \
                        resource2 >= factory_pattern_making.price_resource2 and \
                        resource3 >= factory_pattern_making.price_resource3 and \
                        resource4 >= factory_pattern_making.price_resource4 and \
                        mineral1 >= factory_pattern_making.price_mineral1 and \
                        mineral2 >= factory_pattern_making.price_mineral2 and \
                        mineral3 >= factory_pattern_making.price_mineral3 and \
                        mineral4 >= factory_pattern_making.price_mineral4:

            new_internal_currency = user.internal_currency - factory_pattern_making.price_internal_currency
            new_resource1 = resource1 - factory_pattern_making.price_resource1
            new_resource2 = resource2 - factory_pattern_making.price_resource1
            new_resource3 = resource3 - factory_pattern_making.price_resource1
            new_resource4 = resource4 - factory_pattern_making.price_resource1
            new_mineral1 = mineral1 - factory_pattern_making.price_mineral1
            new_mineral2 = mineral2 - factory_pattern_making.price_mineral1
            new_mineral3 = mineral3 - factory_pattern_making.price_mineral1
            new_mineral4 = mineral4 - factory_pattern_making.price_mineral1

            for warehouse in warehouses:
                if warehouse.id_resource == 1:
                    warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city,
                                                         id_resource=1).update(amount=new_resource1)
                elif warehouse.id_resource == 2:
                    warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city,
                                                         id_resource=2).update(amount=new_resource2)
                elif warehouse.id_resource == 3:
                    warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city,
                                                         id_resource=3).update(amount=new_resource3)
                elif warehouse.id_resource == 4:
                    warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city,
                                                         id_resource=4).update(amount=new_resource4)
                elif warehouse.id_resource == 5:
                    warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city,
                                                         id_resource=5).update(amount=new_mineral1)
                elif warehouse.id_resource == 6:
                    warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city,
                                                         id_resource=6).update(amount=new_mineral2)
                elif warehouse.id_resource == 7:
                    warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city,
                                                         id_resource=7).update(amount=new_mineral3)
                elif warehouse.id_resource == 8:
                    warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city,
                                                         id_resource=8).update(amount=new_mineral4)

            user = MyUser.objects.filter(user_id=session_user).update(internal_currency=new_internal_currency)
            turn_assembly_piece = TurnAssemblyPieces.objects.filter(user=session_user,
                                                                      user_city=session_user_city).last()
            if turn_assembly_piece is not None:
                start_making = turn_assembly_piece.finish_time_assembly
            else:
                start_making = datetime.now()
            build_time = factory_pattern_making.assembly_workpiece * amount_factory_unit
            finish_making = start_making + timedelta(seconds=build_time)
            turn_assembly_pieces = TurnAssemblyPieces(
                user=session_user,
                user_city=session_user_city,
                pattern_id=pattern_id,
                class_id=class_id,
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
    return message

#Развертывание заготоки
def install_factory_unit(*args):
    session_user = args[0]
    session_user_city = args[1]
    pattern_id = args[2]
    class_id = int(args[3])
    user_city = UserCity.objects.filter(id=session_user_city).first()
    if class_id != 13:
        factory_pattern = FactoryPattern.objects.filter(id=pattern_id).first()
    else:
        factory_pattern = BuildingPattern.objects.filter(id=pattern_id).first()
    free_energy = user_city.power - user_city.use_energy
    len_turn_building = len(TurnBuilding.objects.filter(user=session_user, user_city=session_user_city))
    if len_turn_building < 3:

        if factory_pattern.production_class == 12:
            power_consumption = 0
            free_energy = 100
        else:
            power_consumption = factory_pattern.power_consumption

        if factory_pattern.cost_expert_deployment < user_city.population and free_energy > power_consumption:
            last_building = TurnBuilding.objects.filter(user=session_user, user_city=session_user_city).last()
            if last_building is not None:
                start_time = last_building.finish_time_deployment
            else:
                start_time = datetime.now()

            finish_time = start_time + timedelta(seconds=factory_pattern.time_deployment)
            turn_building = TurnBuilding(
                user=session_user,
                user_city=session_user_city,
                factory_id=pattern_id,
                class_id=class_id,
                x=user_city.x,
                y=user_city.y,
                z=user_city.z,
                start_time_deployment=start_time,
                finish_time_deployment=finish_time,
            )
            turn_building.save()
            install_factory = WarehouseFactory.objects.filter(user=session_user, factory_id=pattern_id,
                                                               production_class=class_id).first()
            new_amount = install_factory.amount - 1
            install_factory = WarehouseFactory.objects.filter(user=session_user, factory_id=pattern_id,
                                                               production_class=class_id).update(amount=new_amount)
            if factory_pattern.production_class != 10:
                user_city = UserCity.objects.filter(user=session_user, id=session_user_city).first()
                new_population = user_city.population - factory_pattern.cost_expert_deployment
                user_city = UserCity.objects.filter(id=user_city.id).update(population=new_population)
            message = 'Развертывание начато'
        else:
            message = 'Нехватает инженеров или энергии'
    else:
        message = 'Очередь заполнена'
    return message
