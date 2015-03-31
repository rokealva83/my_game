# -*- coding: utf-8 -*-

from datetime import datetime
from my_game.models import MyUser, User_city
from my_game.models import Factory_pattern, Factory_installed,  Building_installed
from my_game.models import Warehouse


def verification_of_resources(*args):
    arg = args
    user = arg[0]
    elapsed_time_seconds = arg[1]
    time_update = arg[2]
    tax = 0.01
    user_citys = User_city.objects.filter(user=user)
    for user_city in user_citys:
        city_id = user_city.id
        check_user_factory_resourse_city = Factory_installed.objects.filter(user=user, user_city=city_id,
                                                                            production_class=11)
        attributes = ['resource1', 'resource2', 'resource3', 'resource4', 'mineral1', 'mineral2', 'mineral3',
                      'mineral4']
        prod_id = 1
        for attribute in attributes:
            check_factorys = check_user_factory_resourse_city.filter(production_id=prod_id)
            resourse = 0

            for check_factory in check_factorys:
                resourse = resourse + elapsed_time_seconds / check_factory.time_production
            warehouse = Warehouse.objects.filter(user=user, user_city=city_id, id_resource=prod_id).first()
            new_resourse = warehouse.amount + resourse
            warehouse = Warehouse.objects.filter(user=user, user_city=city_id, id_resource=prod_id).update(
                amount=new_resourse)
            prod_id = prod_id + 1

        population = 0
        population_buildings = Factory_installed.objects.filter(user=user, user_city=city_id, production_class=10)
        for population_building in population_buildings:
            population = population + elapsed_time_seconds / population_building.time_production

        new_population = user_city.population + population
        if new_population > user_city.max_population:
            new_population = user_city.max_population
        user_city = User_city.objects.filter(id=city_id).update(population=new_population)

        check_all_user_factorys = Factory_installed.objects.filter(user=user, user_city=city_id)
        total_number_specialists = 0
        for check_all_user_factory in check_all_user_factorys:
            install_factory = Factory_pattern.objects.filter(id=check_all_user_factory.factory_pattern_id).first()
            total_number_specialists = total_number_specialists + install_factory.cost_expert_deployment
        increase_internal_currency = total_number_specialists * elapsed_time_seconds * tax
        new_internal_currency = MyUser.objects.get(user_id=user).internal_currency + increase_internal_currency
        money = MyUser.objects.filter(user_id=user).update(internal_currency=new_internal_currency)

        trade_building = Building_installed.objects.filter(user=user, user_city=city_id, production_class=13).first()
        if trade_building:
            if trade_building.max_warehouse > trade_building.warehouse:
                energy = elapsed_time_seconds / trade_building.time_production
                stock_energy = trade_building.warehouse
                new_energy = stock_energy + energy
                if new_energy > trade_building.max_warehouse:
                    new_energy = trade_building.max_warehouse
                trade_building = Building_installed.objects.filter(user=user, user_city=city_id,
                                                                   production_class=13).update(warehouse=new_energy)

    last_time_update = time_update
    last_time_scan_scient = datetime(last_time_update.year, last_time_update.month, last_time_update.day, 0, 0, 0,
                                     0)
    MyUser.objects.filter(user_id=user).update(last_time_check=last_time_update,
                                               last_time_scan_scient=last_time_scan_scient)



































