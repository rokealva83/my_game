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
        trade_space_id = 1
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
        trade_elements = Trade_element.objects.filter()
        ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city)
        project_ships = Project_ship.objects.filter(user=session_user)
        users = MyUser.objects.filter()

        trade_id = request.POST.get('trade_space_id')
        if trade_id is not None:
            password = request.POST.get('password')
            trade_space = Trade_space.objects.filter(id=trade_id).first()
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
                      'trade_space_id': trade_space_id, 'project_ships': project_ships, 'ships': ships,
                      'trade_elements': trade_elements, 'users': users, 'message': message}
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
                  'project_ships': project_ships, 'ships': ships, 'trade_elements': trade_elements, 'users': users}
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
        trade_elements = Trade_element.objects.filter()
        ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city)
        project_ships = Project_ship.objects.filter(user=session_user)
        users = MyUser.objects.filter()
        trade_spaces = Trade_space.objects.filter()

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
                  'project_ships': project_ships, 'ships': ships, 'trade_elements': trade_elements, 'users': users}
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
        trade_space_id = int(trade_space_id[0])

        name = myDict.get('name')
        name = name[0]
        name = name.split(';')
        id_warehouse_element = int(name[0])
        class_element = int(name[1])

        amount = myDict.get('amount')
        amount = int(amount[0])
        price = myDict.get('price')
        price = int(price[0])
        unit_price = myDict.get('unit_price')
        unit_price = int(unit_price[0])
        minimum_lot = myDict.get('minimum_lot')
        minimum_lot = int(minimum_lot[0])

        personal_rate = myDict.get('personal_rate')
        personal_rate = personal_rate[0]
        if personal_rate == 'Empty':
            id_personal = 0
        else:
            user = MyUser.objects.filter(user_name=personal_rate).first()
            id_personal = int(user.user_id)

        notify = myDict.get('notify')
        if notify is not None:
            notify = notify[0]

        ban = myDict.get('ban')
        ban = int(ban[0])

        if class_element == 0:
            warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).first()
            if id_warehouse_element == 1:
                if warehouse.resource1 >= amount:
                    name = 'Resource 1'
                    new_amount = warehouse.resource1 - amount
                    warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).update(
                        resource1=new_amount)
                else:
                    message = 'Не верное количество товара'

            elif id_warehouse_element == 2:
                if warehouse.resource2 >= amount:
                    name = 'Resource 2'
                    new_amount = warehouse.resource2 - amount
                    warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).update(
                        resource2=new_amount)
                else:
                    message = 'Не верное количество товара'

            elif id_warehouse_element == 3:
                if warehouse.resource3 >= amount:
                    name = 'Resource 3'
                    new_amount = warehouse.resource3 - amount
                    warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).update(
                        resource3=new_amount)
                else:
                    message = 'Не верное количество товара'

            elif id_warehouse_element == 4:
                if warehouse.resource4 >= amount:
                    name = 'Resource 4'
                    new_amount = warehouse.resource4 - amount
                    warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).update(
                        resource4=new_amount)
                else:
                    message = 'Не верное количество товара'

            elif id_warehouse_element == 5:
                if warehouse.mineral1 >= amount:
                    name = 'Mineral1'
                    new_amount = warehouse.mineral1 - amount
                    warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).update(
                        mineral1=new_amount)
                else:
                    message = 'Не верное количество товара'

            elif id_warehouse_element == 6:
                if warehouse.mineral2 >= amount:
                    name = 'Mineral 2'
                    new_amount = warehouse.mineral2 - amount
                    warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).update(
                        mineral2=new_amount)
                else:
                    message = 'Не верное количество товара'

            elif id_warehouse_element == 7:
                if warehouse.mineral3 >= amount:
                    name = 'Mineral 3'
                    new_amount = warehouse.mineral3 - amount
                    warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).update(
                        mineral3=new_amount)
                else:
                    message = 'Не верное количество товара'

            elif id_warehouse_element == 8:
                if warehouse.mineral4 >= amount:
                    name = 'Mineral 4'
                    new_amount = warehouse.mineral4 - amount
                    warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).update(
                        mineral4=new_amount)
                else:
                    message = 'Не верное количество товара'

        elif class_element == 1:
            warehouse_element = Warehouse_element.objects.filter(id=id_warehouse_element).first()
            if warehouse_element.amount >= amount:
                hull = Hull_pattern.objects.filter(id=warehouse_element.element_id).first()
                basic_hull = Basic_hull.objects.filter(id=hull.basic_id).first()
                new_amount = warehouse_element.amount - amount
                name = basic_hull.name
                warehouse_element = Warehouse_element.objects.filter(id=id_warehouse_element).update(amount=new_amount)
                id_element = hull.id

        elif class_element == 2:
            warehouse_element = Warehouse_element.objects.filter(id=id_warehouse_element).first()
            if warehouse_element.amount >= amount:
                armor = Armor_pattern.objects.filter(id=warehouse_element.element_id).first()
                basic_armor = Basic_armor.objects.filter(id=armor.basic_id).first()
                new_amount = warehouse_element.amount - amount
                name = basic_armor.name
                warehouse_element = Warehouse_element.objects.filter(id=id_warehouse_element).update(amount=new_amount)
                id_element = armor.id

        elif class_element == 3:
            warehouse_element = Warehouse_element.objects.filter(id=id_warehouse_element).first()
            if warehouse_element.amount >= amount:
                shield = Shield_pattern.objects.filter(id=warehouse_element.element_id).first()
                basic_shield = Basic_shield.objects.filter(id=shield.basic_id).first()
                new_amount = warehouse_element.amount - amount
                name = basic_shield.name
                warehouse_element = Warehouse_element.objects.filter(id=id_warehouse_element).update(amount=new_amount)
                id_element = shield.id

        elif class_element == 4:
            warehouse_element = Warehouse_element.objects.filter(id=id_warehouse_element).first()
            if warehouse_element.amount >= amount:
                engine = Engine_pattern.objects.filter(id=warehouse_element.element_id).first()
                basic_engine = Basic_engine.objects.filter(id=engine.basic_id).first()
                new_amount = warehouse_element.amount - amount
                name = basic_engine.name
                warehouse_element = Warehouse_element.objects.filter(id=id_warehouse_element).update(amount=new_amount)
                id_element = engine.id

        elif class_element == 5:
            warehouse_element = Warehouse_element.objects.filter(id=id_warehouse_element).first()
            if warehouse_element.amount >= amount:
                generator = Generator_pattern.objects.filter(id=warehouse_element.element_id).first()
                basic_generator = Basic_generator.objects.filter(id=generator.basic_id).first()
                new_amount = warehouse_element.amount - amount
                name = basic_generator.name
                warehouse_element = Warehouse_element.objects.filter(id=id_warehouse_element).update(amount=new_amount)
                id_element = generator.id

        elif class_element == 6:
            warehouse_element = Warehouse_element.objects.filter(id=id_warehouse_element).first()
            if warehouse_element.amount >= amount:
                weapon = Weapon_pattern.objects.filter(id=warehouse_element.element_id).first()
                basic_weapon = Basic_weapon.objects.filter(id=weapon.basic_id).first()
                new_amount = warehouse_element.amount - amount
                name = basic_weapon.name
                warehouse_element = Warehouse_element.objects.filter(id=id_warehouse_element).update(amount=new_amount)
                id_element = weapon.id

        elif class_element == 7:
            warehouse_element = Warehouse_element.objects.filter(id=id_warehouse_element).first()
            if warehouse_element.amount >= amount:
                shell = Shell_pattern.objects.filter(id=warehouse_element.element_id).first()
                basic_shell = Basic_shell.objects.filter(id=shell.basic_id).first()
                new_amount = warehouse_element.amount - amount
                name = basic_shell.name
                warehouse_element = Warehouse_element.objects.filter(id=id_warehouse_element).update(amount=new_amount)
                id_element = shell.id

        elif class_element == 8:
            warehouse_element = Warehouse_element.objects.filter(id=id_warehouse_element).first()
            if warehouse_element.amount >= amount:
                module = Module_pattern.objects.filter(id=warehouse_element.element_id).first()
                basic_module = Basic_module.objects.filter(id=module.basic_id).first()
                new_amount = warehouse_element.amount - amount
                name = basic_module.name
                warehouse_element = Warehouse_element.objects.filter(id=id_warehouse_element).update(amount=new_amount)
                id_element = module.id

        elif class_element == 10:
            warehouse_factory = Warehouse_factory.objects.filter(id=id_warehouse_element).first()
            if warehouse_factory.amount >= amount:
                factory = Factory_pattern.objects.filter(id=warehouse_factory.factory_id).first()
                basic_factory = Basic_factory.objects.filter(id=factory.basic_id).first()
                new_amount = warehouse_factory.amount - amount
                name = basic_factory.name
                warehouse_factory = Warehouse_factory.objects.filter(id=id_warehouse_element).update(amount=new_amount)
                id_element = factory.id

        elif class_element == 11:
            ship = Ship.objects.filter(id=id_warehouse_element).first()
            if ship.amount_ship >= amount:
                project_ship = Project_ship.objects.filter(id=ship.id_project_ship).first()
                new_amount = ship.amount_ship - amount
                name = project_ship.name
                ship = Ship.objects.filter(id=id_warehouse_element).update(amount_ship=new_amount)
                id_element = ship.id_project_ship

        user_city = User_city.objects.filter(id=session_user_city).first()
        trade_element = Trade_element(
            name=name,
            user=session_user,
            buyer=id_personal,
            trade_space=trade_space_id,
            class_element=class_element,
            id_element=id_element,
            amount=amount,
            min_amount=minimum_lot,
            cost=price,
            cost_element=unit_price,
            diplomacy=ban,
            x=user_city.x,
            y=user_city.y,
            z=user_city.z,
        )
        trade_element.save()

        function.check_all_queues(session_user)
        trade_space_id = request.POST.get('trade_space_id')

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
        trade_elements = Trade_element.objects.filter()
        ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city)
        project_ships = Project_ship.objects.filter(user=session_user)
        users = MyUser.objects.filter()
        trade_spaces = Trade_space.objects.filter()
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
                  'project_ships': project_ships, 'ships': ships, 'trade_elements': trade_elements, 'users': users}
        return render(request, "trade.html", output)


