# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from my_game.models import MyUser
from my_game.models import Turn_production
from my_game.models import Hull_pattern, Shell_pattern, Shield_pattern, Generator_pattern, Engine_pattern, \
    Armor_pattern, Module_pattern, Weapon_pattern, Factory_installed
from my_game.models import Warehouse



def rename_element_pattern(*args):
    session_user = args[0]
    session_user_city = args[1]
    pattern_id = args[2]
    element_id = args[3]
    new_names = args[4]
    factory = Factory_installed.objects.filter(id=pattern_id).first()
    production_class = factory.production_class
    if production_class == 1:
        new_name = Hull_pattern.objects.filter(id=element_id).update(name=new_names)
    if production_class == 2:
        new_name = Armor_pattern.objects.filter(id=element_id).update(name=new_names)
    if production_class == 3:
        new_name = Shield_pattern.objects.filter(id=element_id).update(name=new_names)
    if production_class == 4:
        new_name = Engine_pattern.objects.filter(id=element_id).update(name=new_names)
    if production_class == 5:
        new_name = Generator_pattern.objects.filter(id=element_id).update(name=new_names)
    if production_class == 6:
        new_name = Weapon_pattern.objects.filter(id=element_id).update(name=new_names)
    if production_class == 7:
        new_name = Shell_pattern.objects.filter(id=element_id).update(name=new_names)
    if production_class == 8:
        new_name = Module_pattern.objects.filter(id=element_id).update(name=new_names)
        # if production_class == 9:
    # new_name = Device_pattern.objects.filter(id = element_id).update(name = new_name)
    message = 'Модуль переименован'
    return (message)


def production_module(*args):
    session_user = args[0]
    session_user_city = args[1]
    factory_id = args[2]
    element_id = args[3]
    amount_element = args[4]

    user = MyUser.objects.filter(user_id=session_user).first()
    warehouses = Warehouse.objects.filter(user=session_user, user_city = session_user_city).order_by('id_resource')
    factory_worker = Factory_installed.objects.filter(id=factory_id).first()
    len_turn_production = len(Turn_production.objects.filter(user=session_user, user_city=session_user_city, \
                                                             factory_id=factory_worker.id))
    module_which_produces = 0
    if len_turn_production < 1:
        if factory_worker.production_class == 1:
            module_which_produces = Hull_pattern.objects.filter(id=element_id).first()
        if factory_worker.production_class == 2:
            module_which_produces = Armor_pattern.objects.filter(id=element_id).first()
        if factory_worker.production_class == 3:
            module_which_produces = Shield_pattern.objects.filter(id=element_id).first()
        if factory_worker.production_class == 4:
            module_which_produces = Engine_pattern.objects.filter(id=element_id).first()
        if factory_worker.production_class == 5:
            module_which_produces = Generator_pattern.objects.filter(id=element_id).first()
        if factory_worker.production_class == 6:
            module_which_produces = Weapon_pattern.objects.filter(id=element_id).first()
        if factory_worker.production_class == 7:
            module_which_produces = Shell_pattern.objects.filter(id=element_id).first()
        if factory_worker.production_class == 8:
            module_which_produces = Module_pattern.objects.filter(id=element_id).first()
#        if factory_worker.production_class == 9:
#            module_which_produces = Device_pattern.objects.filter(id=element_id).first()



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

            new_internal_currency = user.internal_currency - module_which_produces.price_internal_currency * int(amount_element)
            new_resource1 = resource1 - module_which_produces.price_resource1 * int(amount_element)
            new_resource2 = resource2 - module_which_produces.price_resource1 * int(amount_element)
            new_resource3 = resource3 - module_which_produces.price_resource1 * int(amount_element)
            new_resource4 = resource4 - module_which_produces.price_resource1 * int(amount_element)
            new_mineral1 = mineral1 - module_which_produces.price_mineral1 * int(amount_element)
            new_mineral2 = mineral2 - module_which_produces.price_mineral1 * int(amount_element)
            new_mineral3 = mineral3 - module_which_produces.price_mineral1 * int(amount_element)
            new_mineral4 = mineral4 - module_which_produces.price_mineral1 *int(amount_element)

            for warehouse in warehouses:
                if warehouse.id_resource == 1:
                    warehouse = Warehouse.objects.filter(user=session_user, user_city = session_user_city).update(resource1=new_resource1)
                elif warehouse.id_resource == 2:
                    warehouse = Warehouse.objects.filter(user=session_user, user_city = session_user_city).update(resource2=new_resource2)
                elif warehouse.id_resource == 3:
                    warehouse = Warehouse.objects.filter(user=session_user, user_city = session_user_city).update(resource3=new_resource3)
                elif warehouse.id_resource == 4:
                    warehouse = Warehouse.objects.filter(user=session_user, user_city = session_user_city).update(resource4=new_resource4)
                elif warehouse.id_resource == 5:
                    warehouse = Warehouse.objects.filter(user=session_user, user_city = session_user_city).update(mineral1=new_mineral1)
                elif warehouse.id_resource == 6:
                    warehouse = Warehouse.objects.filter(user=session_user, user_city = session_user_city).update(mineral2=new_mineral2)
                elif warehouse.id_resource == 7:
                    warehouse = Warehouse.objects.filter(user=session_user, user_city = session_user_city).update(mineral3=new_mineral3)
                elif warehouse.id_resource == 8:
                    warehouse = Warehouse.objects.filter(user=session_user, user_city = session_user_city).update(mineral4=new_mineral4)


            user = MyUser.objects.filter(user_id=session_user).update(internal_currency=new_internal_currency)
            turn_productions = Turn_production.objects.filter(user=session_user, user_city=session_user_city,
                                                              factory_id=factory_id).last()
            if turn_productions is not None:
                start_making = turn_productions.finish_time_production
            else:
                start_making = datetime.now()
            build_time = factory_worker.time_production * int(amount_element)
            finish_making = start_making + timedelta(seconds=build_time)
            turn_production = Turn_production(
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