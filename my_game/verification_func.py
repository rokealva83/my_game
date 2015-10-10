# -*- coding: utf-8 -*-

from django.utils import timezone
from my_game.models import MyUser, UserCity
from my_game.models import FactoryInstalled, BuildingInstalled
from my_game.models import Warehouse
from my_game.models import ManufacturingComplex, WarehouseComplex


def verification_of_resources(request):
    user = request
    user_city = 0
    tax = 0.01
    now_date = timezone.now()
    time_update = user.last_time_check
    elapsed_time_full = now_date - time_update
    elapsed_time_seconds = elapsed_time_full.seconds
    time_update = now_date
    if elapsed_time_seconds > 300:
        user_citys = UserCity.objects.filter(user=user)
        for user_city in user_citys:
            check_user_factory_resourse_city = FactoryInstalled.objects.filter(user=user, user_city=user_city,
                                                                               production_class=11)
            attributes = ['resource1', 'resource2', 'resource3', 'resource4', 'mineral1', 'mineral2', 'mineral3',
                          'mineral4']
            prod_id = 1
            for attribute in attributes:
                check_factorys = check_user_factory_resourse_city.filter(production_id=prod_id, complex_status=0)
                resourse = 0
                for check_factory in check_factorys:
                    resourse = resourse + elapsed_time_seconds / check_factory.time_production
                warehouse = Warehouse.objects.filter(user=user, user_city=user_city, resource_id=prod_id).first()
                new_resourse = warehouse.amount + resourse
                warehouse = Warehouse.objects.filter(user=user, user_city=user_city, resource_id=prod_id).update(
                    amount=new_resourse)
                user_complexs = ManufacturingComplex.objects.filter(user_city=user_city)
                for user_complex in user_complexs:
                    check_complex_factorys = check_user_factory_resourse_city.filter(production_id=prod_id,
                                                                                     complex_status=1,
                                                                                     complex=user_complex)
                    if check_complex_factorys:
                        for check_complex_factory in check_complex_factorys:
                            resourse = resourse + elapsed_time_seconds / check_complex_factory.time_production
                        koef = 1.0 - user_complex.extraction_parametr / 100.0
                        complex_resource = resourse * koef
                        complex_warehouse = WarehouseComplex.objects.filter(complex=complex,
                                                                            resource_id=prod_id).first()
                        if complex_warehouse:
                            complex_resource = complex_resource + complex_warehouse.amount
                            complex_warehouse = WarehouseComplex.objects.filter(complex=complex,
                                                                                resource_id=prod_id).update(
                                amount=complex_resource)
                        else:
                            complex_warehouse = WarehouseComplex(
                                complex=complex,
                                resource_id=prod_id,
                                amount=complex_resource
                            )
                            complex_warehouse.save()
                        warehouse_resource = resourse * user_complex.extraction_parametr / 100.0
                        if warehouse_resource != 0:
                            warehouse = Warehouse.objects.filter(user=user, user_city=user_city,
                                                                 resource_id=prod_id).first()
                            new_resourse = warehouse.amount + warehouse_resource
                            warehouse = Warehouse.objects.filter(user=user, user_city=user_city,
                                                                 resource_id=prod_id).update(
                                amount=new_resourse)
                prod_id = prod_id + 1

        population = 0
        population_buildings = FactoryInstalled.objects.filter(user=user, user_city=user_city, production_class=10)
        for population_building in population_buildings:
            population = population + elapsed_time_seconds / population_building.time_production

        new_population = user_city.population + population
        if new_population > user_city.max_population:
            new_population = user_city.max_population
        user_city_update = UserCity.objects.filter(id=user_city.id).update(population=new_population)

        check_all_user_factorys = FactoryInstalled.objects.filter(user=user, user_city=user_city)
        total_number_specialists = 0
        for check_all_user_factory in check_all_user_factorys:
            install_factory = check_all_user_factory
            if install_factory:
                total_number_specialists = total_number_specialists + install_factory.cost_expert_deployment
        increase_internal_currency = total_number_specialists * elapsed_time_seconds * tax
        new_internal_currency = user.internal_currency + increase_internal_currency
        money = MyUser.objects.filter(user=user.id).update(internal_currency=new_internal_currency)

        trade_building = BuildingInstalled.objects.filter(user=user, user_city=user_city, production_class=13).first()
        if trade_building:
            if trade_building.max_warehouse > trade_building.warehouse:
                energy = elapsed_time_seconds / trade_building.time_production
                stock_energy = trade_building.warehouse
                new_energy = stock_energy + energy
                if new_energy > trade_building.max_warehouse:
                    new_energy = trade_building.max_warehouse
                trade_building = BuildingInstalled.objects.filter(user=user, user_city=user_city,
                                                                  production_class=13).update(warehouse=new_energy)

        last_time_update = time_update
        MyUser.objects.filter(user_id=user.id).update(last_time_check=last_time_update)