def del_trade(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)

        full_request = request.POST
        myDict = dict(full_request.iterlists())
        trade_space_id = myDict.get('trade_space_id')
        trade_space_id = int(trade_space_id[0])
        id_element = myDict.get('trade_del')
        id_element = int(id_element[0])

        trade_element = Trade_element.objects.filter(id=id_element).first()
        if trade_element.class_element == 0:
            warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).first()
            if trade_element.id_element == 1:
                new_amount = warehouse.resource1 + trade_element.amount
                warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).update(
                    resource1=new_amount)

            if trade_element.id_element == 2:
                new_amount = warehouse.resource2 + trade_element.amount
                warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).update(
                    resource2=new_amount)
            if trade_element.id_element == 3:
                new_amount = warehouse.resource3 + trade_element.amount
                warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).update(
                    resource3=new_amount)
            if trade_element.id_element == 4:
                new_amount = warehouse.resource4 + trade_element.amount
                warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).update(
                    resource4=new_amount)
            if trade_element.id_element == 5:
                new_amount = warehouse.mineral1 + trade_element.amount
                warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).update(
                    mineral1=new_amount)
            if trade_element.id_element == 6:
                new_amount = warehouse.mineral2 + trade_element.amount
                warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).update(
                    mineral2=new_amount)
            if trade_element.id_element == 7:
                new_amount = warehouse.mineral3 + trade_element.amount
                warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).update(
                    mineral3=new_amount)
            if trade_element.id_element == 8:
                new_amount = warehouse.mineral4 + trade_element.amount
                warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).update(
                    mineral4=new_amount)
        elif 0 < trade_element.class_element < 9:
            warehouse_element = Warehouse_element.objects.filter(user=session_user, user_city=session_user_city,
                                                                 element_class=trade_element.class_element,
                                                                 element_id=trade_element.id_element).first()
            if warehouse_element:
                new_amount = warehouse_element.amount + trade_element.amount
                warehouse_element = Warehouse_element.objects.filter(user=session_user, user_city=session_user_city,
                                                                     element_class=trade_element.class_element,
                                                                     element_id=trade_element.id_element).update(
                    amount=new_amount)
            else:
                warehouse_element = Warehouse_element(
                    user=session_user,
                    user_city=session_user_city,
                    element_class=trade_element.class_element,
                    element_id=trade_element.id_element
                )
                warehouse_element.save()

        elif trade_element.class_element == 10:
            warehouse_factory = Warehouse_factory.objects.filter(user=session_user, user_city=session_user_city,
                                                                 factory_id=trade_element.id_element).first()
            if warehouse_factory:
                new_amount = warehouse_factory.amount + trade_element.amount
                warehouse_factory = Warehouse_factory.objects.filter(user=session_user, user_city=session_user_city,
                                                                     factory_id=trade_element.id_element).update(
                    amount=new_amount)
            else:
                factory_pattern = Factory_pattern.objects.filter(id=trade_element.id_element).first()
                warehouse_factory = Warehouse_factory(
                    user=session_user,
                    user_city=session_user_city,
                    factory_id=trade_element.id_element,
                    production_class=factory_pattern.production_class,
                    production_id=factory_pattern.production_id,
                    time_production=factory_pattern.time_production,
                    amount=trade_element.amount,
                    size=factory_pattern.size,
                    mass=factory_pattern.mass,
                    power_consumption=factory_pattern.power_consumption
                )
                warehouse_factory.save()

        elif trade_element.class_element == 11:
            ship = Ship.objects.filter(user=session_user, place_id=session_user_city, id_ship_project=id_element,
                                       fleet_status=0).first()
            if ship:
                new_amount = ship.amount_ship + trade_element.amount
                ship = Ship.objects.filter(user=session_user, place_id=session_user_city, id_ship_project=id_element,
                                           fleet_status=0).update(amount_ship=new_amount)
            else:
                project_ship = Project_ship.objects.filter(id = id_element).first()
                ship = Ship(
                    user = session_user,
                    id_project_ship = id_element,
                    amount_ship = trade_element.amount,
                    fleet_status = 0,
                    place_id = session_user_city,
                    name = project_ship.name
                )
                ship.save()
        trade_element = Trade_element.objects.filter(id=id_element).delete()

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
        trade_elements = Trade_element.objects.filter()
        ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city)
        project_ships = Project_ship.objects.filter(user=session_user)
        users = MyUser.objects.filter()
        trade_spaces = Trade_space.objects.filter()
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
                  'project_ships': project_ships, 'ships': ships, 'trade_elements': trade_elements, 'users': users}
        return render(request, "trade.html", output)