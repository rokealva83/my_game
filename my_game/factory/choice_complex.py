# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, User_city, Warehouse, Turn_complex_production
from my_game.models import Hull_pattern, Shell_pattern, Shield_pattern, Generator_pattern, Engine_pattern, \
    Armor_pattern, Module_pattern, Weapon_pattern, Factory_installed, Fuel_pattern, Device_pattern
from my_game.models import Manufacturing_complex
from my_game.factory import verification_stage_production, verification_complex_stage
from my_game.building import assembly_line_workpieces


def choice_complex(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        complex_id = request.POST.get('complex_id')
        assembly_line_workpieces.check_assembly_line_workpieces(session_user)
        verification_stage_production.verification_stage_production(session_user)
        verification_complex_stage.verification_complex_stage(session_user)

        complex_factorys = Factory_installed.objects.filter(complex_id=complex_id).order_by('production_class')

        hull_patterns = Hull_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        armor_patterns = Armor_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        shield_patterns = Shield_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        engine_patterns = Engine_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        generator_patterns = Generator_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        weapon_patterns = Weapon_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        shell_patterns = Shell_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        module_patterns = Module_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        device_patterns = Device_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        fuel_patterns = Fuel_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('id_resource')
        factory_installeds = Factory_installed.objects.filter(user=session_user, user_city=session_user_city,
                                                              complex_status=0).order_by('production_class',
                                                                                         'production_id')
        manufacturing_complexs = Manufacturing_complex.objects.filter(user=session_user, user_city=session_user_city)
        turn_complex_productions = Turn_complex_production.objects.filter(complex_id=complex_id)
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = User_city.objects.filter(user=int(session_user))
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouses': warehouses, 'user_city': user_city,
                  'turn_productions': turn_complex_productions, 'user_citys': user_citys,
                  'manufacturing_complexs': manufacturing_complexs, 'complex_id': complex_id,
                  'complex_factorys': complex_factorys, 'hull_patterns': hull_patterns,
                  'armor_patterns': armor_patterns, 'shield_patterns': shield_patterns,
                  'engine_patterns': engine_patterns, 'generator_patterns': generator_patterns,
                  'weapon_patterns': weapon_patterns, 'shell_patterns': shell_patterns,
                  'device_patterns': device_patterns, 'module_patterns': module_patterns,
                  'fuel_patterns': fuel_patterns, 'factory_installeds': factory_installeds}
        return render(request, "factory.html", output)
