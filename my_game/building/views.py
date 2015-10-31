# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity, Warehouse, TurnBuilding, TurnAssemblyPieces
from my_game.models import FactoryPattern, BuildingPattern, FactoryInstalled, BasicResource
from my_game.models import WarehouseFactory
from my_game.models import ManufacturingComplex, WarehouseComplex, TurnComplexProduction
from my_game import function, verification_func
from django.utils import timezone
from my_game.building import build_function, assembly_line_workpieces


def building(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        turn_assembly_piecess = TurnAssemblyPieces.objects.filter(user=session_user, user_city=session_user_city)
        turn_buildings = TurnBuilding.objects.filter(user=session_user, user_city=session_user_city)
        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city)
        manufacturing_complexs = ManufacturingComplex.objects.filter(user=session_user, user_city=session_user_city)
        user_city = UserCity.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = UserCity.objects.filter(user=int(session_user))
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouses': warehouses, 'user_city': user_city,
                  'turn_assembly_piecess': turn_assembly_piecess, 'turn_buildings': turn_buildings,
                  'user_citys': user_citys, 'manufacturing_complexs': manufacturing_complexs}
        return render(request, "building.html", output)


def choice_build(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        factory_patterns = {}
        building_patterns = {}
        warehouse_elements = {}
        attributes = ("price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                      "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                      "price_expert_deployment", "assembly_workpiece", "time_deployment", "time_production", "size",
                      "mass", "power_consumption")

        if request.POST.get('housing_unit') is not None:
            factory_patterns = FactoryPattern.objects.filter(user=session_user, production_class=10).order_by(
                'production_id')
            warehouse_elements = WarehouseFactory.objects.filter(user=session_user, user_city=session_user_city,
                                                                  production_class=10)
        if request.POST.get('mine') is not None:
            factory_patterns = FactoryPattern.objects.filter(user=session_user, production_class=11).order_by(
                'production_id')
            warehouse_elements = WarehouseFactory.objects.filter(user=session_user, user_city=session_user_city,
                                                                  production_class=11)
        if request.POST.get('energy_unit') is not None:
            factory_patterns = FactoryPattern.objects.filter(user=session_user, production_class=12).order_by(
                'production_id')
            warehouse_elements = WarehouseFactory.objects.filter(user=session_user, user_city=session_user_city,
                                                                  production_class=12)
        if request.POST.get('infrastructure') is not None:
            building_patterns = BuildingPattern.objects.filter(user=session_user).order_by('production_class',
                                                                                            'production_id')
            attributes = ("price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "price_expert_deployment", "assembly_workpiece", "time_deployment", "time_production", "size",
                          "mass", "power_consumption", "max_warehouse")
            warehouse_elements = WarehouseFactory.objects.filter(user=session_user, user_city=session_user_city,
                                                                  production_class=13)
        if request.POST.get('hull') is not None:
            factory_patterns = FactoryPattern.objects.filter(user=session_user, production_class=1).order_by(
                'production_id')
            warehouse_elements = WarehouseFactory.objects.filter(user=session_user, user_city=session_user_city,
                                                                  production_class=1)
        if request.POST.get('armor') is not None:
            factory_patterns = FactoryPattern.objects.filter(user=session_user, production_class=2).order_by(
                'production_id')
            warehouse_elements = WarehouseFactory.objects.filter(user=session_user, user_city=session_user_city,
                                                                  production_class=2)
        if request.POST.get('shield') is not None:
            factory_patterns = FactoryPattern.objects.filter(user=session_user, production_class=3).order_by(
                'production_id')
            warehouse_elements = WarehouseFactory.objects.filter(user=session_user, user_city=session_user_city,
                                                                  production_class=3)
        if request.POST.get('engine') is not None:
            factory_patterns = FactoryPattern.objects.filter(user=session_user, production_class=4).order_by(
                'production_id')
            warehouse_elements = WarehouseFactory.objects.filter(user=session_user, user_city=session_user_city,
                                                                  production_class=4)
        if request.POST.get('generator') is not None:
            factory_patterns = FactoryPattern.objects.filter(user=session_user, production_class=5).order_by(
                'production_id')
            warehouse_elements = WarehouseFactory.objects.filter(user=session_user, user_city=session_user_city,
                                                                  production_class=5)
        if request.POST.get('weapon') is not None:
            factory_patterns = FactoryPattern.objects.filter(user=session_user, production_class=6).order_by(
                'production_id')
            warehouse_elements = WarehouseFactory.objects.filter(user=session_user, user_city=session_user_city,
                                                                  production_class=6)
        if request.POST.get('shell') is not None:
            factory_patterns = FactoryPattern.objects.filter(user=session_user, production_class=7, ).order_by(
                'production_class', 'production_id')
            warehouse_elements = WarehouseFactory.objects.filter(user=session_user, user_city=session_user_city,
                                                                  production_class=7)
        if request.POST.get('module') is not None:
            factory_patterns = FactoryPattern.objects.filter(user=session_user, production_class=8).order_by(
                'production_id')
            warehouse_elements = WarehouseFactory.objects.filter(user=session_user, user_city=session_user_city,
                                                                  production_class=8)
        if request.POST.get('device') is not None:
            factory_patterns = FactoryPattern.objects.filter(user=session_user, production_class=9).order_by(
                'production_id')
            warehouse_elements = WarehouseFactory.objects.filter(user=session_user, user_city=session_user_city,
                                                                  production_class=9)

        if request.POST.get('fuel') is not None:
            user = session_user
            prod = 14

            factory_patterns = FactoryPattern.objects.filter(user=session_user, production_class=14).order_by(
                'production_id')
            warehouse_elements = WarehouseFactory.objects.filter(user=session_user, user_city=session_user_city,
                                                                  production_class=14)

        turn_assembly_piecess = TurnAssemblyPieces.objects.filter(user=session_user, user_city=session_user_city)
        turn_buildings = TurnBuilding.objects.filter(user=session_user, user_city=session_user_city)
        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city)
        manufacturing_complexs = ManufacturingComplex.objects.filter(user=session_user, user_city=session_user_city)
        user_city = UserCity.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = UserCity.objects.filter(user=int(session_user))
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouses': warehouses, 'user_city': user_city, 'factory_patterns': factory_patterns,
                  'attributes': attributes, 'turn_assembly_piecess': turn_assembly_piecess,
                  'building_patterns': building_patterns, 'turn_buildings': turn_buildings,
                  'warehouse_elements': warehouse_elements, 'user_citys': user_citys,
                  'manufacturing_complexs': manufacturing_complexs}

        return render(request, "building.html", output)


