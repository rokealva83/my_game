# -*- coding: utf-8 -*-

from django.shortcuts import render

from my_game.models import MyUser, User_city, Warehouse
from my_game.models import Hull_pattern, Shell_pattern, Shield_pattern, Generator_pattern, Engine_pattern, \
    Armor_pattern, Module_pattern, Factory_pattern, Weapon_pattern, Fuel_pattern
from my_game.models import Warehouse_factory, Warehouse_element, Basic_resource
from my_game import function


def warehouse(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('id_resource')
        basic_resources = Basic_resource.objects.filter()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_city = User_city.objects.filter(user=session_user).first()
        user_citys = User_city.objects.filter(user=int(session_user))
        warehouse_factorys = Warehouse_factory.objects.filter(user=session_user, user_city=session_user_city).order_by(
            'production_class', 'production_id')
        factory_patterns = Factory_pattern.objects.filter(user=session_user)
        warehouse_elements = Warehouse_element.objects.filter(user=session_user, user_city=session_user_city).order_by(
            'element_class', 'element_id')
        hull_patterns = Hull_pattern.objects.filter(user=session_user)
        armor_patterns = Armor_pattern.objects.filter(user=session_user)
        shield_patterns = Shield_pattern.objects.filter(user=session_user)
        engine_patterns = Engine_pattern.objects.filter(user=session_user)
        generator_patterns = Generator_pattern.objects.filter(user=session_user)
        weapon_patterns = Weapon_pattern.objects.filter(user=session_user)
        shell_patterns = Shell_pattern.objects.filter(user=session_user)
        module_patterns = Module_pattern.objects.filter(user=session_user)
        # device_patterns = Device_pattern.objects.filter(user = session_user)
        fuel_patterns = Fuel_pattern.objects.filter(user=session_user)

        attribute_factorys = ("cost_expert_deployment", "assembly_workpiece", "time_deployment", "production_class", \
                              "production_id", "time_production", "size", "mass", "power_consumption")
        attribute_hulls = ("health", "generator", "engine", "weapon", "armor", "shield", "main_weapon", "module", \
                           "hold_size","fuel_tank", "size", "mass", "power_consuption")
        attribute_armors = ("health", "value_energy_resistance", "value_phisical_resistance", "power", "regeneration", \
                            "mass")
        attribute_shields = ("health", "value_energy_resistance", "value_phisical_resistance", "number_of_emitter", \
                             "regeneration", "mass", "size", "power_consuption")
        attribute_engines = ("health", "system_power", "intersystem_power", "giper_power", "nullT_power", \
                             "regeneration", "mass", "size", "power_consuption")
        attribute_generators = ("health", "produced_energy", "fuel_necessary", "mass", "size")
        attribute_weapons = ("health", "energy_damage", "regenerations", "number_of_bursts", "range", "accuracy", \
                             "mass", "size", "power_consuption")
        attribute_shells = ("phisical_damage", "speed", "mass", "size")
        attribute_modules = ("health", "param1", "param2", "param3", "mass", "size", "power_consuption")
        attribute_fuels = ("mass", "size", "efficiency")

    request.session['userid'] = session_user
    request.session['user_city'] = session_user_city
    request.session['live'] = True
    output = {'user': user, 'warehouses': warehouses, 'basic_resources': basic_resources, 'user_city': user_city,
              'user_citys': user_citys, 'warehouse_factorys': warehouse_factorys, 'factory_patterns': factory_patterns,
              'warehouse_elements': warehouse_elements, 'hull_patterns': hull_patterns,
              'armor_patterns': armor_patterns, 'shield_patterns': shield_patterns, 'engine_patterns': engine_patterns,
              'generator_patterns': generator_patterns, 'weapon_patterns': weapon_patterns,
              'shell_patterns': shell_patterns, 'module_patterns': module_patterns, 'fuel_patterns':fuel_patterns,
              'attribute_factorys': attribute_factorys, 'attribute_hulls': attribute_hulls,
              'attribute_armors': attribute_armors, 'attribute_shields': attribute_shields,
              'attribute_engines': attribute_engines, 'attribute_generators': attribute_generators,
              'attribute_weapons': attribute_weapons, 'attribute_shells': attribute_shells,
              'attribute_modules': attribute_modules, 'attribute_fuels0':attribute_fuels}
    return render(request, "warehouse.html", output)
