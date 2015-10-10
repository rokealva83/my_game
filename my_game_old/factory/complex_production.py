# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity, Warehouse
from my_game.models import ManufacturingComplex, TurnComplexProduction
from my_game.models import HullPattern, ArmorPattern, ShieldPattern, EnginePattern, GeneratorPattern, \
    WeaponPattern, ShellPattern, ModulePattern, FuelPattern, DevicePattern
from my_game.models import FactoryInstalled
from my_game.factory import factory_function
from my_game.building import assembly_line_workpieces
from my_game import verification_func


def complex_production(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        assembly_line_workpieces.check_assembly_line_workpieces(session_user)
        message = ''
        factory_id = request.GET.get('hidden_factory')
        element_id = request.GET.get('hidden_element')
        complex_id = request.GET.get('complex_id')
        verification_func.verification_of_resources(session_user)
        message = factory_function.complex_production_module(complex_id, factory_id, element_id, 0)
        factory_installeds = FactoryInstalled.objects.filter(user=session_user, user_city=session_user_city,
                                                              complex_status=0).order_by('production_class',
                                                                                         'production_id')
        complex_factorys = FactoryInstalled.objects.filter(complex_id=complex_id).order_by('production_class')
        hull_patterns = HullPattern.objects.filter(user=session_user).order_by('basic_id', 'id')
        armor_patterns = ArmorPattern.objects.filter(user=session_user).order_by('basic_id', 'id')
        shield_patterns = ShieldPattern.objects.filter(user=session_user).order_by('basic_id', 'id')
        engine_patterns = EnginePattern.objects.filter(user=session_user).order_by('basic_id', 'id')
        generator_patterns = GeneratorPattern.objects.filter(user=session_user).order_by('basic_id', 'id')
        weapon_patterns = WeaponPattern.objects.filter(user=session_user).order_by('basic_id', 'id')
        shell_patterns = ShellPattern.objects.filter(user=session_user).order_by('basic_id', 'id')
        module_patterns = ModulePattern.objects.filter(user=session_user).order_by('basic_id', 'id')
        device_patterns = DevicePattern.objects.filter(user=session_user).order_by('basic_id', 'id')
        fuel_patterns = FuelPattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        turn_complex_productions = TurnComplexProduction.objects.filter(complex_id=complex_id)
        manufacturing_complexs = ManufacturingComplex.objects.filter(user=session_user, user_city=session_user_city)
        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('id_resource')
        user_city = UserCity.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = UserCity.objects.filter(user=int(session_user))
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouses': warehouses, 'user_city': user_city,
                  'turn_productions': turn_complex_productions,
                  'user_citys': user_citys, 'manufacturing_complexs': manufacturing_complexs, 'complex_id': complex_id,
                  'complex_factorys': complex_factorys, 'hull_patterns': hull_patterns,
                  'armor_patterns': armor_patterns, 'shield_patterns': shield_patterns,
                  'engine_patterns': engine_patterns, 'generator_patterns': generator_patterns,
                  'fuel_patterns': fuel_patterns, 'weapon_patterns': weapon_patterns, 'shell_patterns': shell_patterns,
                  'module_patterns': module_patterns, 'factory_installeds': factory_installeds,
                  'device_patterns': device_patterns}
        return render(request, "factory.html", output)