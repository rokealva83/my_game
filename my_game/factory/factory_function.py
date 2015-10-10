# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from my_game.models import MyUser
from my_game.models import TurnProduction
from my_game.models import HullPattern, ShellPattern, ShieldPattern, GeneratorPattern, EnginePattern, \
    ArmorPattern, ModulePattern, WeaponPattern, FactoryInstalled, FuelPattern, DevicePattern
from my_game.models import WarehouseFactoryResource
from my_game.models import ManufacturingComplex, WarehouseComplex, TurnComplexProduction


def rename_element_pattern(*args):
    pattern_id = args[2]
    element_id = args[3]
    new_names = args[4]
    factory = FactoryInstalled.objects.filter(id=pattern_id).first()
    production_class = factory.production_class
    if production_class == 1:
        new_name = HullPattern.objects.filter(id=element_id).update(name=new_names)
    if production_class == 2:
        new_name = ArmorPattern.objects.filter(id=element_id).update(name=new_names)
    if production_class == 3:
        new_name = ShieldPattern.objects.filter(id=element_id).update(name=new_names)
    if production_class == 4:
        new_name = EnginePattern.objects.filter(id=element_id).update(name=new_names)
    if production_class == 5:
        new_name = GeneratorPattern.objects.filter(id=element_id).update(name=new_names)
    if production_class == 6:
        new_name = WeaponPattern.objects.filter(id=element_id).update(name=new_names)
    if production_class == 7:
        new_name = ShellPattern.objects.filter(id=element_id).update(name=new_names)
    if production_class == 8:
        new_name = ModulePattern.objects.filter(id=element_id).update(name=new_names)
    if production_class == 9:
        new_name = DevicePattern.objects.filter(id=element_id).update(name=new_names)
    if production_class == 14:
        new_name = FuelPattern.objects.filter(id=element_id).update(name=new_names)
    message = 'Модуль переименован'
    return (message)


