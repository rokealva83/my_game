# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from my_game.models import MyUser, User_city, Warehouse, Turn_building, Turn_assembly_pieces
from my_game.models import Factory_pattern, Factory_installed
from my_game.models import Warehouse_factory


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
    factory = Factory_installed.objects.filter(factory_pattern_id=pattern_id).first()
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

        if factory_pattern.production_class == 12:
            power_consumption = 0
        else:
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