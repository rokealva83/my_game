# -*- coding: utf-8 -*-

import math
from datetime import datetime, timedelta
from my_game.models import BasicScientic, TurnScientic


def scien_up(*args):
    session_user = args[0]
    level_up = int(args[1])
    scientic = int(args[2])
    session_user_city = args[3]
    number_scientic = len(TurnScientic.objects.filter(user=session_user))

    if number_scientic < 3:
        warehouse = session_user_city.warehouse

        science = BasicScientic.objects.get(scientic_id=scientic)
        time_studys = int(science.time_study)
        if level_up == 1:
            time_study_turn = time_studys
            cost_study_internal_currency = int(science.price_internal_currency)
            cost_study_nickel = int(science.price_nickel)
            cost_study_iron = int(science.price_iron)
            cost_study_cooper = int(science.price_cooper)
            cost_study_aluminum = int(science.price_aluminum)
            cost_study_veriarit = int(science.price_veriarit)
            cost_study_inneilit = int(science.price_inneilit)
            cost_study_renniit = int(science.price_renniit)
            cost_study_cobalt = int(science.price_cobalt)
        else:
            time_study_turn = int(time_studys * int(math.exp(level_up) / 5))
            cost_study_internal_currency = int(science.price_internal_currency * math.exp(level_up) / 5)
            cost_study_nickel = int(science.price_nickel * math.exp(level_up) / 5)
            cost_study_iron = int(science.price_iron * math.exp(level_up) / 5)
            cost_study_cooper = int(science.price_cooper * math.exp(level_up) / 5)
            cost_study_aluminum = int(science.price_aluminum * math.exp(level_up) / 5)
            cost_study_veriarit = int(science.price_veriarit * math.exp(level_up) / 5)
            cost_study_inneilit = int(science.price_inneilit * math.exp(level_up) / 5)
            cost_study_renniit = int(science.price_renniit * math.exp(level_up) / 5)
            cost_study_cobalt = int(science.price_cobalt * math.exp(level_up) / 5)

        if session_user.internal_currency >= cost_study_internal_currency and \
                        warehouse.res_nickel >= cost_study_nickel and \
                        warehouse.res_iron >= cost_study_iron and \
                        warehouse.res_cooper >= cost_study_cooper and \
                        warehouse.res_aluminum >= cost_study_aluminum and \
                        warehouse.res_veriarit >= cost_study_veriarit and \
                        warehouse.res_inneilit >= cost_study_inneilit and \
                        warehouse.res_renniit >= cost_study_renniit and \
                        warehouse.res_cobalt >= cost_study_cobalt:
            new_internal_currency = session_user.internal_currency - cost_study_internal_currency
            new_nickel = warehouse.res_nickel - cost_study_nickel
            new_iron = warehouse.res_iron - cost_study_iron
            new_cooper = warehouse.res_cooper - cost_study_cooper
            new_aluminum = warehouse.res_aluminum - cost_study_aluminum
            new_veriarit = warehouse.res_veriarit - cost_study_veriarit
            new_inneilit = warehouse.res_inneilit - cost_study_inneilit
            new_renniit = warehouse.res_renniit - cost_study_renniit
            new_cobalt = warehouse.res_cobalt - cost_study_cobalt

            setattr(warehouse, 'res_nickel', new_nickel)
            setattr(warehouse, 'res_iron', new_iron)
            setattr(warehouse, 'res_cooper', new_cooper)
            setattr(warehouse, 'res_aluminum', new_aluminum)
            setattr(warehouse, 'res_veriarit', new_veriarit)
            setattr(warehouse, 'res_inneilit', new_inneilit)
            setattr(warehouse, 'res_renniit', new_renniit)
            setattr(warehouse, 'res_cobalt', new_cobalt)
            warehouse.save()

            setattr(session_user, 'internal_currency', new_internal_currency)
            session_user.save()

            turn_scientic = TurnScientic.objects.filter(user=session_user).last()
            if turn_scientic:
                finish_time = turn_scientic.finish_time_science + timedelta(seconds=time_study_turn)
            else:
                finish_time = datetime.now() + timedelta(seconds=time_study_turn)

            if scientic == 1:
                turn_scientic = TurnScientic(
                    user=session_user,
                    mathematics_up=level_up,
                    start_time_science=datetime.now(),
                    finish_time_science=finish_time,
                )
            if scientic == 2:
                turn_scientic = TurnScientic(
                    user=session_user,
                    phisics_up=level_up,
                    start_time_science=datetime.now(),
                    finish_time_science=finish_time,
                )
            if scientic == 3:
                turn_scientic = TurnScientic(
                    user=session_user,
                    biologic_chimics_up=level_up,
                    start_time_science=datetime.now(),
                    finish_time_science=finish_time,
                )
            if scientic == 4:
                turn_scientic = TurnScientic(
                    user=session_user,
                    energetics_up=level_up,
                    start_time_science=datetime.now(),
                    finish_time_science=finish_time,
                )
            if scientic == 5:
                turn_scientic = TurnScientic(
                    user=session_user,
                    radionics_up=level_up,
                    start_time_science=datetime.now(),
                    finish_time_science=finish_time,
                )
            if scientic == 6:
                turn_scientic = TurnScientic(
                    user=session_user,
                    nanotech_up=level_up,
                    start_time_science=datetime.now(),
                    finish_time_science=finish_time,
                )
            if scientic == 7:
                turn_scientic = TurnScientic(
                    user=session_user,
                    astronomy_up=level_up,
                    start_time_science=datetime.now(),
                    finish_time_science=finish_time,
                )
            if scientic == 8:
                turn_scientic = TurnScientic(
                    user=session_user,
                    logistic_up=level_up,
                    start_time_science=datetime.now(),
                    finish_time_science=finish_time,
                )
            turn_scientic.save()
