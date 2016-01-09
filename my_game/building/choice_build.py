# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity, TurnBuildingBuilding, TurnBuildingFactory
from my_game.models import FactoryPattern, BuildingPattern
from my_game.models import WarehouseFactory, WarehouseBuilding
from my_game.models import ManufacturingComplex
from my_game.models import TurnAssemblyPiecesBuilding, TurnAssemblyPiecesFactory
from my_game import function


def choice_build(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        function.check_all_queues(session_user)
        factory_patterns = {}
        building_patterns = {}
        attributes = (
            "price_internal_currency", 'price_construction_material', 'price_chemical', 'price_high_strength_allov',
            'price_nanoelement', 'price_microprocessor_element', 'price_fober_optic_element', "cost_expert_deployment",
            "assembly_workpiece", "time_deployment", "time_production", "factory_size", "factory_mass",
            "power_consumption")

        if request.POST.get('housing_unit') is not None:
            factory_patterns = FactoryPattern.objects.filter(user=session_user, production_class=10).order_by(
                'production_id')
        if request.POST.get('mine') is not None:
            factory_patterns = FactoryPattern.objects.filter(user=session_user, production_class=11).order_by(
                'production_id')
        if request.POST.get('material'):
            factory_patterns = FactoryPattern.objects.filter(user=session_user, production_class=13).order_by(
                'production_id')
        if request.POST.get('energy_unit') is not None:
            factory_patterns = FactoryPattern.objects.filter(user=session_user, production_class=12).order_by(
                'production_id')
        if request.POST.get('infrastructure') is not None:
            building_patterns = BuildingPattern.objects.filter(user=session_user).order_by('production_class',
                                                                                           'production_id')
            attributes = (
                "price_internal_currency", 'price_construction_material', 'price_chemical', 'price_high_strength_allov',
                'price_nanoelement', 'price_microprocessor_element', 'price_fober_optic_element',
                "cost_expert_deployment", "assembly_workpiece", "time_deployment", "time_production", "building_size",
                "building_mass", "power_consumption", "max_warehouse")
        if request.POST.get('hull') is not None:
            factory_patterns = FactoryPattern.objects.filter(user=session_user, production_class=1).order_by(
                'production_class','production_id')
        if request.POST.get('armor') is not None:
            factory_patterns = FactoryPattern.objects.filter(user=session_user, production_class=2).order_by(
                'production_class','production_id')
        if request.POST.get('shield') is not None:
            factory_patterns = FactoryPattern.objects.filter(user=session_user, production_class=3).order_by(
                'production_class','production_id')
        if request.POST.get('engine') is not None:
            factory_patterns = FactoryPattern.objects.filter(user=session_user, production_class=4).order_by(
                'production_class','production_id')
        if request.POST.get('generator') is not None:
            factory_patterns = FactoryPattern.objects.filter(user=session_user, production_class=5).order_by(
                'production_class','production_id')
        if request.POST.get('weapon') is not None:
            factory_patterns = FactoryPattern.objects.filter(user=session_user, production_class=6).order_by(
                'production_class','production_id')
        if request.POST.get('shell') is not None:
            factory_patterns = FactoryPattern.objects.filter(user=session_user, production_class=7, ).order_by(
                'production_class','production_id')
        if request.POST.get('module') is not None:
            factory_patterns = FactoryPattern.objects.filter(user=session_user, production_class=8).order_by(
                'production_class','production_id')
        if request.POST.get('device') is not None:
            factory_patterns = FactoryPattern.objects.filter(user=session_user, production_class=9).order_by(
                'production_class','production_id')
        if request.POST.get('fuel') is not None:
            factory_patterns = FactoryPattern.objects.filter(user=session_user, production_class=14).order_by(
                'production_class','production_id')

        if request.POST.get('infrastructure') is not None:
            warehouse_elements = [
                WarehouseBuilding.objects.filter(user=session_user, user_city=session_user_city,
                                                 building=building_pattern).first() for building_pattern in
                building_patterns]
        else:
            warehouse_elements = [WarehouseFactory.objects.filter(user=session_user, user_city=session_user_city,
                                                                  factory=factory_pattern).first() for factory_pattern
                                  in factory_patterns]

        factory_turn_assembly_piecess = TurnAssemblyPiecesFactory.objects.filter(user=session_user,
                                                                                 user_city=session_user_city).all()
        building_turn_assembly_piecess = TurnAssemblyPiecesBuilding.objects.filter(user=session_user,
                                                                                   user_city=session_user_city).all()
        turn_building_buildings = TurnBuildingBuilding.objects.filter(user=session_user,
                                                                      user_city=session_user_city).all()
        turn_building_factorys = TurnBuildingFactory.objects.filter(user=session_user,
                                                                    user_city=session_user_city).all()
        manufacturing_complexs = ManufacturingComplex.objects.filter(user=session_user, user_city=session_user_city)
        user_citys = UserCity.objects.filter(user=session_user)
        request.session['user'] = session_user.id
        request.session['user_city'] = session_user_city.id
        request.session['live'] = True
        output = {'user': session_user, 'warehouse': session_user_city.warehouse, 'user_city': session_user_city,
                  'factory_patterns': factory_patterns, 'attributes': attributes,
                  'factory_turn_assembly_piecess': factory_turn_assembly_piecess,
                  'building_turn_assembly_piecess': building_turn_assembly_piecess,
                  'building_patterns': building_patterns, 'turn_building_buildings': turn_building_buildings,
                  'turn_building_factorys': turn_building_factorys, 'warehouse_elements': warehouse_elements,
                  'user_citys': user_citys, 'manufacturing_complexs': manufacturing_complexs}

        return render(request, "building.html", output)
