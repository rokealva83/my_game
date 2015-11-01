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
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        assembly_line_workpieces.check_assembly_line_workpieces(session_user)
        verification_stage_production.verification_stage_production(session_user)
        factory_id = request.POST.get('factory_id')
        factory_installed = FactoryInstalled.objects.filter(id=factory_id).first()
        factory_installeds = FactoryInstalled.objects.filter(user=session_user, user_city=session_user_city,
                                                             complex_status=0)
        attributes = {}
        element_patterns = {}
        if factory_installed.factory_pattern.production_class == 1:
            attributes = ("price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "hull_health", "generator", "engine", "weapon", "armor", "shield", "main_weapon", "module",
                          "hold_size", "hull_size", "hull_mass", "power_consuption")
            element_patterns = HullPattern.objects.filter(user=session_user).order_by('basic_hull', 'id')
        elif factory_installed.factory_pattern.production_class == 2:
            attributes = (
                "price_internal_currency", "price_resource1", "price_resource2", "price_resource3", "price_resource4",
                "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4", "armor_health",
                "value_energy_resistance", "value_phisical_resistance", "armor_power", "armor_regeneration",
                "armor_mass")
            element_patterns = ArmorPattern.objects.filter(user=session_user).order_by('basic_armor', 'id')
        elif factory_installed.factory_pattern.production_class == 3:
            attributes = ("price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "shield_health", "value_energy_resistance", "value_phisical_resistance", "number_of_emitter",
                          "shield_regeneration", "shield_mass", "shield_size", "power_consuption")
            element_patterns = ShieldPattern.objects.filter(user=session_user).order_by('basic_shield', 'id')
        elif factory_installed.factory_pattern.production_class == 4:
            attributes = (
                "price_internal_currency", "price_resource1", "price_resource2", "price_resource3", "price_resource4",
                "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4", "engine_health", "system_power",
                "intersystem_power", "giper_power", "nullT_power", "engine_mass", "engine_size", "power_consuption")
            element_patterns = EnginePattern.objects.filter(user=session_user).order_by('basic_engine', 'id')
        elif factory_installed.factory_pattern.production_class == 5:
            attributes = ("price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "generator_health", "produced_energy", "fuel_necessary", "generator_mass", "generator_size")
            element_patterns = GeneratorPattern.objects.filter(user=session_user).order_by('basic_generator', 'id')
        elif factory_installed.factory_pattern.production_class == 6:
            attributes = (
            "price_internal_currency", "price_resource1", "price_resource2", "price_resource3", "price_resource4",
            "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4", "weapon_health",
            "weapon_energy_damage", "weapon_regenerations", "number_of_bursts", "weapon_range", "weapon_accuracy",
            "weapon_mass", "weapon_size", "power_consuption")
            element_patterns = WeaponPattern.objects.filter(user=session_user).order_by('basic_weapon', 'id')

        elif factory_installed.factory_pattern.production_class == 7:
            attributes = ("price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "shell_phisical_damage", "shell_speed", "shell_mass", "shell_size")
            element_patterns = ShellPattern.objects.filter(user=session_user).order_by('basic_shell', 'id')

        elif factory_installed.factory_pattern.production_class == 8:
            attributes = ("price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "module_health", "param1", "param2", "param3", "module_mass", "module_size", "power_consuption")
            element_patterns = ModulePattern.objects.filter(user=session_user).order_by('basic_module', 'id')

        elif factory_installed.factory_pattern.production_class == 9:
            attributes = (
                "price_internal_currency", "price_resource1", "price_resource2", "price_resource3", "price_resource4",
                "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4", "device_health", "produced_energy",
                "fuel_necessary", "device_mass", "device_size", "power_consuption")
            element_patterns = DevicePattern.objects.filter(user=session_user).order_by('basic_device', 'id')

        elif factory_installed.factory_pattern.production_class == 14:
            attributes = ("price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "fuel_mass", "fuel_size", "fuel_efficiency")
            element_patterns = FuelPattern.objects.filter(user=session_user).order_by('basic_fuel', 'id')

        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('resource_id')
        factory_warehouses = WarehouseFactoryResource.objects.filter(factory=factory_installed)
        basic_resources = BasicResource.objects.filter()
        manufacturing_complexs = ManufacturingComplex.objects.filter(user=session_user, user_city=session_user_city)
        turn_productions = TurnProduction.objects.filter(user=session_user, user_city=session_user_city)
        user_citys = UserCity.objects.filter(user=session_user)
        request.session['userid'] = session_user.id
        request.session['user_city'] = session_user_city.id
        request.session['live'] = True
        output = {'user': session_user, 'warehouses': warehouses, 'user_city': session_user_city,
                  'factory_installeds': factory_installeds, 'factory_installed': factory_installed,
                  'element_patterns': element_patterns, 'attributes': attributes, 'turn_productions': turn_productions,
                  'user_citys': user_citys, 'manufacturing_complexs': manufacturing_complexs,
                  'factory_warehouses': factory_warehouses, 'basic_resources': basic_resources}
        return render(request, "factory.html", output)
