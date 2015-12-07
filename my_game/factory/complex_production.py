# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity
from my_game.models import ManufacturingComplex, TurnComplexProduction
from my_game.models import HullPattern, ArmorPattern, ShieldPattern, EnginePattern, GeneratorPattern, \
    WeaponPattern, ShellPattern, ModulePattern, FuelPattern, DevicePattern
from my_game.models import FactoryInstalled
from my_game.factory import complex_production_module
from my_game.building import assembly_line_workpieces
from my_game import verification_func


def complex_production(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        assembly_line_workpieces.check_assembly_line_workpieces(session_user)
        message = ''
        factory = FactoryInstalled.objects.filter(id=request.GET.get('hidden_factory')).first()
        element_id = request.GET.get('hidden_element')
        complex = ManufacturingComplex.objects.filter(id=request.GET.get('complex_id')).first()
        verification_func.verification_of_resources(session_user)
        message = complex_production_module.complex_production_module(complex, factory, element_id, 0)
        factory_installeds = FactoryInstalled.objects.filter(user=session_user, user_city=session_user_city,
                                                             complex_status=0).order_by('production_class',
                                                                                        'production_id')
        complex_factorys = FactoryInstalled.objects.filter(complex_id=complex.id).order_by('production_class')
        hull_patterns = HullPattern.objects.filter(user=session_user).all()
        armor_patterns = ArmorPattern.objects.filter(user=session_user).all()
        shield_patterns = ShieldPattern.objects.filter(user=session_user).all()
        engine_patterns = EnginePattern.objects.filter(user=session_user).all()
        generator_patterns = GeneratorPattern.objects.filter(user=session_user).all()
        weapon_patterns = WeaponPattern.objects.filter(user=session_user).all()
        shell_patterns = ShellPattern.objects.filter(user=session_user).all()
        module_patterns = ModulePattern.objects.filter(user=session_user).all()
        device_patterns = DevicePattern.objects.filter(user=session_user).all()
        fuel_patterns = FuelPattern.objects.filter(user=session_user).all()

        turn_complex_productions = TurnComplexProduction.objects.filter(manufacturing_complex=complex)
        manufacturing_complexs = ManufacturingComplex.objects.filter(user=session_user, user_city=session_user_city)
        user_citys = UserCity.objects.filter(user=int(session_user))
        request.session['user'] = session_user.id
        request.session['user_city'] = session_user_city.id
        request.session['live'] = True
        output = {'user': session_user, 'warehouses': session_user_city.warehouse, 'user_city': session_user_city,
                  'turn_productions': turn_complex_productions, 'user_citys': user_citys,
                  'manufacturing_complexs': manufacturing_complexs, 'complex_id': complex.id,
                  'complex_factorys': complex_factorys, 'hull_patterns': hull_patterns,
                  'armor_patterns': armor_patterns, 'shield_patterns': shield_patterns,
                  'engine_patterns': engine_patterns, 'generator_patterns': generator_patterns,
                  'fuel_patterns': fuel_patterns, 'weapon_patterns': weapon_patterns, 'shell_patterns': shell_patterns,
                  'module_patterns': module_patterns, 'factory_installeds': factory_installeds,
                  'device_patterns': device_patterns}
        return render(request, "factory.html", output)
