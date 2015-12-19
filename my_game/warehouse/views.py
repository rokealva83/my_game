# -*- coding: utf-8 -*-

from django.shortcuts import render

from my_game.models import MyUser, UserCity
from my_game.models import HullPattern, ShellPattern, ShieldPattern, GeneratorPattern, EnginePattern, \
    ArmorPattern, ModulePattern, FactoryPattern, WeaponPattern, FuelPattern, DevicePattern
from my_game.models import WarehouseFactory, WarehouseElement, BasicResource, BasicMaterial
from my_game import function


def warehouse(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        function.check_all_queues(session_user)
        basic_resources = BasicResource.objects.filter()
        basic_materials = BasicMaterial.objects.filter()
        user_citys = UserCity.objects.filter(user=session_user)
        warehouse_factorys = WarehouseFactory.objects.filter(user=session_user, user_city=session_user_city).order_by(
            'factory')
        factory_patterns = FactoryPattern.objects.filter(user=session_user)
        warehouse_elements = WarehouseElement.objects.filter(user=session_user, user_city=session_user_city).order_by(
            'element_class', 'element_id')
        hull_patterns = HullPattern.objects.filter(user=session_user)
        armor_patterns = ArmorPattern.objects.filter(user=session_user)
        shield_patterns = ShieldPattern.objects.filter(user=session_user)
        engine_patterns = EnginePattern.objects.filter(user=session_user)
        generator_patterns = GeneratorPattern.objects.filter(user=session_user)
        weapon_patterns = WeaponPattern.objects.filter(user=session_user)
        shell_patterns = ShellPattern.objects.filter(user=session_user)
        module_patterns = ModulePattern.objects.filter(user=session_user)
        device_patterns = DevicePattern.objects.filter(user=session_user)
        fuel_patterns = FuelPattern.objects.filter(user=session_user)

        attribute_factorys = (
            "cost_expert_deployment", "assembly_workpiece", "time_deployment", "production_class", "production_id",
            "time_production", "factory_size", "factory_mass", "power_consumption")

        attribute_hulls = (
            "hull_health", "generator", "engine", "weapon", "armor", "shield", "main_weapon", "module", "hold_size",
            "fuel_tank", "hull_size", "hull_mass", "power_consuption")

        attribute_armors = (
            "armor_health", "value_energy_resistance", "value_phisical_resistance", "armor_power", "armor_regeneration",
            "armor_mass")
        attribute_shields = (
            "shield_health", "value_energy_resistance", "value_phisical_resistance", "number_of_emitter",
            "shield_regeneration",
            "shield_mass", "shield_size", "power_consuption")
        attribute_engines = (
            "engine_health", "system_power", "intersystem_power", "giper_power", "nullT_power", "engine_regeneration",
            "engine_mass", "engine_size", "power_consuption")
        attribute_generators = ("health", "produced_energy", "fuel_necessary", "mass", "size")
        attribute_weapons = (
            "health", "energy_damage", "regenerations", "number_of_bursts", "range", "accuracy", "mass", "size",
            "power_consuption")
        attribute_shells = ("phisical_damage", "speed", "mass", "size")
        attribute_modules = ("health", "param1", "param2", "param3", "mass", "size", "power_consuption")
        attribute_devices = ("health", "param1", "param2", "param3", "mass", "size", "power_consuption")
        attribute_fuels = ("mass", "size", "efficiency")

    request.session['userid'] = session_user.id
    request.session['user_city'] = session_user_city.id
    request.session['live'] = True
    output = {'user': session_user, 'warehouse': session_user_city.warehouse, 'basic_resources': basic_resources,
              'basic_materials': basic_materials, 'user_city': session_user_city, 'user_citys': user_citys,
              'warehouse_factorys': warehouse_factorys, 'factory_patterns': factory_patterns,
              'warehouse_elements': warehouse_elements, 'hull_patterns': hull_patterns,
              'armor_patterns': armor_patterns, 'shield_patterns': shield_patterns, 'engine_patterns': engine_patterns,
              'generator_patterns': generator_patterns, 'weapon_patterns': weapon_patterns,
              'shell_patterns': shell_patterns, 'module_patterns': module_patterns, 'fuel_patterns': fuel_patterns,
              'device_patterns': device_patterns, 'attribute_factorys': attribute_factorys,
              'attribute_hulls': attribute_hulls, 'attribute_armors': attribute_armors,
              'attribute_shields': attribute_shields, 'attribute_engines': attribute_engines,
              'attribute_generators': attribute_generators, 'attribute_weapons': attribute_weapons,
              'attribute_shells': attribute_shells, 'attribute_modules': attribute_modules,
              'attribute_fuels': attribute_fuels, 'attribute_devices': attribute_devices}
    return render(request, "warehouse.html", output)
