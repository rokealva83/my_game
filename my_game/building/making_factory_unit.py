# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from my_game.models import MyUser, TurnAssemblyPiecesFactory, TurnAssemblyPiecesBuilding
from my_game.models import FactoryPattern, BuildingPattern


# Создание из шаблона заготовки
def making_factory_unit(*args):
    session_user = args[0]
    session_user_city = args[1]
    amount_factory_unit = int(args[2])
    pattern_id = int(args[3])
    class_id = int(args[4])

    warehouse = session_user_city.warehouse
    if class_id != 21:
        factory_pattern_making = FactoryPattern.objects.filter(id=pattern_id).first()
        turn_assembly_pieces = TurnAssemblyPiecesFactory.objects.filter(user=session_user, user_city=session_user_city).all()
        len_turn_assembly_pieces = len(turn_assembly_pieces)
    else:
        factory_pattern_making = BuildingPattern.objects.filter(id=pattern_id).first()
        turn_assembly_pieces = TurnAssemblyPiecesBuilding.objects.filter(user=session_user, user_city=session_user_city).all()
        len_turn_assembly_pieces = len(turn_assembly_pieces)

    if len_turn_assembly_pieces < 3:

        # Проверка наличия ресурсов
        if session_user.internal_currency >= factory_pattern_making.price_internal_currency and \
                        warehouse.mat_construction_material >= factory_pattern_making.price_construction_material and \
                        warehouse.mat_chemical >= factory_pattern_making.price_chemical and \
                        warehouse.mat_high_strength_allov >= factory_pattern_making.price_high_strength_allov and \
                        warehouse.mat_nanoelement >= factory_pattern_making.price_nanoelement and \
                        warehouse.mat_microprocessor_element >= factory_pattern_making.price_microprocessor_element and \
                        warehouse.mat_fober_optic_element >= factory_pattern_making.price_fober_optic_element:

            new_internal_currency = session_user.internal_currency - factory_pattern_making.price_internal_currency
            new_construction_material = warehouse.mat_construction_material - factory_pattern_making.price_construction_material
            new_chemical = warehouse.mat_chemical - factory_pattern_making.price_chemical
            new_high_strength_allov = warehouse.mat_high_strength_allov - factory_pattern_making.price_high_strength_allov
            new_nanoelement = warehouse.mat_nanoelement - factory_pattern_making.price_nanoelement
            new_microprocessor_element = warehouse.mat_microprocessor_element - factory_pattern_making.price_microprocessor_element
            new_fober_optic_element = warehouse.mat_fober_optic_element - factory_pattern_making.price_fober_optic_element

            setattr(warehouse, 'mat_construction_material', new_construction_material)
            setattr(warehouse, 'new_chemical', new_chemical)
            setattr(warehouse, 'new_high_strength_allov', new_high_strength_allov)
            setattr(warehouse, 'new_nanoelement', new_nanoelement)
            setattr(warehouse, 'new_microprocessor_element', new_microprocessor_element)
            setattr(warehouse, 'new_fober_optic_elemen', new_fober_optic_element)
            warehouse.save()

            MyUser.objects.filter(user_id=session_user.id).update(internal_currency=new_internal_currency)
            turn_assembly_pieces_last = []
            if len_turn_assembly_pieces >=1:
                turn_assembly_pieces_last = turn_assembly_pieces[len_turn_assembly_pieces - 1]
            if turn_assembly_pieces_last:
                start_making = turn_assembly_pieces_last.finish_time_assembly
            else:
                start_making = datetime.now()
            build_time = factory_pattern_making.assembly_workpiece * amount_factory_unit
            finish_making = start_making + timedelta(seconds=build_time)
            if class_id != 21:
                turn_assembly_pieces = TurnAssemblyPiecesFactory(
                    user=session_user,
                    user_city=session_user_city,
                    pattern=factory_pattern_making,
                    class_id=class_id,
                    start_time_assembly=start_making,
                    finish_time_assembly=finish_making,
                    amount_assembly=amount_factory_unit
                )
                turn_assembly_pieces.save()
            else:
                turn_assembly_pieces = TurnAssemblyPiecesBuilding(
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
