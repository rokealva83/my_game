# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from my_game.models import TurnProduction
from my_game.models import HullPattern, ShellPattern, ShieldPattern, GeneratorPattern, EnginePattern, \
    ArmorPattern, ModulePattern, WeaponPattern, FuelPattern, DevicePattern


def production_module(*args):
    session_user = args[0]
    session_user_city = args[1]
    factory = args[2]
    element_id = args[3]
    amount_element = args[4]

    warehouse = factory.factory_warehouse

    if warehouse:
        len_turn_production = len(TurnProduction.objects.filter(user=session_user, user_city=session_user_city,
                                                                factory=factory))
        module_which_produces = 0
        if len_turn_production < 1:
            if factory.production_class == 1:
                module_which_produces = HullPattern.objects.filter(id=element_id).first()
            elif factory.production_class == 2:
                module_which_produces = ArmorPattern.objects.filter(id=element_id).first()
            elif factory.production_class == 3:
                module_which_produces = ShieldPattern.objects.filter(id=element_id).first()
            elif factory.production_class == 4:
                module_which_produces = EnginePattern.objects.filter(id=element_id).first()
            elif factory.production_class == 5:
                module_which_produces = GeneratorPattern.objects.filter(id=element_id).first()
            elif factory.production_class == 6:
                module_which_produces = WeaponPattern.objects.filter(id=element_id).first()
            elif factory.production_class == 7:
                module_which_produces = ShellPattern.objects.filter(id=element_id).first()
            elif factory.production_class == 8:
                module_which_produces = ModulePattern.objects.filter(id=element_id).first()
            elif factory.production_class == 9:
                module_which_produces = DevicePattern.objects.filter(id=element_id).first()
            elif factory.production_class == 14:
                module_which_produces = FuelPattern.objects.filter(id=element_id).first()

            if session_user.internal_currency >= module_which_produces.price_internal_currency * int(amount_element) \
                    and warehouse.res_nickel >= module_which_produces.price_nickel * int(amount_element) \
                    and warehouse.res_iron >= module_which_produces.price_iron * int(amount_element) \
                    and warehouse.res_cooper >= module_which_produces.price_cooper * int(amount_element) \
                    and warehouse.res_aluminum >= module_which_produces.price_aluminum * int(amount_element) \
                    and warehouse.res_veriarit >= module_which_produces.price_veriarit * int(amount_element) \
                    and warehouse.res_inneilit >= module_which_produces.price_inneilit * int(amount_element) \
                    and warehouse.res_renniit >= module_which_produces.price_renniit * int(amount_element) \
                    and warehouse.res_cobalt >= module_which_produces.price_cobalt * int(amount_element) \
                    and warehouse.mat_construction_material >= module_which_produces.price_construction_material * (
                                                int(amount_element)) \
                    and warehouse.mat_chemical >= module_which_produces.price_chemical * int(amount_element) \
                    and warehouse.mat_high_strength_allov >= module_which_produces.price_high_strength_allov * (
                            int(amount_element)) \
                    and warehouse.mat_nanoelement >= module_which_produces.price_nanoelement * int(amount_element) \
                    and warehouse.mat_microprocessor_element >= module_which_produces.price_microprocessor_element * (
                                int(amount_element)) \
                    and warehouse.mat_fober_optic_element >= module_which_produces.price_fober_optic_element * (
                            int(amount_element)):

                new_internal_currency = session_user.internal_currency - (
                    module_which_produces.price_internal_currency * int(amount_element))
                new_res_nickel = warehouse.res_nickel - module_which_produces.price_nickel * int(amount_element)
                new_res_iron = warehouse.res_iron - module_which_produces.price_iron * int(amount_element)
                new_res_cooper = warehouse.res_cooper - module_which_produces.price_cooper * int(amount_element)
                new_res_aluminum = warehouse.res_aluminum - module_which_produces.price_aluminum * int(amount_element)
                new_res_veriarit = warehouse.res_veriarit - module_which_produces.price_veriarit * int(amount_element)
                new_res_inneilit = warehouse.res_inneilit - module_which_produces.price_inneilit * int(amount_element)
                new_res_renniit = warehouse.res_renniit - module_which_produces.price_renniit * int(amount_element)
                new_res_cobalt = warehouse.res_cobalt - module_which_produces.price_cobalt * int(amount_element)
                new_construction_material = warehouse.mat_construction_material - (
                    module_which_produces.price_construction_material * int(amount_element))
                new_chemical = warehouse.mat_chemical - module_which_produces.price_chemical * int(amount_element)
                new_high_strength_allov = warehouse.mat_high_strength_allov - (
                    module_which_produces.price_high_strength_allov * int(amount_element))
                new_nanoelement = warehouse.mat_nanoelement - (
                    module_which_produces.price_nanoelement * int(amount_element))
                new_microprocessor_element = warehouse.mat_microprocessor_element - (
                    module_which_produces.price_microprocessor_element * int(amount_element))
                new_fober_optic_element = warehouse.mat_fober_optic_element - (
                    module_which_produces.price_fober_optic_element * int(amount_element))

                setattr(warehouse, 'res_nickel', new_res_nickel)
                setattr(warehouse, 'res_iron', new_res_iron)
                setattr(warehouse, 'res_cooper', new_res_cooper)
                setattr(warehouse, 'res_aluminum', new_res_aluminum)
                setattr(warehouse, 'res_veriarit', new_res_veriarit)
                setattr(warehouse, 'res_inneilit', new_res_inneilit)
                setattr(warehouse, 'res_renniit', new_res_renniit)
                setattr(warehouse, 'res_cobalt', new_res_cobalt)
                setattr(warehouse, 'mat_construction_material', new_construction_material)
                setattr(warehouse, 'mat_chemical', new_chemical)
                setattr(warehouse, 'mat_high_strength_allov', new_high_strength_allov)
                setattr(warehouse, 'mat_nanoelement', new_nanoelement)
                setattr(warehouse, 'mat_microprocessor_element', new_microprocessor_element)
                setattr(warehouse, 'mat_fober_optic_element', new_fober_optic_element)
                warehouse.save()
                setattr(session_user, 'internal_currency', new_internal_currency)
                session_user.save()

                turn_productions = TurnProduction.objects.filter(user=session_user, user_city=session_user_city,
                                                                 factory=factory).last()
                if turn_productions is not None:
                    start_making = turn_productions.finish_time_production
                else:
                    start_making = datetime.now()
                build_time = factory.factory_pattern.time_production * int(amount_element)
                finish_making = start_making + timedelta(seconds=build_time)
                turn_production = TurnProduction(
                    user=session_user,
                    user_city=session_user_city,
                    factory=factory,
                    element_id=element_id,
                    start_time_production=start_making,
                    finish_time_production=finish_making,
                    amount_element=amount_element
                )
                turn_production.save()
                message = 'Производство начато'
            else:
                message = 'Нехватает ресурсов'
        else:
            message = 'Очередь завода занята'
        return message
    else:
        message = 'Нехватает ресурсов'
    return message
