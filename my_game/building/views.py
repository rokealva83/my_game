# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, User_city, Warehouse, Turn_building, Turn_assembly_pieces
from my_game.models import Factory_pattern
from my_game.models import Warehouse_factory
from my_game import function
from my_game import verification_func
from my_game.building import build_function


def building(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        turn_assembly_piecess = Turn_assembly_pieces.objects.filter(user=session_user, user_city=session_user_city)
        turn_buildings = Turn_building.objects.filter(user=session_user, user_city=session_user_city)
        warehouse = Warehouse.objects.filter(user=session_user).first()
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = User_city.objects.filter(user=int(session_user))
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouse': warehouse, 'user_city': user_city,
                  'turn_assembly_piecess': turn_assembly_piecess, 'turn_buildings': turn_buildings,
                  'user_citys': user_citys}
        return render(request, "building.html", output)


def choice_build(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        verification_func.check_assembly_line_workpieces(session_user)
        factory_patterns = {}
        attributes = ("name", "price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                      "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                      "cost_expert_deployment", "assembly_workpiece", "time_deployment", "production_class",
                      "production_id", "time_production", "size", "mass", "power_consumption")
        if request.POST.get('housing_unit') is not None:
            factory_patterns = Factory_pattern.objects.filter(user=session_user, production_class=10).order_by(
                'production_id')
        if request.POST.get('mine') is not None:
            factory_patterns = Factory_pattern.objects.filter(user=session_user, production_class=11).order_by(
                'production_id')
        if request.POST.get('energy_unit') is not None:
            factory_patterns = Factory_pattern.objects.filter(user=session_user, production_class=12).order_by(
                'production_id')
        if request.POST.get('hull') is not None:
            factory_patterns = Factory_pattern.objects.filter(user=session_user, production_class=1).order_by(
                'production_id')
        if request.POST.get('armor') is not None:
            factory_patterns = Factory_pattern.objects.filter(user=session_user, production_class=2).order_by(
                'production_id')
        if request.POST.get('shield') is not None:
            factory_patterns = Factory_pattern.objects.filter(user=session_user, production_class=3).order_by(
                'production_id')
        if request.POST.get('engine') is not None:
            factory_patterns = Factory_pattern.objects.filter(user=session_user, production_class=4).order_by(
                'production_id')
        if request.POST.get('generator') is not None:
            factory_patterns = Factory_pattern.objects.filter(user=session_user, production_class=5).order_by(
                'production_id')
        if request.POST.get('weapon') is not None:
            factory_patterns = Factory_pattern.objects.filter(user=session_user, production_class=6).order_by(
                'production_id')
        if request.POST.get('shell') is not None:
            factory_patterns = Factory_pattern.objects.filter(user=session_user, production_class=7).order_by(
                'production_id')
        if request.POST.get('module') is not None:
            factory_patterns = Factory_pattern.objects.filter(user=session_user, production_class=8).order_by(
                'production_id')
            # if request.POST.get('device') is not None:
        # factory_patterns = Factory_pattern.objects.filter(user=session_user, production_class=9).order_by('production_id')
        turn_assembly_piecess = Turn_assembly_pieces.objects.filter(user=session_user, user_city=session_user_city)
        turn_buildings = Turn_building.objects.filter(user=session_user, user_city=session_user_city)
        warehouse = Warehouse.objects.filter(user=session_user).first()
        warehouse_elements = Warehouse_factory.objects.filter(user=session_user, user_city=session_user_city)
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = User_city.objects.filter(user=int(session_user))
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouse': warehouse, 'user_city': user_city, 'factory_patterns': factory_patterns,
                  'attributes': attributes, 'turn_assembly_piecess': turn_assembly_piecess,
                  'turn_buildings': turn_buildings, 'warehouse_elements': warehouse_elements, 'user_citys': user_citys}

        return render(request, "building.html", output)


def working(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        verification_func.check_assembly_line_workpieces(session_user)
        message = ''

        if request.POST.get('rename_factory_pattern') is not None:
            new_name = request.POST.get('rename_factory_pattern')
            pattern_id = request.POST.get('hidden_factory')
            message = build_function.rename_factory_pattern(new_name, pattern_id)

        if request.POST.get('upgrade_factory_pattern') is not None:
            number = request.POST.get('number')
            speed = request.POST.get('speed')
            pattern_id = request.POST.get('hidden_factory')
            message = build_function.upgrade_factory_pattern(number, speed, pattern_id)

        if request.POST.get('delete_factory_pattern') is not None:
            pattern_id = request.POST.get('hidden_factory')
            message = build_function.delete_factory_pattern(pattern_id)

        if request.POST.get('making_factory_unit') is not None:
            amount_factory_unit = request.POST.get('amount_factory')
            pattern_id = request.POST.get('hidden_factory')
            message = build_function.making_factory_unit(session_user, session_user_city, amount_factory_unit, pattern_id)

        if request.POST.get('install_factory_unit') is not None:
            pattern_id = request.POST.get('hidden_factory')
            message = build_function.install_factory_unit(session_user, session_user_city, pattern_id)

        turn_assembly_piecess = Turn_assembly_pieces.objects.filter(user=session_user, user_city=session_user_city)
        turn_buildings = Turn_building.objects.filter(user=session_user, user_city=session_user_city)
        warehouse = Warehouse.objects.filter(user=session_user).first()
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouse': warehouse, 'user_city': user_city, 'message': message,
                  'turn_assembly_piecess': turn_assembly_piecess, 'turn_buildings': turn_buildings}
        return render(request, "building.html", output)