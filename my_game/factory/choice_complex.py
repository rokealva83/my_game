# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity, Warehouse, TurnComplexProduction
from my_game.models import HullPattern, ShellPattern, ShieldPattern, GeneratorPattern, EnginePattern, \
    ArmorPattern, ModulePattern, WeaponPattern, FactoryInstalled, FuelPattern, DevicePattern
from my_game.models import ManufacturingComplex
from my_game.factory import verification_stage_production, verification_complex_stage
from my_game.building import assembly_line_workpieces


def choice_complex(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        complex_id = request.POST.get('complex_id')
        assembly_line_workpieces.check_assembly_line_workpieces(session_user)
        verification_stage_production.verification_stage_production(session_user)
        verification_complex_stage.verification_complex_stage(session_user)

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

        warehouse= session_user_city.warehouse
        factory_installeds = FactoryInstalled.objects.filter(user=session_user, user_city=session_user_city,
                                                              complex_status=0).order_by('production_class',
                                                                                         'production_id')
        manufacturing_complexs = ManufacturingComplex.objects.filter(user=session_user, user_city=session_user_city)
        turn_complex_productions = TurnComplexProduction.objects.filter(complex_id=complex_id)
        user_city = UserCity.objects.filter(user=session_user).first()
        user_citys = UserCity.objects.filter(user=int(session_user))
        request.session['user'] = session_user.id
        request.session['user_city'] = session_user_city.id
        request.session['live'] = True
        output = {'user': session_user, 'warehouses': warehouses, 'user_city': user_city,
                  'turn_productions': turn_complex_productions, 'user_citys': user_citys,
                  'manufacturing_complexs': manufacturing_complexs, 'complex_id': complex_id,
                  'complex_factorys': complex_factorys, 'hull_patterns': hull_patterns,
                  'armor_patterns': armor_patterns, 'shield_patterns': shield_patterns,
                  'engine_patterns': engine_patterns, 'generator_patterns': generator_patterns,
                  'weapon_patterns': weapon_patterns, 'shell_patterns': shell_patterns,
                  'device_patterns': device_patterns, 'module_patterns': module_patterns,
                  'fuel_patterns': fuel_patterns, 'factory_installeds': factory_installeds}
        return render(request, "factory.html", output)