# -*- coding: utf-8 -*-

from datetime import datetime
from my_game.models import MyUser
from my_game.models import HullPattern, ShellPattern, ShieldPattern, GeneratorPattern, EnginePattern, \
    ArmorPattern, ModulePattern, WeaponPattern, FuelPattern, DevicePattern
from my_game.models import TurnComplexProduction, Warehouse


def complex_production_module(*args):
    manufacturing_complex = args[0]
    factory = args[1]
    element_id = args[2]
    start_time_production = args[3]
    if start_time_production != 0:
        start_time_production = start_time_production
    else:
        start_time_production = datetime.now()
    session_user = manufacturing_complex.user
    warehouse = manufacturing_complex.warehouse_complex

    if warehouse:
        module_which_produces = 0
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

        if session_user.internal_currency >= module_which_produces.price_internal_currency and \
                        warehouse.res_construction_material >= module_which_produces.price_construction_material and \
                        warehouse.res_chemical >= module_which_produces.price_chemical and \
                        warehouse.res_high_strength_allov >= module_which_produces.price_high_strength_allov and \
                        warehouse.res_nanoelement >= module_which_produces.price_nanoelement and \
                        warehouse.res_microprocessor_element >= module_which_produces.price_microprocessor_element and \
                        warehouse.res_fober_optic_element >= module_which_produces.price_fober_optic_element:

            new_internal_currency = session_user.internal_currency - module_which_produces.price_internal_currency
            new_construction_material = warehouse.construction_material - module_which_produces.price_construction_material
            new_chemical = warehouse.chemical - module_which_produces.price_construction_material
            new_high_strength_allov = warehouse.high_strength_allov - module_which_produces.price_construction_material
            new_nanoelement = warehouse.nanoelement - module_which_produces.price_construction_material
            new_microprocessor_element = warehouse.microprocessor_element - module_which_produces.price_microprocessor_element
            new_fober_optic_element = warehouse.fober_optic_element - module_which_produces.price_fober_optic_element

            Warehouse.objects.filter(id=manufacturing_complex.warehouse_complex.id).update(
                construction_material=new_construction_material,
                chemical=new_chemical,
                high_strength_allov=new_high_strength_allov,
                nanoelement=new_nanoelement,
                microprocessor_element=new_microprocessor_element,
                fober_optic_element=new_fober_optic_element
            )
            MyUser.objects.filter(user_id=manufacturing_complex.user).update(
                internal_currency=new_internal_currency)

            turn_production = TurnComplexProduction(
                manufacturing_complex=manufacturing_complex,
                factory=factory,
                element_id=element_id,
                start_time_production=start_time_production,
                time=factory.time_production
            )
            turn_production.save()
            message = 0
        else:
            message = 1
        return message
    else:
        message = 1
    return message
