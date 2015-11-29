# -*- coding: utf-8 -*-

from django.utils import timezone
from my_game.models import MyUser, UserCity
from my_game.models import FactoryInstalled, BuildingInstalled
from my_game.models import Warehouse
from my_game.models import ManufacturingComplex, WarehouseComplex
from my_game.models import UserVariables


def verification_of_resources(request):
    user = request
    now_date = timezone.now()
    time_update = user.last_time_check
    elapsed_time_full = now_date - time_update
    elapsed_time_seconds = elapsed_time_full.seconds
    time_update = now_date
    user_variables = UserVariables.objects.first()
    if elapsed_time_seconds > 300:
        user_citys = UserCity.objects.filter(user=user)
        for user_city in user_citys:
            check_user_factory_resourse_city = FactoryInstalled.objects.filter(user=user, user_city=user_city,
                                                                               production_class=11)
            production_id = 1
            res_nickel = res_iron = res_cooper = res_aluminum = res_variarit = res_inneilit = res_renniit = \
                res_cobalt = mat_construction_material = mat_chemical = mat_high_strength_allov = mat_nanoelement = \
                mat_microprocessor_element = mat_fober_optic_element = complex_res_nickel = complex_res_iron = \
                complex_res_cooper = complex_res_aluminum = complex_res_variarit = complex_res_inneilit = \
                complex_res_renniit = complex_res_cobalt = complex_mat_construction_material = complex_mat_chemical = \
                complex_mat_high_strength_allov = complex_mat_nanoelement = complex_mat_microprocessor_element = \
                complex_mat_fober_optic_element = 0
            while production_id < 14:
                check_factorys = check_user_factory_resourse_city.filter(production_id=production_id, complex_status=0)
                resourse = 0
                warehouse = user_city.warehouse
                for check_factory in check_factorys:
                    resourse = resourse + elapsed_time_seconds / check_factory.factory_pattern.time_production
                if production_id == 1:
                    res_nickel = resourse + warehouse.res_nickel
                elif production_id == 2:
                    res_iron = resourse + warehouse.res_iron
                elif production_id == 3:
                    res_cooper = resourse + warehouse.res_cooper
                elif production_id == 4:
                    res_aluminum = resourse + warehouse.res_aluminum
                elif production_id == 5:
                    res_variarit = resourse + warehouse.res_variarit
                elif production_id == 6:
                    res_inneilit = resourse + warehouse.res_inneilit
                elif production_id == 7:
                    res_renniit = resourse + warehouse.res_renniit
                elif production_id == 8:
                    res_cobalt = resourse + warehouse.res_cobalt
                elif production_id == 9:
                    mat_construction_material = resourse + warehouse.mat_construction_material
                elif production_id == 10:
                    mat_chemical = resourse + warehouse.mat_chemical
                elif production_id == 11:
                    mat_high_strength_allov = resourse + warehouse.mat_high_strength_allov
                elif production_id == 12:
                    mat_nanoelement = resourse + warehouse.mat_nanoelement
                elif production_id == 13:
                    mat_microprocessor_element = resourse + warehouse.mat_microprocessor_element
                elif production_id == 14:
                    mat_fober_optic_element = resourse

                user_complexes = ManufacturingComplex.objects.filter(user_city=user_city)
                for user_complex in user_complexes:
                    check_complex_factorys = check_user_factory_resourse_city.filter(production_id=production_id,
                                                                                     complex_status=1,
                                                                                     complex=user_complex)
                    if check_complex_factorys:
                        for check_complex_factory in check_complex_factorys:
                            resourse = resourse + elapsed_time_seconds / check_complex_factory.time_production

                        koef = 1.0 - user_complex.extraction_parametr / 100.0
                        warehouse_complex = user_complex.warehouse_complex
                        if production_id == 1:
                            complex_res_nickel = resourse * koef
                            res_nickel = res_nickel + resourse - complex_res_nickel
                        elif production_id == 2:
                            complex_res_iron = resourse * koef
                            res_iron = res_iron + resourse - complex_res_iron
                        elif production_id == 3:
                            complex_res_cooper = resourse * koef
                            res_cooper = res_cooper + resourse - complex_res_cooper
                        elif production_id == 4:
                            complex_res_aluminum = resourse * koef
                            res_aluminum = res_aluminum + resourse - complex_res_aluminum
                        elif production_id == 5:
                            complex_res_variarit = resourse * koef
                            res_variarit = res_variarit + resourse - complex_res_variarit
                        elif production_id == 6:
                            complex_res_inneilit = resourse * koef
                            res_inneilit = res_inneilit + resourse - complex_res_inneilit
                        elif production_id == 7:
                            complex_res_renniit = resourse * koef
                            res_renniit = res_renniit + resourse - complex_res_renniit
                        elif production_id == 8:
                            complex_res_cobalt = resourse * koef
                            res_cobalt = res_cobalt + resourse - complex_res_cobalt
                        elif production_id == 9:
                            complex_mat_construction_material = resourse * koef
                            mat_construction_material = mat_construction_material + resourse - complex_mat_construction_material
                        elif production_id == 10:
                            complex_mat_chemical = resourse * koef
                            mat_chemical = mat_chemical + resourse - complex_mat_chemical
                        elif production_id == 11:
                            complex_mat_high_strength_allov = resourse * koef
                            mat_high_strength_allov = mat_high_strength_allov + resourse - complex_mat_high_strength_allov
                        elif production_id == 12:
                            complex_mat_nanoelement = resourse * koef
                            mat_nanoelement = mat_nanoelement + resourse - complex_mat_nanoelement
                        elif production_id == 13:
                            complex_mat_microprocessor_element = resourse * koef
                            mat_microprocessor_element = mat_microprocessor_element + resourse - complex_mat_microprocessor_element
                        elif production_id == 14:
                            complex_mat_fober_optic_element = resourse * koef
                            mat_fober_optic_element = mat_fober_optic_element + resourse - complex_mat_fober_optic_element

                    setattr(warehouse_complex, 'res_nickel', complex_res_nickel)
                    setattr(warehouse_complex, 'res_iron', complex_res_iron)
                    setattr(warehouse_complex, 'res_cooper', complex_res_cooper)
                    setattr(warehouse_complex, 'res_aluminum', complex_res_aluminum)
                    setattr(warehouse_complex, 'res_variarit', complex_res_variarit)
                    setattr(warehouse_complex, 'res_inneilit', complex_res_inneilit)
                    setattr(warehouse_complex, 'res_renniit', complex_res_renniit)
                    setattr(warehouse_complex, 'res_cobalt', complex_res_cobalt)
                    setattr(warehouse_complex, 'mat_construction_material', complex_mat_construction_material)
                    setattr(warehouse_complex, 'mat_chemical', complex_mat_chemical)
                    setattr(warehouse_complex, 'mat_high_strength_allov', complex_mat_high_strength_allov)
                    setattr(warehouse_complex, 'mat_nanoelement', complex_mat_nanoelement)
                    setattr(warehouse_complex, 'mat_microprocessor_element', complex_mat_microprocessor_element)
                    setattr(warehouse_complex, 'mat_fober_optic_element', complex_mat_fober_optic_element)
                    warehouse_complex.save()

                production_id = production_id + 1

            setattr(warehouse, 'res_nickel', res_nickel)
            setattr(warehouse, 'res_iron', res_iron)
            setattr(warehouse, 'res_cooper', res_cooper)
            setattr(warehouse, 'res_aluminum', res_aluminum)
            setattr(warehouse, 'res_variarit', res_variarit)
            setattr(warehouse, 'res_inneilit', res_inneilit)
            setattr(warehouse, 'res_renniit', res_renniit)
            setattr(warehouse, 'res_cobalt', res_cobalt)
            setattr(warehouse, 'mat_construction_material', mat_construction_material)
            setattr(warehouse, 'mat_chemical', mat_chemical)
            setattr(warehouse, 'mat_high_strength_allov', mat_high_strength_allov)
            setattr(warehouse, 'mat_nanoelement', mat_nanoelement)
            setattr(warehouse, 'mat_microprocessor_element', mat_microprocessor_element)
            setattr(warehouse, 'mat_fober_optic_element', mat_fober_optic_element)
            warehouse.save()

            population = 0
            population_buildings = FactoryInstalled.objects.filter(user=user, user_city=user_city, production_class=10)
            for population_building in population_buildings:
                population = population + elapsed_time_seconds / population_building.factory_pattern.time_production

            new_population = user_city.population + population
            if new_population > user_city.max_population:
                new_population = user_city.max_population
            UserCity.objects.filter(id=user_city.id).update(population=new_population)

            check_all_user_factorys = FactoryInstalled.objects.filter(user=user, user_city=user_city)
            total_number_specialists = 0
            for check_all_user_factory in check_all_user_factorys:
                install_factory = check_all_user_factory
                if install_factory:
                    total_number_specialists = total_number_specialists + install_factory.factory_pattern.cost_expert_deployment
            increase_internal_currency = total_number_specialists * elapsed_time_seconds * user_variables.tax_per_person
            new_internal_currency = user.internal_currency + increase_internal_currency
            MyUser.objects.filter(id=user.id).update(internal_currency=new_internal_currency)

            trade_building = BuildingInstalled.objects.filter(user=user, user_city=user_city,
                                                              production_class=14).first()
            if trade_building:
                if trade_building.max_warehouse > trade_building.warehouse:
                    energy = elapsed_time_seconds / trade_building.time_production
                    stock_energy = trade_building.warehouse
                    new_energy = stock_energy + energy
                    if new_energy > trade_building.max_warehouse:
                        new_energy = trade_building.max_warehouse
                    BuildingInstalled.objects.filter(user=user, user_city=user_city, production_class=13).update(
                        warehouse=new_energy)

        last_time_update = time_update
        MyUser.objects.filter(user_id=user.id).update(last_time_check=last_time_update)
