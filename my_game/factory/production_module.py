# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from my_game.models import MyUser
from my_game.models import TurnProduction
from my_game.models import HullPattern, ShellPattern, ShieldPattern, GeneratorPattern, EnginePattern, \
    ArmorPattern, ModulePattern, WeaponPattern, FuelPattern, DevicePattern
from my_game.models import Warehouse


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

            if session_user.internal_currency >= module_which_produces.price_internal_currency * \
                    int(amount_element) and warehouse.res_construction_material >= \
                            module_which_produces.price_construction_material * int(amount_element) and \
                            warehouse.res_chemical >= module_which_produces.price_chemical * int(amount_element) and \
                            warehouse.res_high_strength_allov >= module_which_produces.price_high_strength_allov * \
                            int(amount_element) and warehouse.res_nanoelement >= \
                            module_which_produces.price_nanoelement * int(amount_element) and \
                            warehouse.res_microprocessor_element >= module_which_produces.price_microprocessor_element * \
                            int(amount_element) and warehouse.res_fober_optic_element >= \
                            module_which_produces.price_fober_optic_element * int(amount_element):

                new_internal_currency = session_user.internal_currency - \
                                        module_which_produces.price_internal_currency * int(amount_element)
                new_construction_material = warehouse.res_construction_material - \
                                            module_which_produces.price_construction_material * int(amount_element)
                new_chemical = warehouse.res_chemical - module_which_produces.price_chemical * int(amount_element)
                new_high_strength_allov = warehouse.res_high_strength_allov - \
                                          module_which_produces.price_res_high_strength_allov * int(amount_element)
                new_nanoelement = warehouse.res_nanoelement - \
                                  module_which_produces.price_nanoelement * int(amount_element)
                new_microprocessor_element = warehouse.res_microprocessor_element - \
                                             module_which_produces.price_microprocessor_element * int(amount_element)
                new_fober_optic_element = warehouse.res_fober_optic_element - \
                                          module_which_produces.price_fober_optic_element * int(amount_element)

                Warehouse.objects.filter(user=session_user, user_city=session_user_city).update(
                    construction_material=new_construction_material,
                    chemical=new_chemical,
                    high_strength_allov=new_high_strength_allov,
                    nanoelement=new_nanoelement,
                    microprocessor_element=new_microprocessor_element,
                    fober_optic_element=new_fober_optic_element
                )

                MyUser.objects.filter(user_id=session_user.id).update(internal_currency=new_internal_currency)
                turn_productions = TurnProduction.objects.filter(user=session_user, user_city=session_user_city,
                                                                 factory=factory).last()
                if turn_productions is not None:
                    start_making = turn_productions.finish_time_production
                else:
                    start_making = datetime.now()
                build_time = factory.time_production * int(amount_element)
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
