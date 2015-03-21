# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, User_city, Warehouse, Planet, System
from my_game.models import Hull_pattern, Shield_pattern, Generator_pattern, Engine_pattern, \
    Armor_pattern, Module_pattern, Weapon_pattern, Shell_pattern, Factory_pattern
from my_game.models import Basic_armor, Basic_factory, Basic_engine, Basic_generator, Basic_hull, Basic_module, \
    Basic_shell, Basic_shield, Basic_weapon
from my_game.models import Warehouse_element, Warehouse_factory, Basic_resource
from my_game import function
from my_game.models import Project_ship, Ship
from my_game.models import Trade_element, Trade_space, Building_installed, Delivery_queue


def add_trade_element(request):
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
            warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city,
                                                 id_resource=id_warehouse_element).first()
            resource = Basic_resource.objects.filter(id=id_warehouse_element).first()
            if warehouse.amount >= amount:
                amount = amount
            else:
                amount = warehouse.amount

            name = resource.name
            new_amount = warehouse.amount - amount
            warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city,
                                                 id_resource=id_warehouse_element).update(amount=new_amount)
            id_element = id_warehouse_element
            mass_element = 1
            size_element = 1

        elif class_element == 1:
            warehouse_element = Warehouse_element.objects.filter(id=id_warehouse_element).first()
            if warehouse_element.amount >= amount:
                amount = amount
            else:
                amount = warehouse_element.amount
            hull = Hull_pattern.objects.filter(id=warehouse_element.element_id).first()
            basic_hull = Basic_hull.objects.filter(id=hull.basic_id).first()
            new_amount = warehouse_element.amount - amount
            name = basic_hull.name
            warehouse_element = Warehouse_element.objects.filter(id=id_warehouse_element).update(amount=new_amount)
            id_element = hull.id
            mass_element = hull.mass
            size_element = hull.size

        elif class_element == 2:
            warehouse_element = Warehouse_element.objects.filter(id=id_warehouse_element).first()
            if warehouse_element.amount >= amount:
                amount = amount
            else:
                amount = warehouse_element.amount
            armor = Armor_pattern.objects.filter(id=warehouse_element.element_id).first()
            basic_armor = Basic_armor.objects.filter(id=armor.basic_id).first()
            new_amount = warehouse_element.amount - amount
            name = basic_armor.name
            warehouse_element = Warehouse_element.objects.filter(id=id_warehouse_element).update(amount=new_amount)
            id_element = armor.id
            mass_element = armor.mass
            size_element = armor.size

        elif class_element == 3:
            warehouse_element = Warehouse_element.objects.filter(id=id_warehouse_element).first()
            if warehouse_element.amount >= amount:
                amount = amount
            else:
                amount = warehouse_element.amount
            shield = Shield_pattern.objects.filter(id=warehouse_element.element_id).first()
            basic_shield = Basic_shield.objects.filter(id=shield.basic_id).first()
            new_amount = warehouse_element.amount - amount
            name = basic_shield.name
            warehouse_element = Warehouse_element.objects.filter(id=id_warehouse_element).update(amount=new_amount)
            id_element = shield.id
            mass_element = shield.mass
            size_element = shield.size

        elif class_element == 4:
            warehouse_element = Warehouse_element.objects.filter(id=id_warehouse_element).first()
            if warehouse_element.amount >= amount:
                amount = amount
            else:
                amount = warehouse_element.amount
            engine = Engine_pattern.objects.filter(id=warehouse_element.element_id).first()
            basic_engine = Basic_engine.objects.filter(id=engine.basic_id).first()
            new_amount = warehouse_element.amount - amount
            name = basic_engine.name
            warehouse_element = Warehouse_element.objects.filter(id=id_warehouse_element).update(amount=new_amount)
            id_element = engine.id
            mass_element = engine.mass
            size_element = engine.size

        elif class_element == 5:
            warehouse_element = Warehouse_element.objects.filter(id=id_warehouse_element).first()
            if warehouse_element.amount >= amount:
                amount = amount
            else:
                amount = warehouse_element.amount
            generator = Generator_pattern.objects.filter(id=warehouse_element.element_id).first()
            basic_generator = Basic_generator.objects.filter(id=generator.basic_id).first()
            new_amount = warehouse_element.amount - amount
            name = basic_generator.name
            warehouse_element = Warehouse_element.objects.filter(id=id_warehouse_element).update(amount=new_amount)
            id_element = generator.id
            mass_element = generator.mass
            size_element = generator.size

        elif class_element == 6:
            warehouse_element = Warehouse_element.objects.filter(id=id_warehouse_element).first()
            if warehouse_element.amount >= amount:
                amount = amount
            else:
                amount = warehouse_element.amount
            weapon = Weapon_pattern.objects.filter(id=warehouse_element.element_id).first()
            basic_weapon = Basic_weapon.objects.filter(id=weapon.basic_id).first()
            new_amount = warehouse_element.amount - amount
            name = basic_weapon.name
            warehouse_element = Warehouse_element.objects.filter(id=id_warehouse_element).update(amount=new_amount)
            id_element = weapon.id
            mass_element = weapon.mass
            size_element = weapon.size

        elif class_element == 7:
            warehouse_element = Warehouse_element.objects.filter(id=id_warehouse_element).first()
            if warehouse_element.amount >= amount:
                amount = amount
            else:
                amount = warehouse_element.amount
            shell = Shell_pattern.objects.filter(id=warehouse_element.element_id).first()
            basic_shell = Basic_shell.objects.filter(id=shell.basic_id).first()
            new_amount = warehouse_element.amount - amount
            name = basic_shell.name
            warehouse_element = Warehouse_element.objects.filter(id=id_warehouse_element).update(amount=new_amount)
            id_element = shell.id
            mass_element = shell.mass
            size_element = shell.size

        elif class_element == 8:
            warehouse_element = Warehouse_element.objects.filter(id=id_warehouse_element).first()
            if warehouse_element.amount >= amount:
                amount = amount
            else:
                amount = warehouse_element.amount
            module = Module_pattern.objects.filter(id=warehouse_element.element_id).first()
            basic_module = Basic_module.objects.filter(id=module.basic_id).first()
            new_amount = warehouse_element.amount - amount
            name = basic_module.name
            warehouse_element = Warehouse_element.objects.filter(id=id_warehouse_element).update(amount=new_amount)
            id_element = module.id
            mass_element = module.mass
            size_element = module.size

        elif class_element == 10:
            warehouse_factory = Warehouse_factory.objects.filter(id=id_warehouse_element).first()
            if warehouse_factory.amount >= amount:
                amount = amount
            else:
                amount = warehouse_factory.amount
            factory = Factory_pattern.objects.filter(id=warehouse_factory.factory_id).first()
            basic_factory = Basic_factory.objects.filter(id=factory.basic_id).first()
            new_amount = warehouse_factory.amount - amount
            name = basic_factory.name
            warehouse_factory = Warehouse_factory.objects.filter(id=id_warehouse_element).update(amount=new_amount)
            id_element = factory.id
            mass_element = factory.mass
            size_element = factory.size

        elif class_element == 11:
            ship = Ship.objects.filter(id=id_warehouse_element).first()
            if ship.amount_ship >= amount:
                amount = amount
            else:
                amount = ship.amount
            project_ship = Project_ship.objects.filter(id=ship.id_project_ship).first()
            new_amount = ship.amount_ship - amount
            name = project_ship.name
            ship = Ship.objects.filter(id=id_warehouse_element).update(amount_ship=new_amount)
            id_element = ship.id_project_ship
            mass_element = ship.mass
            size_element = ship.size

        user_city = User_city.objects.filter(id=session_user_city).first()
        planet = Planet.objects.filter(x=user_city.x, y=user_city.y, z=user_city.z).first()
        system_id = planet.system_id
        if planet:
            planet = 1
            system = System.objects.filter(id=system_id).first()
            x = int(system.x) * 1000 + int(user_city.x)
            y = int(system.y) * 1000 + int(user_city.y)
            z = int(system.z) * 1000 + int(user_city.z)
        else:
            planet = 0
            x = (user_city.x) * 1000
            y = (user_city.y) * 1000
            z = (user_city.z) * 1000

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
            x=x,
            y=y,
            z=z,
            planet=planet,
            user_city=session_user_city,
            mass_element = mass_element,
            size_element = size_element
        )
        trade_element.save()

        trade_space_id = request.POST.get('trade_space_id')

        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('id_resource')
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
        ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city)
        project_ships = Project_ship.objects.filter(user=session_user)
        users = MyUser.objects.filter()
        trade_elements = Trade_element.objects.filter(trade_space=trade_space_id)
        user_trade_elements = Trade_element.objects.filter(trade_space=trade_space_id, user=session_user)
        trade_spaces = Trade_space.objects.filter()
        trade_space = Trade_space.objects.filter(id=trade_space_id).first()
        trade_building = Building_installed.objects.filter(user=session_user, user_city=session_user_city,
                                                           production_class=13).first()
        delivery_queues = Delivery_queue.objects.filter(user=session_user, user_city=session_user_city)
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouses': warehouses, 'user_city': user_city, 'user_citys': user_citys,
                  'warehouse_factorys': warehouse_factorys, 'factory_patterns': factory_patterns,
                  'warehouse_elements': warehouse_elements, 'hull_patterns': hull_patterns,
                  'armor_patterns': armor_patterns, 'shield_patterns': shield_patterns,
                  'engine_patterns': engine_patterns, 'generator_patterns': generator_patterns,
                  'weapon_patterns': weapon_patterns, 'shell_patterns': shell_patterns,
                  'module_patterns': module_patterns, 'trade_spaces': trade_spaces, 'trade_space_id': trade_space_id,
                  'project_ships': project_ships, 'ships': ships, 'trade_elements': trade_elements, 'users': users,
                  'user_trade_elements': user_trade_elements, 'users': users, 'trade_space': trade_space,
                  'trade_building': trade_building, 'delivery_queues': delivery_queues}
        return render(request, "trade.html", output)