def working(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        assembly_line_workpieces.check_assembly_line_workpieces(session_user)
        message = ''

        if request.POST.get('rename_factory_pattern') is not None:
            new_name = request.POST.get('rename_factory_pattern')
            pattern_id = request.POST.get('hidden_factory')
            class_id = request.POST.get('hidden_class')
            message = build_function.rename_factory_pattern(new_name, pattern_id, class_id)

        if request.POST.get('upgrade_factory_pattern') is not None:
            number = request.POST.get('number')
            speed = request.POST.get('speed')
            pattern_id = request.POST.get('hidden_factory')
            class_id = request.POST.get('hidden_class')
            message = build_function.upgrade_factory_pattern(number, speed, pattern_id, class_id)

        if request.POST.get('delete_factory_pattern') is not None:
            pattern_id = request.POST.get('hidden_factory')
            class_id = request.POST.get('hidden_class')
            message = build_function.delete_factory_pattern(pattern_id, class_id)

        if request.POST.get('making_factory_unit') is not None:
            amount_factory_unit = request.POST.get('amount_factory')
            pattern_id = request.POST.get('hidden_factory')
            class_id = request.POST.get('hidden_class')
            message = build_function.making_factory_unit(session_user, session_user_city, amount_factory_unit,
                                                         pattern_id, class_id)

        if request.POST.get('install_factory_unit') is not None:
            pattern_id = request.POST.get('hidden_factory')
            class_id = request.POST.get('hidden_class')
            message = build_function.install_factory_unit(session_user, session_user_city, pattern_id, class_id)

        turn_assembly_piecess = TurnAssemblyPieces.objects.filter(user=session_user, user_city=session_user_city)
        turn_buildings = TurnBuilding.objects.filter(user=session_user, user_city=session_user_city)
        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('resource_id')
        manufacturing_complexs = ManufacturingComplex.objects.filter(user=session_user, user_city=session_user_city)
        user_city = UserCity.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = UserCity.objects.filter(user=int(session_user))
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouses': warehouses, 'user_city': user_city, 'message': message,
                  'turn_assembly_piecess': turn_assembly_piecess, 'turn_buildings': turn_buildings,
                  'user_citys': user_citys, 'manufacturing_complexs': manufacturing_complexs}
        return render(request, "building.html", output)


