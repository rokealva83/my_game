# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity, TurnProduction
from my_game.models import HullPattern, ShellPattern, ShieldPattern, GeneratorPattern, EnginePattern, \
    ArmorPattern, ModulePattern, WeaponPattern, FactoryInstalled, FuelPattern, DevicePattern
from my_game.models import BasicResource
from my_game.models import ManufacturingComplex
from my_game import function


def produce_warehouse(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        function.check_all_queues(session_user)
        factory = FactoryInstalled.objects.filter(id=request.POST.get('factory_id')).first()
        warehouse_resource = int(request.POST.get('warehouse_resource'))
        resource_amount = int(request.POST.get('resource_amount'))
        warehouse = session_user_city.warehouse
        attribute = ['res_nickel', 'res_iron', 'res_cooper', 'res_aluminum', 'res_veriarit', 'res_inneilit',
                     'res_renniit', 'res_cobalt', 'mat_construction_material',
                     'mat_chemical', 'mat_high_strength_allov', 'mat_nanoelement', 'mat_microprocessor_element',
                     'mat_fober_optic_element']
        if warehouse_resource == 1:
            amount = warehouse.res_nickel
        elif warehouse_resource == 2:
            amount = warehouse.res_iron
        elif warehouse_resource == 3:
            amount = warehouse.res_cooper
        elif warehouse_resource == 4:
            amount = warehouse.res_aluminum
        elif warehouse_resource == 5:
            amount = warehouse.res_veriarit
        elif warehouse_resource == 6:
            amount = warehouse.res_inneilit
        elif warehouse_resource == 7:
            amount = warehouse.res_renniit
        elif warehouse_resource == 8:
            amount = warehouse.res_cobalt
        elif warehouse_resource == 9:
            amount = warehouse.mat_construction_material
        elif warehouse_resource == 10:
            amount = warehouse.mat_chemical
        elif warehouse_resource == 11:
            amount = warehouse.mat_high_strength_allov
        elif warehouse_resource == 12:
            amount = warehouse.mat_nanoelement
        elif warehouse_resource == 13:
            amount = warehouse.mat_microprocessor_element
        elif warehouse_resource == 14:
            amount = warehouse.mat_fober_optic_element

        if amount > resource_amount:
            factory_warehouse = factory.factory_warehouse
            new_amount = amount - resource_amount
            setattr(warehouse, attribute[warehouse_resource - 1], new_amount)
            warehouse.save()
            new_factory_warehouse_resource = getattr(factory_warehouse,
                                                     attribute[warehouse_resource - 1]) + resource_amount
            setattr(factory_warehouse, attribute[warehouse_resource - 1], new_factory_warehouse_resource)
            factory_warehouse.save()
            message = 'Ресурсы переданы комплексу'
        else:
            message = 'Нехватает ресурсов на основном складе'

        attributes = {}
        element_patterns = {}

        if factory.production_class == 1:
            attributes = ("price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "health", "generator", "engine", "weapon", "armor", "shield", "main_weapon", "module",
                          "hold_size", "size", "mass", "power_consuption")
            element_patterns = HullPattern.objects.filter(user=session_user).all()
        elif factory.production_class == 2:
            attributes = ("price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "health", "value_energy_resistance", "value_phisical_resistance", "power", "regeneration",
                          "mass")
            element_patterns = ArmorPattern.objects.filter(user=session_user).all()

        elif factory.production_class == 3:
            attributes = ("price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "health", "value_energy_resistance", "value_phisical_resistance", "number_of_emitter",
                          "regeneration",
                          "mass", "size", "power_consuption")
            element_patterns = ShieldPattern.objects.filter(user=session_user).all()

        elif factory.production_class == 4:
            attributes = ("price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "health", "system_power", "intersystem_power", "giper_power", "nullT_power", "regeneration",
                          "mass", "size", "power_consuption")
            element_patterns = EnginePattern.objects.filter(user=session_user).all()

        elif factory.production_class == 5:
            attributes = ("price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "health", "produced_energy", "fuel_necessary", "mass", "size")
            element_patterns = GeneratorPattern.objects.filter(user=session_user).all()

        elif factory.production_class == 6:
            attributes = ("price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "health", "energy_damage", "regenerations", "number_of_bursts", "range", "accuracy", "mass",
                          "size", "power_consuption")
            element_patterns = WeaponPattern.objects.filter(user=session_user).all()

        elif factory.production_class == 7:
            attributes = ("price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "phisical_damage", "speed", "mass", "size")
            element_patterns = ShellPattern.objects.filter(user=session_user).all()

        elif factory.production_class == 8:
            attributes = ("price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "health", "param1", "param2", "param3", "mass", "size", "power_consuption")
            element_patterns = ModulePattern.objects.filter(user=session_user).all()

        elif factory.production_class == 9:
            attributes = ("price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "health", "produced_energy", "fuel_necessary", "mass", "size", "power_consuption")
            element_patterns = DevicePattern.objects.filter(user=session_user).all()

        elif factory.production_class == 14:
            attributes = ("price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "mass", "size", "efficiency")
            element_patterns = FuelPattern.objects.filter(user=session_user).all()

        basic_resources = BasicResource.objects.filter()
        manufacturing_complexs = ManufacturingComplex.objects.filter(user=session_user, user_city=session_user_city)
        user_citys = UserCity.objects.filter(user=session_user)
        factory_installeds = FactoryInstalled.objects.filter(user=session_user, user_city=session_user_city,
                                                             complex_status=0).order_by(
            'production_class', 'production_id')
        factory_warehouse = factory.factory_warehouse
        turn_productions = TurnProduction.objects.filter(user=session_user, user_city=session_user_city)
        request.session['user'] = session_user.id
        request.session['user_city'] = session_user_city.id
        request.session['live'] = True
        output = {'user': session_user, 'warehouse': session_user_city.warehouse, 'user_city': session_user_city,
                  'factory_installeds': factory_installeds, 'factory_installed': factory,
                  'element_patterns': element_patterns, 'attributes': attributes, 'turn_productions': turn_productions,
                  'user_citys': user_citys, 'manufacturing_complexs': manufacturing_complexs,
                  'factory_warehouse': factory_warehouse, 'basic_resources': basic_resources, 'message': message}
        return render(request, "factory.html", output)
