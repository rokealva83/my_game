# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from django.shortcuts import render
from my_game.models import MyUser, User_city, Warehouse, Basic_resource
from my_game.models import Hull_pattern, Shield_pattern, Generator_pattern, Engine_pattern, \
    Armor_pattern, Module_pattern, Weapon_pattern, Shell_pattern, Factory_pattern, Device_pattern
from my_game.models import Basic_armor, Basic_factory, Basic_engine, Basic_generator, Basic_hull, Basic_module, \
    Basic_shell, Basic_shield, Basic_weapon, Basic_scientic
from my_game.models import Warehouse_element, Warehouse_factory
from my_game import function
from my_game.models import Project_ship, Element_ship, Turn_ship_build, Ship
from my_game.models import Trade_element, Trade_space, Building_installed, Delivery_queue


def buy_credit(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        message = ''
        trade_space_id = request.POST.get('trade_space_id')
        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('id_resource')
        basic_resources = Basic_resource.objects.filter()
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        foreigh_currency = user.foreigh_currency
        internal_currency = user.internal_currency
        amount_foreigh = int(request.POST.get('amount'))
        operation = int(request.POST.get('operation'))
        if operation == 0:
            need_internal_currency = amount_foreigh * 500
            if internal_currency >= need_internal_currency:
                new_internal_currency = internal_currency - need_internal_currency
                new_foreigh_currency = foreigh_currency + amount_foreigh
                user = MyUser.objects.filter(user_id=session_user).update(internal_currency = new_internal_currency, foreigh_currency = new_foreigh_currency)
                message = 'Покупка совершена'
            else:
                message = 'Нехватка внутренней валюты'
        else:
            if foreigh_currency >= amount_foreigh:
                bought_currency = amount_foreigh * 495
                new_internal_currency = internal_currency + bought_currency
                new_foreigh_currency = foreigh_currency - amount_foreigh
                user = MyUser.objects.filter(user_id=session_user).update(internal_currency = new_internal_currency, foreigh_currency = new_foreigh_currency)
                message = 'Продажа совершена'
        user_citys = User_city.objects.filter(user=int(session_user))
        user = MyUser.objects.filter(user_id=session_user).first()
        warehouse_elements = Warehouse_element.objects.filter(user=session_user, user_city=session_user_city).order_by(
            'element_class', 'element_id')
        warehouse_factorys = Warehouse_factory.objects.filter(user=session_user, user_city=session_user_city).order_by(
            'production_class', 'production_id')
        factory_patterns = Factory_pattern.objects.filter(user=session_user)
        hull_patterns = Hull_pattern.objects.filter(user=session_user)
        armor_patterns = Armor_pattern.objects.filter(user=session_user)
        shield_patterns = Shield_pattern.objects.filter(user=session_user)
        engine_patterns = Engine_pattern.objects.filter(user=session_user)
        generator_patterns = Generator_pattern.objects.filter(user=session_user)
        weapon_patterns = Weapon_pattern.objects.filter(user=session_user)
        shell_patterns = Shell_pattern.objects.filter(user=session_user)
        module_patterns = Module_pattern.objects.filter(user=session_user)
        device_patterns = Device_pattern.objects.filter(user=session_user)
        trade_spaces = Trade_space.objects.filter()
        ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city)
        project_ships = Project_ship.objects.filter(user=session_user)
        users = MyUser.objects.filter()
        trade_space = Trade_space.objects.filter(id=trade_space_id).first()
        trade_elements = Trade_element.objects.filter(trade_space=trade_space_id)
        trade_building = Building_installed.objects.filter(user=session_user, user_city=session_user_city,
                                                           production_class=13).first()
        delivery_queues = Delivery_queue.objects.filter(user=session_user, user_city=session_user_city)
        user_trade_elements = Trade_element.objects.filter(user = session_user)
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True

        output = {'user': user, 'warehouses': warehouses, 'user_city': user_city, 'user_citys': user_citys,
                  'basic_resources': basic_resources,
                  'warehouse_factorys': warehouse_factorys, 'factory_patterns': factory_patterns,
                  'warehouse_elements': warehouse_elements, 'hull_patterns': hull_patterns,
                  'armor_patterns': armor_patterns, 'shield_patterns': shield_patterns,
                  'engine_patterns': engine_patterns, 'generator_patterns': generator_patterns,
                  'weapon_patterns': weapon_patterns, 'shell_patterns': shell_patterns, 'device_patterns':device_patterns,
                  'module_patterns': module_patterns, 'trade_spaces': trade_spaces, 'trade_space_id': trade_space_id,
                  'project_ships': project_ships, 'ships': ships, 'trade_elements': trade_elements, 'users': users, 'user_trade_elements':user_trade_elements,
                  'trade_space': trade_space, 'message': message, 'trade_building': trade_building, 'delivery_queues': delivery_queues}
        return render(request, "trade.html", output)