def create_complex(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        name = request.POST.get('complex_name')
        turn_assembly_piecess = TurnAssemblyPieces.objects.filter(user=session_user, user_city=session_user_city)
        turn_buildings = TurnBuilding.objects.filter(user=session_user, user_city=session_user_city)
        manufacturing_complex = ManufacturingComplex(
            user=session_user,
            user_city=session_user_city,
            name=name,
        )
        manufacturing_complex.save()
        complex_id = manufacturing_complex.id
        message = 'Комплекс создано'

        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city)
        manufacturing_complexs = ManufacturingComplex.objects.filter(user=session_user, user_city=session_user_city)
        manufacturing_complex = ManufacturingComplex.objects.filter(id=complex_id).first()
        factory_installeds = FactoryInstalled.objects.filter(user=session_user, complex_status=0).order_by(
            'production_class', 'production_id')
        complex_factorys = FactoryInstalled.objects.filter(user=session_user, complex_status=1,
                                                            complex_id=complex_id).order_by('production_id')
        warehouse_complexs = WarehouseComplex.objects.filter(id_complex=complex_id).order_by('resource_id')
        basic_resources = BasicResource.objects.filter()
        user_city = UserCity.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = UserCity.objects.filter(user=int(session_user))
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouses': warehouses, 'user_city': user_city,
                  'turn_assembly_piecess': turn_assembly_piecess, 'turn_buildings': turn_buildings,
                  'user_citys': user_citys, 'message': message, 'complex_id': complex_id,
                  'manufacturing_complexs': manufacturing_complexs, 'manufacturing_complex': manufacturing_complex,
                  'factory_installeds': factory_installeds, 'complex_factorys': complex_factorys,
                  'basic_resources': basic_resources, 'warehouse_complexs': warehouse_complexs}
        return render(request, "building.html", output)


def management_complex(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        complex_id = request.POST.get('complex_id')
        message = ''
        turn_assembly_piecess = TurnAssemblyPieces.objects.filter(user=session_user, user_city=session_user_city)
        turn_buildings = TurnBuilding.objects.filter(user=session_user, user_city=session_user_city)
        factory_installeds = FactoryInstalled.objects.filter(user=session_user, complex_status=0).order_by(
            'production_class', 'production_id')
        complex_factorys = FactoryInstalled.objects.filter(user=session_user, complex_status=1,
                                                            complex_id=complex_id).order_by('production_id')
        warehouse_complexs = WarehouseComplex.objects.filter(id_complex=complex_id).order_by('resource_id')
        basic_resources = BasicResource.objects.filter()
        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city)
        manufacturing_complexs = ManufacturingComplex.objects.filter(user=session_user, user_city=session_user_city)
        manufacturing_complex = ManufacturingComplex.objects.filter(id=complex_id).first()
        user_city = UserCity.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = UserCity.objects.filter(user=int(session_user))
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouses': warehouses, 'user_city': user_city,
                  'turn_assembly_piecess': turn_assembly_piecess, 'turn_buildings': turn_buildings,
                  'user_citys': user_citys, 'message': message, 'complex_id': complex_id,
                  'manufacturing_complexs': manufacturing_complexs, 'manufacturing_complex': manufacturing_complex,
                  'factory_installeds': factory_installeds, 'complex_factorys': complex_factorys,
                  'basic_resources': basic_resources, 'warehouse_complexs': warehouse_complexs}
        return render(request, "building.html", output)


