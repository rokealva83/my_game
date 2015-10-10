# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity, Warehouse, BasicResource
from my_game.models import HullPattern, ShieldPattern, GeneratorPattern, EnginePattern, \
    ArmorPattern, ModulePattern, WeaponPattern, ShellPattern, FactoryPattern, DevicePattern
from my_game.models import WarehouseElement, WarehouseFactory
from my_game import function
from my_game.models import ProjectShip, Ship
from my_game.models import TradeElement, TradeSpace, BuildingInstalled, DeliveryQueue


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
        basic_resources = BasicResource.objects.filter()
        user_city = UserCity.objects.filter(user=session_user).first()
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
                user = MyUser.objects.filter(user_id=session_user).update(internal_currency=new_internal_currency,
                                                                          foreigh_currency=new_foreigh_currency)
                message = 'Покупка совершена'
            else:
                message = 'Нехватка внутренней валюты'
        else:
            if foreigh_currency >= amount_foreigh:
                bought_currency = amount_foreigh * 495
                new_internal_currency = internal_currency + bought_currency
                new_foreigh_currency = foreigh_currency - amount_foreigh
                user = MyUser.objects.filter(user_id=session_user).update(internal_currency=new_internal_currency,
                                                                          foreigh_currency=new_foreigh_currency)
                message = 'Продажа совершена'
        user_citys = UserCity.objects.filter(user=int(session_user))
        user = MyUser.objects.filter(user_id=session_user).first()
        warehouse_elements = WarehouseElement.objects.filter(user=session_user, user_city=session_user_city).order_by(
            'element_class', 'element_id')
        warehouse_factorys = WarehouseFactory.objects.filter(user=session_user, user_city=session_user_city).order_by(
            'production_class', 'production_id')
        factory_patterns = FactoryPattern.objects.filter(user=session_user)
        hull_patterns = HullPattern.objects.filter(user=session_user)
        armor_patterns = ArmorPattern.objects.filter(user=session_user)
        shield_patterns = ShieldPattern.objects.filter(user=session_user)
        engine_patterns = EnginePattern.objects.filter(user=session_user)
        generator_patterns = GeneratorPattern.objects.filter(user=session_user)
        weapon_patterns = WeaponPattern.objects.filter(user=session_user)
        shell_patterns = ShellPattern.objects.filter(user=session_user)
        module_patterns = ModulePattern.objects.filter(user=session_user)
        device_patterns = DevicePattern.objects.filter(user=session_user)
        trade_spaces = TradeSpace.objects.filter()
        ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city)
        project_ships = ProjectShip.objects.filter(user=session_user)
        users = MyUser.objects.filter()
        trade_space = TradeSpace.objects.filter(id=trade_space_id).first()
        trade_elements = TradeElement.objects.filter(trade_space=trade_space_id)
        trade_building = BuildingInstalled.objects.filter(user=session_user, user_city=session_user_city,
                                                           production_class=13).first()
        delivery_queues = DeliveryQueue.objects.filter(user=session_user, user_city=session_user_city)
        user_trade_elements = TradeElement.objects.filter(user=session_user)
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True

        output = {'user': user, 'warehouses': warehouses, 'user_city': user_city, 'user_citys': user_citys,
                  'basic_resources': basic_resources,
                  'warehouse_factorys': warehouse_factorys, 'factory_patterns': factory_patterns,
                  'warehouse_elements': warehouse_elements, 'hull_patterns': hull_patterns,
                  'armor_patterns': armor_patterns, 'shield_patterns': shield_patterns,
                  'engine_patterns': engine_patterns, 'generator_patterns': generator_patterns,
                  'weapon_patterns': weapon_patterns, 'shell_patterns': shell_patterns,
                  'device_patterns': device_patterns,
                  'module_patterns': module_patterns, 'trade_spaces': trade_spaces, 'trade_space_id': trade_space_id,
                  'project_ships': project_ships, 'ships': ships, 'trade_elements': trade_elements, 'users': users,
                  'user_trade_elements': user_trade_elements,
                  'trade_space': trade_space, 'message': message, 'trade_building': trade_building,
                  'delivery_queues': delivery_queues}
        return render(request, "trade.html", output)