def production_module(*args):
    session_user = args[0]
    session_user_city = args[1]
    factory_id = args[2]
    element_id = args[3]
    amount_element = args[4]

    user = MyUser.objects.filter(user_id=session_user).first()
    warehouses = WarehouseFactoryResource.objects.filter(id_factory=factory_id).order_by('id_resource')
    if warehouses:
        factory_worker = FactoryInstalled.objects.filter(id=factory_id).first()
        len_turn_production = len(TurnProduction.objects.filter(user=session_user, user_city=session_user_city,
                                                                 factory_id=factory_worker.id))
        module_which_produces = 0
        if len_turn_production < 1:
            if factory_worker.production_class == 1:
                module_which_produces = HullPattern.objects.filter(id=element_id).first()
            elif factory_worker.production_class == 2:
                module_which_produces = ArmorPattern.objects.filter(id=element_id).first()
            elif factory_worker.production_class == 3:
                module_which_produces = ShieldPattern.objects.filter(id=element_id).first()
            elif factory_worker.production_class == 4:
                module_which_produces = EnginePattern.objects.filter(id=element_id).first()
            elif factory_worker.production_class == 5:
                module_which_produces = GeneratorPattern.objects.filter(id=element_id).first()
            elif factory_worker.production_class == 6:
                module_which_produces = WeaponPattern.objects.filter(id=element_id).first()
            elif factory_worker.production_class == 7:
                module_which_produces = ShellPattern.objects.filter(id=element_id).first()
            elif factory_worker.production_class == 8:
                module_which_produces = ModulePattern.objects.filter(id=element_id).first()
            elif factory_worker.production_class == 9:
                module_which_produces = DevicePattern.objects.filter(id=element_id).first()
            elif factory_worker.production_class == 14:
                module_which_produces = FuelPattern.objects.filter(id=element_id).first()

            resource1 = 0
            resource2 = 0
            resource3 = 0
            resource4 = 0
            mineral1 = 0
            mineral2 = 0
            mineral3 = 0
            mineral4 = 0

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

            if user.internal_currency >= module_which_produces.price_internal_currency * int(amount_element) and \
                            resource1 >= module_which_produces.price_resource1 * int(amount_element) and \
                            resource2 >= module_which_produces.price_resource2 * int(amount_element) and \
                            resource3 >= module_which_produces.price_resource3 * int(amount_element) and \
                            resource4 >= module_which_produces.price_resource4 * int(amount_element) and \
                            mineral1 >= module_which_produces.price_mineral1 * int(amount_element) and \
                            mineral2 >= module_which_produces.price_mineral2 * int(amount_element) and \
                            mineral3 >= module_which_produces.price_mineral3 * int(amount_element) and \
                            mineral4 >= module_which_produces.price_mineral4 * int(amount_element):

                new_internal_currency = user.internal_currency - module_which_produces.price_internal_currency * int(
                    amount_element)
                new_resource1 = resource1 - module_which_produces.price_resource1 * int(amount_element)
                new_resource2 = resource2 - module_which_produces.price_resource2 * int(amount_element)
                new_resource3 = resource3 - module_which_produces.price_resource3 * int(amount_element)
                new_resource4 = resource4 - module_which_produces.price_resource4 * int(amount_element)
                new_mineral1 = mineral1 - module_which_produces.price_mineral1 * int(amount_element)
                new_mineral2 = mineral2 - module_which_produces.price_mineral2 * int(amount_element)
                new_mineral3 = mineral3 - module_which_produces.price_mineral3 * int(amount_element)
                new_mineral4 = mineral4 - module_which_produces.price_mineral4 * int(amount_element)

                for warehouse in warehouses:
                    if warehouse.id_resource == 1:
                        warehouse = WarehouseFactoryResource.objects.filter(id_factory=factory_id,
                                                                              id_resource=1).update(
                            amount=new_resource1)
                    elif warehouse.id_resource == 2:
                        warehouse = WarehouseFactoryResource.objects.filter(id_factory=factory_id,
                                                                              id_resource=2).update(
                            amount=new_resource2)
                    elif warehouse.id_resource == 3:
                        warehouse = WarehouseFactoryResource.objects.filter(id_factory=factory_id,
                                                                              id_resource=3).update(
                            amount=new_resource3)
                    elif warehouse.id_resource == 4:
                        warehouse = WarehouseFactoryResource.objects.filter(id_factory=factory_id,
                                                                              id_resource=4).update(
                            amount=new_resource4)
                    elif warehouse.id_resource == 5:
                        warehouse = WarehouseFactoryResource.objects.filter(id_factory=factory_id,
                                                                              id_resource=5).update(amount=new_mineral1)
                    elif warehouse.id_resource == 6:
                        warehouse = WarehouseFactoryResource.objects.filter(id_factory=factory_id,
                                                                              id_resource=6).update(amount=new_mineral2)
                    elif warehouse.id_resource == 7:
                        warehouse = WarehouseFactoryResource.objects.filter(id_factory=factory_id,
                                                                              id_resource=7).update(amount=new_mineral3)
                    elif warehouse.id_resource == 8:
                        warehouse = WarehouseFactoryResource.objects.filter(id_factory=factory_id,
                                                                              id_resource=8).update(amount=new_mineral4)

                user = MyUser.objects.filter(user_id=session_user).update(internal_currency=new_internal_currency)
                turn_productions = TurnProduction.objects.filter(user=session_user, user_city=session_user_city,
                                                                  factory_id=factory_id).last()
                if turn_productions is not None:
                    start_making = turn_productions.finish_time_production
                else:
                    start_making = datetime.now()
                build_time = factory_worker.time_production * int(amount_element)
                finish_making = start_making + timedelta(seconds=build_time)
                turn_production = TurnProduction(
                    user=session_user,
                    user_city=session_user_city,
                    factory_id=factory_id,
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
        return (message)
    else:
        message = 'Нехватает ресурсов'
    return (message)


def complex_production_module(*args):
    complex_id = args[0]
    factory_id = args[1]
    element_id = args[2]
    start_time_production = args[3]
    if start_time_production != 0:
        start_time_production = start_time_production
    else:
        start_time_production = datetime.now()
    manufacturing_complex = ManufacturingComplex.objects.filter(id=complex_id).first()
    user = MyUser.objects.filter(user_id=manufacturing_complex.user).first()
    warehouses = WarehouseComplex.objects.filter(id_complex=complex_id).order_by('id_resource')

    if warehouses:
        factory_worker = FactoryInstalled.objects.filter(id=factory_id).first()

        module_which_produces = 0
        if factory_worker.production_class == 1:
            module_which_produces = HullPattern.objects.filter(id=element_id).first()
        elif factory_worker.production_class == 2:
            module_which_produces = ArmorPattern.objects.filter(id=element_id).first()
        elif factory_worker.production_class == 3:
            module_which_produces = ShieldPattern.objects.filter(id=element_id).first()
        elif factory_worker.production_class == 4:
            module_which_produces = EnginePattern.objects.filter(id=element_id).first()
        elif factory_worker.production_class == 5:
            module_which_produces = GeneratorPattern.objects.filter(id=element_id).first()
        elif factory_worker.production_class == 6:
            module_which_produces = WeaponPattern.objects.filter(id=element_id).first()
        elif factory_worker.production_class == 7:
            module_which_produces = ShellPattern.objects.filter(id=element_id).first()
        elif factory_worker.production_class == 8:
            module_which_produces = ModulePattern.objects.filter(id=element_id).first()
        elif factory_worker.production_class == 9:
            module_which_produces = DevicePattern.objects.filter(id=element_id).first()
        elif factory_worker.production_class == 14:
            module_which_produces = FuelPattern.objects.filter(id=element_id).first()

        resource1 = 0
        resource2 = 0
        resource3 = 0
        resource4 = 0
        mineral1 = 0
        mineral2 = 0
        mineral3 = 0
        mineral4 = 0

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

        if user.internal_currency >= module_which_produces.price_internal_currency and \
                        resource1 >= module_which_produces.price_resource1 and \
                        resource2 >= module_which_produces.price_resource2 and \
                        resource3 >= module_which_produces.price_resource3 and \
                        resource4 >= module_which_produces.price_resource4 and \
                        mineral1 >= module_which_produces.price_mineral1 and \
                        mineral2 >= module_which_produces.price_mineral2 and \
                        mineral3 >= module_which_produces.price_mineral3 and \
                        mineral4 >= module_which_produces.price_mineral4:

            new_internal_currency = user.internal_currency - module_which_produces.price_internal_currency
            new_resource1 = resource1 - module_which_produces.price_resource1
            new_resource2 = resource2 - module_which_produces.price_resource2
            new_resource3 = resource3 - module_which_produces.price_resource3
            new_resource4 = resource4 - module_which_produces.price_resource4
            new_mineral1 = mineral1 - module_which_produces.price_mineral1
            new_mineral2 = mineral2 - module_which_produces.price_mineral2
            new_mineral3 = mineral3 - module_which_produces.price_mineral3
            new_mineral4 = mineral4 - module_which_produces.price_mineral4

            for warehouse in warehouses:
                if warehouse.id_resource == 1:
                    warehouse = WarehouseComplex.objects.filter(id_complex=complex_id, id_resource=1).update(
                        amount=new_resource1)
                elif warehouse.id_resource == 2:
                    warehouse = WarehouseComplex.objects.filter(id_complex=complex_id, id_resource=2).update(
                        amount=new_resource2)
                elif warehouse.id_resource == 3:
                    warehouse = WarehouseComplex.objects.filter(id_complex=complex_id, id_resource=3).update(
                        amount=new_resource3)
                elif warehouse.id_resource == 4:
                    warehouse = WarehouseComplex.objects.filter(id_complex=complex_id, id_resource=4).update(
                        amount=new_resource4)
                elif warehouse.id_resource == 5:
                    warehouse = WarehouseComplex.objects.filter(id_complex=complex_id, id_resource=5).update(
                        amount=new_mineral1)
                elif warehouse.id_resource == 6:
                    warehouse = WarehouseComplex.objects.filter(id_complex=complex_id, id_resource=6).update(
                        amount=new_mineral2)
                elif warehouse.id_resource == 7:
                    warehouse = WarehouseComplex.objects.filter(id_complex=complex_id, id_resource=7).update(
                        amount=new_mineral3)
                elif warehouse.id_resource == 8:
                    warehouse = WarehouseComplex.objects.filter(id_complex=complex_id, id_resource=8).update(
                        amount=new_mineral4)

            user = MyUser.objects.filter(user_id=manufacturing_complex.user).update(
                internal_currency=new_internal_currency)

            turn_production = TurnComplexProduction(
                complex_id=complex_id,
                factory_id=factory_id,
                element_id=element_id,
                start_time_production=start_time_production,
                time=factory_worker.time_production
            )
            turn_production.save()
            message = 0
        else:
            message = 1
        return (message)
    else:
        message = 1
    return message