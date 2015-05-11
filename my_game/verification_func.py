# -*- coding: utf-8 -*-

from django.utils import timezone
from my_game.models import MyUser, User_city
from my_game.models import Factory_pattern, Factory_installed, Building_installed
from my_game.models import Warehouse
from my_game.models import Manufacturing_complex, Warehouse_complex


def verification_of_resources(request):
    user = request
    city_id = 0
    user_city = 0
    tax = 0.01
    now_date = timezone.now()
    time_update = MyUser.objects.filter(user_id=user).first().last_time_check
    elapsed_time_full = now_date - time_update
    elapsed_time_seconds = elapsed_time_full.seconds
    time_update = now_date
    if elapsed_time_seconds > 300:
        user_citys = User_city.objects.filter(user=user)
        for user_city in user_citys:
            city_id = user_city.id
            check_user_factory_resourse_city = Factory_installed.objects.filter(user=user, user_city=city_id,
                                                                                production_class=11)
            attributes = ['resource1', 'resource2', 'resource3', 'resource4', 'mineral1', 'mineral2', 'mineral3',
                          'mineral4']
            prod_id = 1
            for attribute in attributes:
                check_factorys = check_user_factory_resourse_city.filter(production_id=prod_id, complex_status=0)
                resourse = 0
                for check_factory in check_factorys:
                    resourse = resourse + elapsed_time_seconds / check_factory.time_production
                warehouse = Warehouse.objects.filter(user=user, user_city=city_id, id_resource=prod_id).first()
                new_resourse = warehouse.amount + resourse
                warehouse = Warehouse.objects.filter(user=user, user_city=city_id, id_resource=prod_id).update(
                    amount=new_resourse)
                user_complexs = Manufacturing_complex.objects.filter(user_city=user_city.id)
                for user_complex in user_complexs:
                    complex_id = user_complex.id
                    check_complex_factorys = check_user_factory_resourse_city.filter(production_id=prod_id,
                                                                                     complex_status=1,
                                                                                     complex_id=user_complex.id)
                    if check_complex_factorys:
                        for check_complex_factory in check_complex_factorys:
                            resourse = resourse + elapsed_time_seconds / check_complex_factory.time_production
                        koef = 1.0 - user_complex.extraction_parametr / 100.0
                        complex_resource = resourse * koef
                        complex_warehouse = Warehouse_complex.objects.filter(id_complex=complex_id,
                                                                             id_resource=prod_id).first()
                        if complex_warehouse:
                            complex_resource = complex_resource + complex_warehouse.amount
                            complex_warehouse = Warehouse_complex.objects.filter(id_complex=complex_id,
                                                                                 id_resource=prod_id).update(
                                amount=complex_resource)
                        else:
                            complex_warehouse = Warehouse_complex(
                                id_complex=complex_id,
                                id_resource=prod_id,
                                amount=complex_resource
                            )
                            complex_warehouse.save()
                        warehouse_resource = resourse * user_complex.extraction_parametr / 100.0
                        if warehouse_resource != 0:
                            warehouse = Warehouse.objects.filter(user=user, user_city=city_id,
                                                                 id_resource=prod_id).first()
                            new_resourse = warehouse.amount + warehouse_resource
                            warehouse = Warehouse.objects.filter(user=user, user_city=city_id,
                                                                 id_resource=prod_id).update(
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
            if install_factory:
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
        MyUser.objects.filter(user_id=user).update(last_time_check=last_time_update)



































