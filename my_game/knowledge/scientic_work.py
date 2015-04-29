# -*- coding: utf-8 -*-

import math

from datetime import datetime, timedelta

from my_game.models import MyUser, Warehouse
from my_game.models import Basic_scientic, Turn_scientic



def scien_up(*args):
    session_user = args[0]
    level_up = int(args[1])
    scientic = int(args[2])
    session_user_city = int(args[3])
    number_scientic = len(Turn_scientic.objects.filter(user=session_user))
    if number_scientic < 3:
        warehouses = Warehouse.objects.filter(user=session_user, user_city = session_user_city).order_by('id_resource')
        user = MyUser.objects.filter(user_id = session_user).first()

        scien = Basic_scientic.objects.get(scientic_id=scientic)
        time_studys = int(scien.time_study)
        if level_up == 1:
            time_study_turn = time_studys
            cost_study_internal_currency = int(scien.cost_internal_currency)
            cost_study_resource1 = int(scien.cost_resource1)
            cost_study_resource2 = int(scien.cost_resource2)
            cost_study_resource3 = int(scien.cost_resource3)
            cost_study_resource4 = int(scien.cost_resource4)
            cost_study_mineral1 = int(scien.cost_mineral1)
            cost_study_mineral2 = int(scien.cost_mineral2)
            cost_study_mineral3 = int(scien.cost_mineral3)
            cost_study_mineral4 = int(scien.cost_mineral4)
        else:
            time_study_turn = int(time_studys * int(math.exp(level_up) / 5))
            cost_study_internal_currency = int(scien.cost_internal_currency * math.exp(level_up) / 5)
            cost_study_resource1 = int(scien.cost_resource1 * math.exp(level_up) / 5)
            cost_study_resource2 = int(scien.cost_resource2 * math.exp(level_up) / 5)
            cost_study_resource3 = int(scien.cost_resource3 * math.exp(level_up) / 5)
            cost_study_resource4 = int(scien.cost_resource4 * math.exp(level_up) / 5)
            cost_study_mineral1 = int(scien.cost_mineral1 * math.exp(level_up) / 5)
            cost_study_mineral2 = int(scien.cost_mineral2 * math.exp(level_up) / 5)
            cost_study_mineral3 = int(scien.cost_mineral3 * math.exp(level_up) / 5)
            cost_study_mineral4 = int(scien.cost_mineral4 * math.exp(level_up) / 5)

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

        if user.internal_currency >= cost_study_internal_currency and resource1 >= cost_study_resource1 and \
                        resource2 >= cost_study_resource2 and \
                        resource3 >= cost_study_resource3 and resource4 >= cost_study_resource4 and \
                        mineral1 >= cost_study_mineral1 and mineral2 >= cost_study_mineral2 and \
                        mineral3 >= cost_study_mineral3 and mineral4 >= cost_study_mineral4:
            new_internal_currency = user.internal_currency - cost_study_internal_currency
            new_resource1 = resource1 - cost_study_resource1
            new_resource2 = resource2 - cost_study_resource2
            new_resource3 = resource3 - cost_study_resource3
            new_resource4 = resource4 - cost_study_resource4
            new_mineral1 = mineral1 - cost_study_mineral1
            new_mineral2 = mineral2 - cost_study_mineral2
            new_mineral3 = mineral3 - cost_study_mineral3
            new_mineral4 = mineral4 - cost_study_mineral4

            for warehouse in warehouses:
                if warehouse.id_resource == 1:
                    warehouse = Warehouse.objects.filter(user=session_user, user_city = session_user_city, id_resource = 1).update(amount=new_resource1)
                elif warehouse.id_resource == 2:
                    warehouse = Warehouse.objects.filter(user=session_user, user_city = session_user_city, id_resource = 2).update(amount=new_resource2)
                elif warehouse.id_resource == 3:
                    warehouse = Warehouse.objects.filter(user=session_user, user_city = session_user_city, id_resource = 3).update(amount=new_resource3)
                elif warehouse.id_resource == 4:
                    warehouse = Warehouse.objects.filter(user=session_user, user_city = session_user_city, id_resource = 4).update(amount=new_resource4)
                elif warehouse.id_resource == 5:
                    warehouse = Warehouse.objects.filter(user=session_user, user_city = session_user_city, id_resource = 5).update(amount=new_mineral1)
                elif warehouse.id_resource == 6:
                    warehouse = Warehouse.objects.filter(user=session_user, user_city = session_user_city, id_resource = 6).update(amount=new_mineral2)
                elif warehouse.id_resource == 7:
                    warehouse = Warehouse.objects.filter(user=session_user, user_city = session_user_city, id_resource = 7).update(amount=new_mineral3)
                elif warehouse.id_resource == 8:
                    warehouse = Warehouse.objects.filter(user=session_user, user_city = session_user_city, id_resource = 8).update(amount=new_mineral4)
            user = MyUser.objects.filter(user_id = session_user).update(internal_currency = new_internal_currency)

            turn_scientic = Turn_scientic.objects.filter(user=session_user).last()
            if turn_scientic:
                finish_time = turn_scientic.finish_time_science + timedelta(seconds=time_study_turn)
            else:
                finish_time = datetime.now() + timedelta(seconds=time_study_turn)

            if scientic == 1:
                turn_scientic = Turn_scientic(
                    user=session_user,
                    mathematics_up=level_up,
                    start_time_science=datetime.now(),
                    finish_time_science=finish_time,
                )
            if scientic == 2:
                turn_scientic = Turn_scientic(
                    user=session_user,
                    phisics_up=level_up,
                    start_time_science=datetime.now(),
                    finish_time_science=finish_time,
                )
            if scientic == 3:
                turn_scientic = Turn_scientic(
                    user=session_user,
                    biologic_chimics_up=level_up,
                    start_time_science=datetime.now(),
                    finish_time_science=finish_time,
                )
            if scientic == 4:
                turn_scientic = Turn_scientic(
                    user=session_user,
                    energetics_up=level_up,
                    start_time_science=datetime.now(),
                    finish_time_science=finish_time,
                )
            if scientic == 5:
                turn_scientic = Turn_scientic(
                    user=session_user,
                    radionics_up=level_up,
                    start_time_science=datetime.now(),
                    finish_time_science=finish_time,
                )
            if scientic == 6:
                turn_scientic = Turn_scientic(
                    user=session_user,
                    nanotech_up=level_up,
                    start_time_science=datetime.now(),
                    finish_time_science=finish_time,
                )
            if scientic == 7:
                turn_scientic = Turn_scientic(
                    user=session_user,
                    astronomy_up=level_up,
                    start_time_science=datetime.now(),
                    finish_time_science=finish_time,
                )
            if scientic == 8:
                turn_scientic = Turn_scientic(
                    user=session_user,
                    logistic_up=level_up,
                    start_time_science=datetime.now(),
                    finish_time_science=finish_time,
                )
            turn_scientic.save()