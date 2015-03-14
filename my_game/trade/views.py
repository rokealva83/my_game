# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from django.shortcuts import render
from my_game.models import MyUser, User_city, Warehouse
from my_game.models import Hull_pattern, Shield_pattern, Generator_pattern, Engine_pattern, \
    Armor_pattern, Module_pattern, Weapon_pattern, Shell_pattern, Factory_pattern
from my_game.models import Basic_armor, Basic_factory, Basic_engine, Basic_generator, Basic_hull, Basic_module, \
    Basic_shell, Basic_shield, Basic_weapon, Basic_scientic
from my_game.models import Warehouse_element, Warehouse_factory
from my_game import function
from my_game.models import Project_ship, Element_ship, Turn_ship_build, Ship
from my_game.models import Trade_element, Trade_space


def trade(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        message = ''
        warehouse = Warehouse.objects.filter(user=session_user).first()
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = User_city.objects.filter(user=int(session_user))
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
        trade_spaces = Trade_space.objects.filter()
        ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city)
        project_ships = Project_ship.objects.filter(user=session_user)

        trade_space_id = request.POST.get('trade_space_id')
        if trade_space_id is not None:
            password = request.POST.get('password')
            trade_space = Trade_space.objects.filter(id=trade_space_id).first()
            trade_pass = trade_space.password
            if password == trade_space.password:
                message = 'Правильный пароль'
            else:
                message = 'Неправильный пароль'

            request.session['userid'] = session_user
            request.session['user_city'] = session_user_city
            request.session['live'] = True
            output = {'user': user, 'warehouse': warehouse, 'user_city': user_city, 'user_citys': user_citys,
                      'warehouse_factorys': warehouse_factorys, 'factory_patterns': factory_patterns,
                      'warehouse_elements': warehouse_elements, 'hull_patterns': hull_patterns,
                      'armor_patterns': armor_patterns, 'shield_patterns': shield_patterns,
                      'engine_patterns': engine_patterns, 'generator_patterns': generator_patterns,
                      'weapon_patterns': weapon_patterns, 'shell_patterns': shell_patterns,
                      'module_patterns': module_patterns, 'trade_spaces': trade_spaces,
                      'trade_space_id': trade_space_id,
                      'project_ships': project_ships, 'ships': ships, 'message': message}
            return render(request, "trade.html", output)
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True

        output = {'user': user, 'warehouse': warehouse, 'user_city': user_city, 'user_citys': user_citys,
                  'warehouse_factorys': warehouse_factorys, 'factory_patterns': factory_patterns,
                  'warehouse_elements': warehouse_elements, 'hull_patterns': hull_patterns,
                  'armor_patterns': armor_patterns, 'shield_patterns': shield_patterns,
                  'engine_patterns': engine_patterns, 'generator_patterns': generator_patterns,
                  'weapon_patterns': weapon_patterns, 'shell_patterns': shell_patterns,
                  'module_patterns': module_patterns, 'trade_spaces': trade_spaces, 'trade_space_id': trade_space_id,
                  'project_ships': project_ships, 'ships': ships}
        return render(request, "trade.html", output)


def new_trade_space(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        trade_space_id = request.POST.get('trade_space_id')
        name = request.POST.get('name')
        password = request.POST.get('pass')
        tax = request.POST.get('tax')
        trade_space = Trade_space(
            name=name,
            user=session_user,
            password=password,
            tax=tax
        )
        trade_space.save()
        warehouse = Warehouse.objects.filter(user=session_user).first()
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = User_city.objects.filter(user=int(session_user))
        trade_spaces = Trade_space.objects.filter()
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouse': warehouse, 'user_city': user_city, 'user_citys': user_citys,
                  'trade_spaces': trade_spaces, 'trade_space_id': trade_space_id}
        return render(request, "trade.html", output)


def add_trade_element(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        full_request = request.POST
        myDict = dict(full_request.iterlists())

        trade_space_id = myDict.get('trade_space_id')
        if trade_space_id is not None:
            trade_space_id = trade_space_id[0]
        else:
            trade_space_id = 0

        name = myDict.get('name')
        name = name[0]
        name = name.split(';')
        id_warehouse_element = name[0]
        class_element = name[1]

        amount = myDict.get('amount')
        amount = amount[0]
        price = myDict.get('price')
        price = price[0]
        unit_price = myDict.get('unit_price')
        unit_price = unit_price[0]
        minimum_lot = myDict.get('minimum_lot')
        minimum_lot = minimum_lot[0]

        personal_rate = myDict.get('personal_rate')
        personal_rate = personal_rate[0]

        notify = myDict.get('notify')
        if notify is not None:
            notify = notify[0]

        if class_element == 0:
            if id_warehouse_element == 1:
                warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).first()
                if warehouse.resource1 >= amount:
                    name = 'Resource 1'
                    new_amount = warehouse.resource1 - amount
                else:
                    message = 'Не верное количество товара'

            elif id_warehouse_element == 2:
                warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).first()
                if warehouse.resource2 >= amount:
                    name = 'Resource 2'

            elif id_warehouse_element == 3:
                name = 'Resource 3'
            elif id_warehouse_element == 4:
                name = 'Resource 4'
            elif id_warehouse_element == 5:
                name = 'Mineral 1'
            elif id_warehouse_element == 6:
                name = 'Mineral 2'
            elif id_warehouse_element == 7:
                name = 'Mineral 3'
            elif id_warehouse_element == 8:
                name = 'Mineral 4'

        elif class_element == 1:
            warehouse_element = Warehouse_element.objects.filter(id=id_warehouse_element).first()
            if warehouse_element.amount >= amount:
                hull = Hull_pattern.objects.filter(id=warehouse_element.element_id).first()
                basic_hull = Basic_hull.objects.filter(id = hull.basic_id).first()
                name = basic_hull.name

        elif class_element == 2:
        elif class_element == 3:
        elif class_element == 4:
        elif class_element == 5:
        elif class_element == 6:
        elif class_element == 7:
        elif class_element == 8:
        elif class_element == 10:
        elif class_element == 11:

        function.check_all_queues(session_user)
        trade_space_id = request.POST.get('trade_space_id')

        warehouse = Warehouse.objects.filter(user=session_user).first()
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = User_city.objects.filter(user=int(session_user))
        trade_spaces = Trade_space.objects.filter()
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouse': warehouse, 'user_city': user_city, 'user_citys': user_citys,
                  'trade_spaces': trade_spaces, 'trade_space_id': trade_space_id}
        return render(request, "trade.html", output)