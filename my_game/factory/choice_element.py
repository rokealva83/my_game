# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity, Warehouse, TurnProduction
from my_game.models import HullPattern, ShellPattern, ShieldPattern, GeneratorPattern, EnginePattern, \
    ArmorPattern, ModulePattern, WeaponPattern, FactoryInstalled, FuelPattern, DevicePattern
from my_game.models import WarehouseFactoryResource, BasicResource
from my_game.models import ManufacturingComplex
from my_game.factory import verification_stage_production
from my_game.building import assembly_line_workpieces


def choice_element(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        assembly_line_workpieces.check_assembly_line_workpieces(session_user)
        verification_stage_production.verification_stage_production(session_user)
        factory_id = request.POST.get('factory_id')
        factory_installed = FactoryInstalled.objects.filter(id=factory_id).first()
        factory_installeds = FactoryInstalled.objects.filter(user=session_user, user_city=session_user_city,
                                                              complex_status=0).order_by(
            'production_class', 'production_id')
        attributes = {}
        element_patterns = {}
        if factory_installed.production_class == 1:
            attributes = ("price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "health", "generator", "engine", "weapon", "armor", "shield", "main_weapon", "module",
                          "hold_size", "size", "mass", "power_consuption")
            element_patterns = HullPattern.objects.filter(user=session_user).order_by('basic_id', 'id')
        elif factory_installed.production_class == 2:
            attributes = ("price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "health", "value_energy_resistance", "value_phisical_resistance", "power", "regeneration",
                          "mass")
            element_patterns = ArmorPattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        elif factory_installed.production_class == 3:
            attributes = ("price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "health", "value_energy_resistance", "value_phisical_resistance", "number_of_emitter",
                          "regeneration",
                          "mass", "size", "power_consuption")
            element_patterns = ShieldPattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        elif factory_installed.production_class == 4:
            attributes = ("price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "health", "system_power", "intersystem_power", "giper_power", "nullT_power", "regeneration",
                          "mass", "size", "power_consuption")
            element_patterns = EnginePattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        elif factory_installed.production_class == 5:
            attributes = ("price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "health", "produced_energy", "fuel_necessary", "mass", "size")
            element_patterns = GeneratorPattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        elif factory_installed.production_class == 6:
            attributes = ("price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "health", "energy_damage", "regenerations", "number_of_bursts", "range", "accuracy", "mass",
                          "size", "power_consuption")
            element_patterns = WeaponPattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        elif factory_installed.production_class == 7:
            attributes = ("price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "phisical_damage", "speed", "mass", "size")
            element_patterns = ShellPattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        elif factory_installed.production_class == 8:
            attributes = ("price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "health", "param1", "param2", "param3", "mass", "size", "power_consuption")
            element_patterns = ModulePattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        elif factory_installed.production_class == 9:
            attributes = (
                "price_internal_currency", "price_resource1", "price_resource2", "price_resource3", "price_resource4",
                "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4", "health", "produced_energy",
                "fuel_necessary", "mass", "size", "power_consuption")
            element_patterns = DevicePattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        elif factory_installed.production_class == 14:
            attributes = ("price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "mass", "size", "efficiency")
            element_patterns = FuelPattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('id_resource')
        factory_warehouses = WarehouseFactoryResource.objects.filter(id_factory=factory_id)
        basic_resources = BasicResource.objects.filter()
        manufacturing_complexs = ManufacturingComplex.objects.filter(user=session_user, user_city=session_user_city)
        user_city = UserCity.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        turn_productions = TurnProduction.objects.filter(user=session_user, user_city=session_user_city)
        user_citys = UserCity.objects.filter(user=int(session_user))
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouses': warehouses, 'user_city': user_city,
                  'factory_installeds': factory_installeds, 'factory_installed': factory_installed,
                  'element_patterns': element_patterns, 'attributes': attributes, 'turn_productions': turn_productions,
                  'user_citys': user_citys, 'manufacturing_complexs': manufacturing_complexs,
                  'factory_warehouses': factory_warehouses, 'basic_resources': basic_resources}
        return render(request, "factory.html", output)