def add_in_complex(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        complex_id = request.POST.get('complex_id')
        installed_factory_id = request.POST.get('factory_id')
        complex_factory = FactoryInstalled.objects.filter(id=installed_factory_id).first()
        manufacturing_complex = ManufacturingComplex.objects.filter(id=complex_id).first()
        if complex_factory.user_city == manufacturing_complex.user_city:
            complex_factory = FactoryInstalled.objects.filter(id=installed_factory_id).update(complex_status=1,
                                                                                               complex_id=complex_id)
            message = 'Производство добавлено в комплекс'
        else:
            message = 'Производство в комплекс не добавлено. Местоположение неверное'

        turn_assembly_piecess = TurnAssemblyPieces.objects.filter(user=session_user, user_city=session_user_city)
        turn_buildings = TurnBuilding.objects.filter(user=session_user, user_city=session_user_city)
        factory_installeds = FactoryInstalled.objects.filter(user=session_user, complex_status=0).order_by(
            'production_class', 'production_id')
        complex_factorys = FactoryInstalled.objects.filter(user=session_user, complex_status=1,
                                                            complex_id=complex_id).order_by('production_class',
                                                                                            'production_id')
        warehouse_complexs = WarehouseComplex.objects.filter(id_complex=complex_id).order_by('resource_id')
        basic_resources = BasicResource.objects.filter()
        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city)
        manufacturing_complexs = ManufacturingComplex.objects.filter(user=session_user, user_city=session_user_city)
        manufacturing_complex = ManufacturingComplex.objects.filter(id=complex_id).first()
        user_city = UserCity.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = UserCity.objects.filter(user=int(session_user))
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouses': warehouses, 'user_city': user_city,
                  'turn_assembly_piecess': turn_assembly_piecess, 'turn_buildings': turn_buildings,
                  'user_citys': user_citys, 'message': message, 'complex_id': complex_id,
                  'manufacturing_complexs': manufacturing_complexs, 'manufacturing_complex': manufacturing_complex,
                  'factory_installeds': factory_installeds, 'complex_factorys': complex_factorys,
                  'basic_resources': basic_resources, 'warehouse_complexs': warehouse_complexs}
        return render(request, "building.html", output)


def remove_from_complex(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        complex_id = request.POST.get('complex_id')
        installed_factory_id = request.POST.get('factory_id')
        turn_production = TurnComplexProduction.objects.filter(complex_id=complex_id,
                                                                 factory_id=installed_factory_id).first()
        if turn_production:
            message = 'Исключение невозможно. Идет производство'
        else:
            complex_factory = FactoryInstalled.objects.filter(id=installed_factory_id).update(complex_status=0,
                                                                                               complex_id=0)
            message = 'Производство добавлено в комплекс'
        turn_assembly_piecess = TurnAssemblyPieces.objects.filter(user=session_user, user_city=session_user_city)
        turn_buildings = TurnBuilding.objects.filter(user=session_user, user_city=session_user_city)
        factory_installeds = FactoryInstalled.objects.filter(user=session_user, complex_status=0).order_by(
            'production_class', 'production_id')
        complex_factorys = FactoryInstalled.objects.filter(user=session_user, complex_status=1,
                                                            complex_id=complex_id).order_by('production_class',
                                                                                            'production_id')
        warehouse_complexs = WarehouseComplex.objects.filter(id_complex=complex_id).order_by('resource_id')
        basic_resources = BasicResource.objects.filter()
        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city)
        manufacturing_complexs = ManufacturingComplex.objects.filter(user=session_user, user_city=session_user_city)
        manufacturing_complex = ManufacturingComplex.objects.filter(id=complex_id).first()
        user_city = UserCity.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = UserCity.objects.filter(user=int(session_user))
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouses': warehouses, 'user_city': user_city,
                  'turn_assembly_piecess': turn_assembly_piecess, 'turn_buildings': turn_buildings,
                  'user_citys': user_citys, 'message': message, 'complex_id': complex_id,
                  'manufacturing_complexs': manufacturing_complexs, 'manufacturing_complex': manufacturing_complex,
                  'factory_installeds': factory_installeds, 'complex_factorys': complex_factorys,
                  'basic_resources': basic_resources, 'warehouse_complexs': warehouse_complexs}
        return render(request, "building.html", output)


