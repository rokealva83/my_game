# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from my_game.models import MyUser, Warehouse, TurnAssemblyPieces
from my_game.models import FactoryPattern, BuildingPattern


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
                        warehouse.res_construction_material >= factory_pattern_making.price_construction_material and \
                        warehouse.res_chemical >= factory_pattern_making.price_chemical and \
                        warehouse.res_high_strength_allov >= factory_pattern_making.price_high_strength_allov and \
                        warehouse.res_nanoelement >= factory_pattern_making.price_nanoelement and \
                        warehouse.res_microprocessor_element >= factory_pattern_making.price_microprocessor_element and \
                        warehouse.res_fober_optic_element >= factory_pattern_making.price_fober_optic_element:

            new_internal_currency = session_user.internal_currency - factory_pattern_making.price_internal_currency
            new_construction_material = warehouse.res_construction_material - factory_pattern_making.price_construction_material
            new_chemical = warehouse.res_chemical - factory_pattern_making.price_construction_material
            new_high_strength_allov = warehouse.res_high_strength_allov - factory_pattern_making.price_construction_material
            new_nanoelement = warehouse.res_nanoelement - factory_pattern_making.price_construction_material
            new_microprocessor_element = warehouse.res_microprocessor_element - factory_pattern_making.price_microprocessor_element
            new_fober_optic_element = warehouse.res_fober_optic_element - factory_pattern_making.price_fober_optic_element

            Warehouse.objects.filter(user=session_user, user_city=session_user_city).update(
                res_construction_material=new_construction_material,
                res_chemical=new_chemical,
                res_high_strength_allov=new_high_strength_allov,
                res_nanoelement=new_nanoelement,
                res_microprocessor_element=new_microprocessor_element,
                res_fober_optic_element=new_fober_optic_element
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
