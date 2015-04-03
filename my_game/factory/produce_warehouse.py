# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, User_city, Warehouse, Turn_production
from my_game.models import Hull_pattern, Shell_pattern, Shield_pattern, Generator_pattern, Engine_pattern, \
    Armor_pattern, Module_pattern, Weapon_pattern, Factory_installed
from my_game.models import Warehouse_factory_resource, Basic_resource
from my_game.models import Manufacturing_complex
from my_game import function



def produce_warehouse(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        factory_id = request.POST.get('factory_id')
        warehouse_resource = request.POST.get('warehouse_resource')
        resource_amount = request.POST.get('resource_amount')
        warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city,
                                             id_resource=warehouse_resource).first()
        if warehouse is not None and int(warehouse.amount) >= int(resource_amount):
            new_amount = int(warehouse.amount) - int(resource_amount)
            warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city,
                                                 id_resource=warehouse_resource).update(amount=new_amount)
            warehouse_factory = Warehouse_factory_resource.objects.filter(id_factory=factory_id,
                                                                          id_resource=warehouse_resource).first()
            if warehouse_factory:
                new_amount = int(warehouse_factory.amount) + int(resource_amount)
                warehouse_factory = Warehouse_factory_resource.objects.filter(id_factory=factory_id,
                                                                              id_resource=warehouse_resource).update(
                    amount=new_amount)
            else:
                warehouse_factory = Warehouse_factory_resource(
                    id_factory=factory_id,
                    id_resource=warehouse_resource,
                    amount=int(resource_amount)
                )
                warehouse_factory.save()
            message = 'Ресурсы переданы комплексу'
        else:
            message = 'Нехватает ресурсов на основном складе'
        factory_installed = Factory_installed.objects.filter(id=factory_id).first()

        if factory_installed.production_class == 1:
            attributes = ("price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "health", "generator", "engine", "weapon", "armor", "shield", "main_weapon", "module",
                          "hold_size", "size", "mass", "power_consuption")
            element_patterns = Hull_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')
        elif factory_installed.production_class == 2:
            attributes = ("price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "health", "value_energy_resistance", "value_phisical_resistance", "power", "regeneration",
                          "mass")
            element_patterns = Armor_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        elif factory_installed.production_class == 3:
            attributes = ("price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "health", "value_energy_resistance", "value_phisical_resistance", "number_of_emitter",
                          "regeneration",
                          "mass", "size", "power_consuption")
            element_patterns = Shield_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        elif factory_installed.production_class == 4:
            attributes = ("price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "health", "system_power", "intersystem_power", "giper_power", "nullT_power", "regeneration",
                          "mass", "size", "power_consuption")
            element_patterns = Engine_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        elif factory_installed.production_class == 5:
            attributes = ("price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "health", "produced_energy", "fuel_necessary", "mass", "size")
            element_patterns = Generator_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        elif factory_installed.production_class == 6:
            attributes = ("price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "health", "energy_damage", "regenerations", "number_of_bursts", "range", "accuracy", "mass",
                          "size", "power_consuption")
            element_patterns = Weapon_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        elif factory_installed.production_class == 7:
            attributes = ("price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "phisical_damage", "speed", "mass", "size")
            element_patterns = Shell_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        elif factory_installed.production_class == 8:
            attributes = ("price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "health", "param1", "param2", "param3", "mass", "size", "power_consuption")
            element_patterns = Module_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')

            # elif factory_installed.production_class == 9:
        # attributes = ("price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
        # "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
        # "health", "produced_energy", "fuel_necessary",  "mass", "size", "power_consuption")
        # element_patterns = Device_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        basic_resources = Basic_resource.objects.filter()
        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city)
        manufacturing_complexs = Manufacturing_complex.objects.filter(user=session_user, user_city=session_user_city)
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = User_city.objects.filter(user=int(session_user))
        factory_installed = Factory_installed.objects.filter(id=factory_id).first()
        factory_installeds = Factory_installed.objects.filter(user=session_user, user_city=session_user_city,
                                                              complex_status=0).order_by(
            'production_class', 'production_id')
        factory_warehouses = Warehouse_factory_resource.objects.filter(id_factory=factory_id)
        turn_productions = Turn_production.objects.filter(user=session_user, user_city=session_user_city)
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouses': warehouses, 'user_city': user_city,
                  'factory_installeds': factory_installeds, 'factory_installed': factory_installed,
                  'element_patterns': element_patterns, 'attributes': attributes, 'turn_productions': turn_productions,
                  'user_citys': user_citys, 'manufacturing_complexs': manufacturing_complexs,
                  'factory_warehouses': factory_warehouses, 'basic_resources': basic_resources}
        return render(request, "factory.html", output)