def percent_extraction(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        time_update = MyUser.objects.filter(user_id=session_user).first().last_time_check
        now_date = timezone.now()
        elapsed_time_full = now_date - time_update
        elapsed_time_seconds = elapsed_time_full.seconds
        time_update = now_date
        verification_func.verification_of_resources(session_user)
        complex_id = request.POST.get('complex_id')
        new_percent = request.POST.get('percent_extraction')
        manufacturing_complex = ManufacturingComplex.objects.filter(id=complex_id).update(
            extraction_parametr=new_percent)
        message = ''
        turn_assembly_piecess = TurnAssemblyPieces.objects.filter(user=session_user, user_city=session_user_city)
        turn_buildings = TurnBuilding.objects.filter(user=session_user, user_city=session_user_city)
        factory_installeds = FactoryInstalled.objects.filter(user=session_user, complex_status=0).order_by(
            'production_class', 'production_id')
        complex_factorys = FactoryInstalled.objects.filter(user=session_user, complex_status=1,
                                                            complex_id=complex_id).order_by('production_class',
                                                                                            'production_id')
        warehouse_complexs = WarehouseComplex.objects.filter(id_complex=complex_id).order_by('resource_id')
        basic_resources = BasicResource.objects.filter()
        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city)
        manufacturing_complexs = ManufacturingComplex.objects.filter(user=session_user, user_city=session_user_city)
        manufacturing_complex = ManufacturingComplex.objects.filter(id=complex_id).first()
        user_city = UserCity.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = UserCity.objects.filter(user=int(session_user))
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouses': warehouses, 'user_city': user_city,
                  'turn_assembly_piecess': turn_assembly_piecess, 'turn_buildings': turn_buildings,
                  'user_citys': user_citys, 'message': message, 'complex_id': complex_id,
                  'manufacturing_complexs': manufacturing_complexs, 'manufacturing_complex': manufacturing_complex,
                  'factory_installeds': factory_installeds, 'complex_factorys': complex_factorys,
                  'basic_resources': basic_resources, 'warehouse_complexs': warehouse_complexs}
        return render(request, "building.html", output)


def complex_warehouse(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        complex_id = request.POST.get('complex_id')
        warehouse_resource = request.POST.get('warehouse_resource')
        resource_amount = request.POST.get('resource_amount')
        warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city,
                                             id_resource=warehouse_resource).first()
        if warehouse is not None and int(warehouse.amount) >= int(resource_amount):
            new_amount = int(warehouse.amount) - int(resource_amount)
            warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city,
                                                 id_resource=warehouse_resource).update(amount=new_amount)
            warehouse_complex = WarehouseComplex.objects.filter(id_complex=complex_id,
                                                                 id_resource=warehouse_resource).first()
            if warehouse_complex:
                new_amount = int(warehouse_complex.amount) + int(resource_amount)
                warehouse_complex = WarehouseComplex.objects.filter(id_complex=complex_id,
                                                                     id_resource=warehouse_resource).update(
                    amount=new_amount)
            else:
                warehouse_complex = WarehouseComplex(
                    id_complex=complex_id,
                    id_resource=warehouse_resource,
                    amount=int(resource_amount)
                )
                warehouse_complex.save()
            message = 'Ресурсы переданы комплексу'
        else:
            message = 'Нехватает ресурсов на основном складе'
        turn_assembly_piecess = TurnAssemblyPieces.objects.filter(user=session_user, user_city=session_user_city)
        turn_buildings = TurnBuilding.objects.filter(user=session_user, user_city=session_user_city)
        factory_installeds = FactoryInstalled.objects.filter(user=session_user, complex_status=0).order_by(
            'production_class', 'production_id')
        complex_factorys = FactoryInstalled.objects.filter(user=session_user, complex_status=1,
                                                            complex_id=complex_id).order_by('production_class',
                                                                                            'production_id')
        warehouse_complexs = WarehouseComplex.objects.filter(id_complex=complex_id).order_by('resource_id')
        basic_resources = BasicResource.objects.filter()
        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city)
        manufacturing_complexs = ManufacturingComplex.objects.filter(user=session_user, user_city=session_user_city)
        manufacturing_complex = ManufacturingComplex.objects.filter(id=complex_id).first()
        user_city = UserCity.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = UserCity.objects.filter(user=int(session_user))
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouses': warehouses, 'user_city': user_city,
                  'turn_assembly_piecess': turn_assembly_piecess, 'turn_buildings': turn_buildings,
                  'user_citys': user_citys, 'message': message, 'complex_id': complex_id,
                  'manufacturing_complexs': manufacturing_complexs, 'manufacturing_complex': manufacturing_complex,
                  'factory_installeds': factory_installeds, 'complex_factorys': complex_factorys,
                  'basic_resources': basic_resources, 'warehouse_complexs': warehouse_complexs}
        return render(request, "building.html", output)