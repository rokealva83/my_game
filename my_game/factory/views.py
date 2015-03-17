# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, User_city, Warehouse, Turn_production
from my_game.models import Hull_pattern, Shell_pattern, Shield_pattern, Generator_pattern, Engine_pattern, \
    Armor_pattern, Module_pattern, Weapon_pattern, Factory_installed
from my_game.models import Warehouse_factory
from my_game import function
from my_game.factory import factory_function
from my_game import verification_func


def factory(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('id_resource')
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = User_city.objects.filter(user=int(session_user))
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouses': warehouses, 'user_city': user_city, 'user_citys': user_citys}
        return render(request, "factory.html", output)


def choice_element(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        verification_func.check_assembly_line_workpieces(session_user)
        verification_func.verification_stage_production(session_user)
        factory_installeds = {}
        element_patterns = {}
        attributes = {}
        if request.POST.get('hull') is not None:
            attributes = ("name", "price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "health", "generator", "engine", "weapon", "armor", "shield", "main_weapon", "module",
                          "hold_size", "size", "mass", "power_consuption")
            factory_installeds = Factory_installed.objects.filter(user=session_user, production_class=1).order_by(
                'production_id')
            element_patterns = Hull_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        if request.POST.get('armor') is not None:
            attributes = ("name", "price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "health", "value_energy_resistance", "value_phisical_resistance", "power", "regeneration",
                          "mass")
            factory_installeds = Factory_installed.objects.filter(user=session_user, production_class=2).order_by(
                'production_id')
            element_patterns = Armor_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        if request.POST.get('shield') is not None:
            attributes = ("name", "price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "health", "value_energy_resistance", "value_phisical_resistance", "number_of_emitter",
                          "regeneration",
                          "mass", "size", "power_consuption")
            factory_installeds = Factory_installed.objects.filter(user=session_user, production_class=3).order_by(
                'production_id')
            element_patterns = Shield_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        if request.POST.get('engine') is not None:
            attributes = ("name", "price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "health", "system_power", "intersystem_power", "giper_power", "nullT_power", "regeneration",
                          "mass", "size", "power_consuption")
            factory_installeds = Factory_installed.objects.filter(user=session_user, production_class=4).order_by(
                'production_id')
            element_patterns = Engine_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        if request.POST.get('generator') is not None:
            attributes = ("name", "price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "health", "produced_energy", "fuel_necessary", "mass", "size")
            factory_installeds = Factory_installed.objects.filter(user=session_user, production_class=5).order_by(
                'production_id')
            element_patterns = Generator_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        if request.POST.get('weapon') is not None:
            attributes = ("name", "price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "health", "energy_damage", "regenerations", "number_of_bursts", "range", "accuracy", "mass",
                          "size", "power_consuption")
            factory_installeds = Factory_installed.objects.filter(user=session_user, production_class=6).order_by(
                'production_id')
            element_patterns = Weapon_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        if request.POST.get('shell') is not None:
            attributes = ("name", "price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "phisical_damage", "speed", "mass", "size")
            factory_installeds = Factory_installed.objects.filter(user=session_user, production_class=7).order_by(
                'production_id')
            element_patterns = Shell_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        if request.POST.get('module') is not None:
            attributes = ("name", "price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "health", "param1", "param2", "param3", "mass", "size", "power_consuption")
            factory_installeds = Factory_installed.objects.filter(user=session_user, production_class=8).order_by(
                'production_id')
            element_patterns = Module_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')

            # if request.POST.get('device') is not None:
        # attributes = ("name", "price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
        # "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
        # "health", "produced_energy", "fuel_necessary",  "mass", "size", "power_consuption")
        # factory_installeds = Factory_installed.objects.filter(user=session_user, production_class=9).order_by(
        # 'production_id')
        # element_patterns = Device_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('id_resource')
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        turn_productions = Turn_production.objects.filter(user=session_user, user_city=session_user_city)
        user_citys = User_city.objects.filter(user=int(session_user))
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouses': warehouses, 'user_city': user_city,
                  'factory_installeds': factory_installeds, 'element_patterns': element_patterns,
                  'attributes': attributes, 'turn_productions': turn_productions, 'user_citys': user_citys}
        return render(request, "factory.html", output)


def production(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        verification_func.check_assembly_line_workpieces(session_user)
        message = ''
        if request.POST.get('rename_element_pattern'):
            new_name = request.POST.get('new_name')
            pattern_id = request.POST.get('hidden_factory')
            element_id = request.POST.get('hidden_element')
            message = factory_function.rename_element_pattern(session_user, session_user_city, pattern_id, element_id,
                                                              new_name)

        if request.POST.get('buttom_amount_element'):
            factory_id = request.POST.get('hidden_factory')
            element_id = request.POST.get('hidden_element')
            amount_element = request.POST.get('amount_element')
            message = factory_function.production_module(session_user, session_user_city, factory_id, element_id,
                                                         amount_element)

        if request.POST.get('disassembling'):
            factory_id = request.POST.get('hidden_factory')
            turn_production = Turn_production.objects.filter(factory_id=factory_id).first()
            user_city = User_city.objects.filter(id=session_user_city).first()
            if turn_production:
                message = 'На фабрике идет производство. Удаление невозможно'
            else:
                delete_factory = Factory_installed.objects.filter(id=factory_id).first()
                return_factory = Warehouse_factory.objects.filter(factory_id=delete_factory.factory_pattern_id).first()
                new_amount = return_factory.amount + 1
                return_factory = Warehouse_factory.objects.filter(factory_id=delete_factory.factory_pattern_id).update(
                    amount=new_amount)
                new_energy = user_city.use_energy - delete_factory.power_consumption
                user_city = User_city.objects.filter(id=session_user_city).update(use_energy=new_energy)
                delete_factory = Factory_installed.objects.filter(id=factory_id).delete()
                message = 'Фабрика удалена'

        turn_productions = Turn_production.objects.filter(user=session_user, user_city=session_user_city)
        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('id_resource')
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = User_city.objects.filter(user=int(session_user))
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouses': warehouses, 'user_city': user_city, 'message': message,
                  'turn_productions': turn_productions, 'user_citys': user_citys}
        return render(request, "factory.html", output)