# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from my_game.models import TurnProduction, FuelPattern


def production_fuel(*args):
    session_user = args[0]
    session_user_city = args[1]
    factory = args[2]
    element_id = args[3]
    amount_element = args[4]
    module_which_produces = FuelPattern.objects.filter(id=element_id).first()
    warehouse = factory.factory_warehouse
    if session_user.internal_currency >= module_which_produces.price_internal_currency * int(amount_element) \
            and warehouse.res_veriarit >= module_which_produces.price_veriarit * int(amount_element) \
            and warehouse.res_inneilit >= module_which_produces.price_inneilit * int(amount_element) \
            and warehouse.res_renniit >= module_which_produces.price_renniit * int(amount_element) \
            and warehouse.res_cobalt >= module_which_produces.price_cobalt * int(amount_element) \
            and warehouse.mat_chemical >= module_which_produces.price_chemical * int(amount_element):

        new_internal_currency = session_user.internal_currency - (
            module_which_produces.price_internal_currency * int(amount_element))
        new_res_veriarit = warehouse.res_veriarit - module_which_produces.price_veriarit * int(amount_element)
        new_res_inneilit = warehouse.res_inneilit - module_which_produces.price_inneilit * int(amount_element)
        new_res_renniit = warehouse.res_renniit - module_which_produces.price_renniit * int(amount_element)
        new_res_cobalt = warehouse.res_cobalt - module_which_produces.price_cobalt * int(amount_element)
        new_chemical = warehouse.mat_chemical - module_which_produces.price_chemical * int(amount_element)

        setattr(warehouse, 'res_veriarit', new_res_veriarit)
        setattr(warehouse, 'res_inneilit', new_res_inneilit)
        setattr(warehouse, 'res_renniit', new_res_renniit)
        setattr(warehouse, 'res_cobalt', new_res_cobalt)
        setattr(warehouse, 'mat_chemical', new_chemical)
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
            element_id=module_which_produces.id,
            start_time_production=start_making,
            finish_time_production=finish_making,
            amount_element=amount_element
        )
        turn_production.save()
        message = 'Производство начато'
    else:
        message = 'Нехватает ресурсов'
    return message
