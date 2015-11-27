# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from my_game.models import MyUser, UserCity, Warehouse, TurnBuilding, TurnAssemblyPieces
from my_game.models import FactoryPattern, FactoryInstalled, BuildingPattern
from my_game.models import WarehouseFactory, WarehouseBuilding


# Переименовани шаблона фибрики
def rename_factory_pattern(*args):
    new_name = args[0]
    pattern_id = args[1]
    class_id = args[2]
    if class_id != 13:
        FactoryPattern.objects.filter(id=pattern_id).update(name=new_name)
    else:
        BuildingPattern.objects.filter(id=pattern_id).update(name=new_name)
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
            basic_factory=old_pattern.basic_factory,
            factory_name=old_pattern.factory_name,
            price_internal_currency=old_pattern.price_internal_currency * koef_speed * koef_number,
            price_construction_material=old_pattern.price_construction_material * koef_speed * koef_number,
            price_chemical=old_pattern.price_chemical * koef_speed * koef_number,
            price_high_strength_allov=old_pattern.price_high_strength_allov * koef_speed * koef_number,
            price_nanoelement=old_pattern.price_nanoelement * koef_speed * koef_number,
            price_microprocessor_element=old_pattern.price_microprocessor_element * koef_speed * koef_number,
            price_fober_optic_element=old_pattern.price_fober_optic_element * koef_speed * koef_number,
            cost_expert_deployment=old_pattern.cost_expert_deployment * koef_speed * koef_number,
            assembly_workpiece=old_pattern.assembly_workpiece * koef_speed * koef_number,
            time_deployment=old_pattern.time_deployment * koef_speed * koef_number,
            production_class=old_pattern.production_class,
            production_id=old_pattern.production_id,
            time_production=old_pattern.time_production / (speed * number),
            factory_size=old_pattern.factory_size * koef_speed * koef_number / 3,
            factory_mass=old_pattern.factory_mass * koef_speed * koef_number / 3,
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
            price_construction_material=old_pattern.price_construction_material * koef_speed * koef_number,
            price_chemical=old_pattern.price_chemical * koef_speed * koef_number,
            price_high_strength_allov=old_pattern.price_high_strength_allov * koef_speed * koef_number,
            price_nanoelement=old_pattern.price_nanoelement * koef_speed * koef_number,
            price_microprocessor_element=old_pattern.price_microprocessor_element * koef_speed * koef_number,
            price_fober_optic_element=old_pattern.price_fober_optic_element * koef_speed * koef_number,
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
        FactoryPattern.objects.filter(id=new_pattern_id).update(power_consumption=new_power_consumption)
    message = 'Шаблон улучшен'
    return message


# Удаление шаблона
def delete_factory_pattern(*args):
    pattern_id = int(args[0])
    class_id = int(args[1])
    factory_pattern = FactoryPattern.objects.filter(id=pattern_id).first()
    factory = FactoryInstalled.objects.filter(factory_pattern=factory_pattern).first()
    if factory is not None:
        message = 'Шаблон не может быть удален'
    else:
        if class_id != 13:
            FactoryPattern.objects.filter(id=pattern_id).delete()
        else:
            BuildingPattern.objects.filter(id=pattern_id).delete()
        message = 'Шаблон удален'
    return message


# Создание из шаблона заготовки
def making_factory_unit(*args):
    session_user = args[0]
    session_user_city = args[1]
    amount_factory_unit = int(args[2])
    pattern_id = int(args[3])
    class_id = int(args[4])

    warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).first()
    if class_id != 13:
        factory_pattern_making = FactoryPattern.objects.filter(id=pattern_id).first()
    else:
        factory_pattern_making = BuildingPattern.objects.filter(id=pattern_id).first()
    turn_assembly_pieces = len(TurnAssemblyPieces.objects.filter(user=session_user, user_city=session_user_city))

    if turn_assembly_pieces < 3:
        # Проверка наличия ресурсов

        if session_user.internal_currency >= factory_pattern_making.price_internal_currency and \
                        warehouse.construction_material >= factory_pattern_making.price_construction_material and \
                        warehouse.chemical >= factory_pattern_making.price_chemical and \
                        warehouse.high_strength_allov >= factory_pattern_making.price_high_strength_allov and \
                        warehouse.nanoelement >= factory_pattern_making.price_nanoelement and \
                        warehouse.microprocessor_element >= factory_pattern_making.price_microprocessor_element and \
                        warehouse.fober_optic_element >= factory_pattern_making.price_fober_optic_element:

            new_internal_currency = session_user.internal_currency - factory_pattern_making.price_internal_currency
            new_construction_material = warehouse.construction_material - factory_pattern_making.price_construction_material
            new_chemical = warehouse.chemical - factory_pattern_making.price_construction_material
            new_high_strength_allov = warehouse.high_strength_allov - factory_pattern_making.price_construction_material
            new_nanoelement = warehouse.nanoelement - factory_pattern_making.price_construction_material
            new_microprocessor_element = warehouse.microprocessor_element - factory_pattern_making.price_microprocessor_element
            new_fober_optic_element = warehouse.fober_optic_element - factory_pattern_making.price_fober_optic_element

            Warehouse.objects.filter(user=session_user, user_city=session_user_city).update(
                construction_material=new_construction_material,
                chemical=new_chemical,
                high_strength_allov=new_high_strength_allov,
                nanoelement=new_nanoelement,
                microprocessor_element=new_microprocessor_element,
                fober_optic_element=new_fober_optic_element
            )

            MyUser.objects.filter(user_id=session_user.id).update(internal_currency=new_internal_currency)
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
                pattern=factory_pattern_making,
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


# Развертывание заготоки
def install_factory_unit(*args):
    session_user = args[0]
    session_user_city = args[1]
    pattern_id = args[2]
    class_id = int(args[3])
    warehouse_factory = None
    warehouse_building = None
    if class_id != 13:
        factory_pattern = FactoryPattern.objects.filter(id=pattern_id).first()
        warehouse_factory = WarehouseFactory.objects.filter(user=session_user, user_city=session_user_city,
                                                            factory=factory_pattern).first()
    else:
        factory_pattern = BuildingPattern.objects.filter(id=pattern_id).first()
        warehouse_building = WarehouseBuilding.objects.filter(user=session_user, user_city=session_user_city,
                                                              factory=factory_pattern).first()
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
                    factory_id=pattern_id,
                    class_id=class_id,
                    x=session_user_city.x,
                    y=session_user_city.y,
                    z=session_user_city.z,
                    start_time_deployment=start_time,
                    finish_time_deployment=finish_time,
                )
                turn_building.save()
                if class_id != 13:
                    new_amount = warehouse_factory.amount - 1
                    WarehouseFactory.objects.filter(user=session_user, user_city=session_user_city,
                                                    factory=factory_pattern).update(amount=new_amount)
                else:
                    new_amount = warehouse_building.amount - 1
                    WarehouseBuilding.objects.filter(user=session_user, user_city=session_user_city,
                                                     factory=factory_pattern).update(amount=new_amount)
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
