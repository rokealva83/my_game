# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity, Warehouse, Planet
from my_game.models import HullPattern, ShieldPattern, GeneratorPattern, EnginePattern, \
    ArmorPattern, ModulePattern, WeaponPattern, ShellPattern, FactoryPattern, DevicePattern
from my_game.models import BasicArmor, BasicFactory, BasicEngine, BasicGenerator, BasicHull, BasicModule, \
    BasicShell, BasicShield, BasicWeapon, BasicDevice
from my_game.models import WarehouseElement, WarehouseFactory, BasicResource
from my_game import function
from my_game.models import ProjectShip, Ship
from my_game.models import TradeElement, TradeSpace, BuildingInstalled, DeliveryQueue


def add_trade_element(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)

        mass_element = 0
        size_element = 0
        id_element = 0

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
            resource = BasicResource.objects.filter(id=id_warehouse_element).first()
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
            warehouse_element = WarehouseElement.objects.filter(id=id_warehouse_element).first()
            if warehouse_element.amount >= amount:
                amount = amount
            else:
                amount = warehouse_element.amount
            hull = HullPattern.objects.filter(id=warehouse_element.element_id).first()
            basic_hull = BasicHull.objects.filter(id=hull.basic_id).first()
            new_amount = warehouse_element.amount - amount
            name = basic_hull.name
            warehouse_element = WarehouseElement.objects.filter(id=id_warehouse_element).update(amount=new_amount)
            id_element = hull.id
            mass_element = hull.mass
            size_element = hull.size

        elif class_element == 2:
            warehouse_element = WarehouseElement.objects.filter(id=id_warehouse_element).first()
            if warehouse_element.amount >= amount:
                amount = amount
            else:
                amount = warehouse_element.amount
            armor = ArmorPattern.objects.filter(id=warehouse_element.element_id).first()
            basic_armor = BasicArmor.objects.filter(id=armor.basic_id).first()
            new_amount = warehouse_element.amount - amount
            name = basic_armor.name
            warehouse_element = WarehouseElement.objects.filter(id=id_warehouse_element).update(amount=new_amount)
            id_element = armor.id
            mass_element = armor.mass
            size_element = armor.size

        elif class_element == 3:
            warehouse_element = WarehouseElement.objects.filter(id=id_warehouse_element).first()
            if warehouse_element.amount >= amount:
                amount = amount
            else:
                amount = warehouse_element.amount
            shield = ShieldPattern.objects.filter(id=warehouse_element.element_id).first()
            basic_shield = BasicShield.objects.filter(id=shield.basic_id).first()
            new_amount = warehouse_element.amount - amount
            name = basic_shield.name
            warehouse_element = WarehouseElement.objects.filter(id=id_warehouse_element).update(amount=new_amount)
            id_element = shield.id
            mass_element = shield.mass
            size_element = shield.size

        elif class_element == 4:
            warehouse_element = WarehouseElement.objects.filter(id=id_warehouse_element).first()
            if warehouse_element.amount >= amount:
                amount = amount
            else:
                amount = warehouse_element.amount
            engine = EnginePattern.objects.filter(id=warehouse_element.element_id).first()
            basic_engine = BasicEngine.objects.filter(id=engine.basic_id).first()
            new_amount = warehouse_element.amount - amount
            name = basic_engine.name
            warehouse_element = WarehouseElement.objects.filter(id=id_warehouse_element).update(amount=new_amount)
            id_element = engine.id
            mass_element = engine.mass
            size_element = engine.size

        elif class_element == 5:
            warehouse_element = WarehouseElement.objects.filter(id=id_warehouse_element).first()
            if warehouse_element.amount >= amount:
                amount = amount
            else:
                amount = warehouse_element.amount
            generator = GeneratorPattern.objects.filter(id=warehouse_element.element_id).first()
            basic_generator = BasicGenerator.objects.filter(id=generator.basic_id).first()
            new_amount = warehouse_element.amount - amount
            name = basic_generator.name
            warehouse_element = WarehouseElement.objects.filter(id=id_warehouse_element).update(amount=new_amount)
            id_element = generator.id
            mass_element = generator.mass
            size_element = generator.size

        elif class_element == 6:
            warehouse_element = WarehouseElement.objects.filter(id=id_warehouse_element).first()
            if warehouse_element.amount >= amount:
                amount = amount
            else:
                amount = warehouse_element.amount
            weapon = WeaponPattern.objects.filter(id=warehouse_element.element_id).first()
            basic_weapon = BasicWeapon.objects.filter(id=weapon.basic_id).first()
            new_amount = warehouse_element.amount - amount
            name = basic_weapon.name
            warehouse_element = WarehouseElement.objects.filter(id=id_warehouse_element).update(amount=new_amount)
            id_element = weapon.id
            mass_element = weapon.mass
            size_element = weapon.size

        elif class_element == 7:
            warehouse_element = WarehouseElement.objects.filter(id=id_warehouse_element).first()
            if warehouse_element.amount >= amount:
                amount = amount
            else:
                amount = warehouse_element.amount
            shell = ShellPattern.objects.filter(id=warehouse_element.element_id).first()
            basic_shell = BasicShell.objects.filter(id=shell.basic_id).first()
            new_amount = warehouse_element.amount - amount
            name = basic_shell.name
            warehouse_element = WarehouseElement.objects.filter(id=id_warehouse_element).update(amount=new_amount)
            id_element = shell.id
            mass_element = shell.mass
            size_element = shell.size

        elif class_element == 8:
            warehouse_element = WarehouseElement.objects.filter(id=id_warehouse_element).first()
            if warehouse_element.amount >= amount:
                amount = amount
            else:
                amount = warehouse_element.amount
            module = ModulePattern.objects.filter(id=warehouse_element.element_id).first()
            basic_module = BasicModule.objects.filter(id=module.basic_id).first()
            new_amount = warehouse_element.amount - amount
            name = basic_module.name
            warehouse_element = WarehouseElement.objects.filter(id=id_warehouse_element).update(amount=new_amount)
            id_element = module.id
            mass_element = module.mass
            size_element = module.size

        elif class_element == 9:
            warehouse_element = WarehouseElement.objects.filter(id=id_warehouse_element).first()
            if warehouse_element.amount >= amount:
                amount = amount
            else:
                amount = warehouse_element.amount
            device = DevicePattern.objects.filter(id=warehouse_element.element_id).first()
            basic_device = BasicDevice.objects.filter(id=device.basic_id).first()
            new_amount = warehouse_element.amount - amount
            name = basic_device.name
            warehouse_element = WarehouseElement.objects.filter(id=id_warehouse_element).update(amount=new_amount)
            id_element = device.id
            mass_element = device.mass
            size_element = device.size

        elif class_element == 10:
            warehouse_factory = WarehouseFactory.objects.filter(id=id_warehouse_element).first()
            if warehouse_factory.amount >= amount:
                amount = amount
            else:
                amount = warehouse_factory.amount
            factory = FactoryPattern.objects.filter(id=warehouse_factory.factory_id).first()
            basic_factory = BasicFactory.objects.filter(id=factory.basic_id).first()
            new_amount = warehouse_factory.amount - amount
            name = basic_factory.name
            warehouse_factory = WarehouseFactory.objects.filter(id=id_warehouse_element).update(amount=new_amount)
            id_element = factory.id
            mass_element = factory.mass
            size_element = factory.size

        elif class_element == 11:
            ship = Ship.objects.filter(id=id_warehouse_element).first()
            if ship.amount_ship >= amount:
                amount = amount
            else:
                amount = ship.amount
            project_ship = ProjectShip.objects.filter(id=ship.id_project_ship).first()
            new_amount = ship.amount_ship - amount
            name = project_ship.name
            ship = Ship.objects.filter(id=id_warehouse_element).update(amount_ship=new_amount)
            id_element = ship.id_project_ship
            mass_element = ship.mass
            size_element = ship.size

        user_city = UserCity.objects.filter(id=session_user_city).first()
        planet = Planet.objects.filter(x=user_city.x, y=user_city.y, z=user_city.z).first()
        system_id = planet.system_id
        if planet:
            planet = 1
        else:
            planet = 0

        trade_element = TradeElement(
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
            planet=planet,
            user_city=session_user_city,
            mass_element=mass_element,
            size_element=size_element
        )
        trade_element.save()

        trade_space_id = request.POST.get('trade_space_id')

        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('id_resource')
        user_city = UserCity.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = UserCity.objects.filter(user=int(session_user))
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
        ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city)
        project_ships = ProjectShip.objects.filter(user=session_user)
        users = MyUser.objects.filter()
        trade_elements = TradeElement.objects.filter(trade_space=trade_space_id)
        user_trade_elements = TradeElement.objects.filter(trade_space=trade_space_id, user=session_user)
        trade_spaces = TradeSpace.objects.filter()
        trade_space = TradeSpace.objects.filter(id=trade_space_id).first()
        trade_building = BuildingInstalled.objects.filter(user=session_user, user_city=session_user_city,
                                                           production_class=13).first()
        delivery_queues = DeliveryQueue.objects.filter(user=session_user, user_city=session_user_city)
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouses': warehouses, 'user_city': user_city, 'user_citys': user_citys,
                  'warehouse_factorys': warehouse_factorys, 'factory_patterns': factory_patterns,
                  'warehouse_elements': warehouse_elements, 'hull_patterns': hull_patterns,
                  'armor_patterns': armor_patterns, 'shield_patterns': shield_patterns,
                  'engine_patterns': engine_patterns, 'generator_patterns': generator_patterns,
                  'weapon_patterns': weapon_patterns, 'shell_patterns': shell_patterns,
                  'device_patterns': device_patterns,
                  'module_patterns': module_patterns, 'trade_spaces': trade_spaces, 'trade_space_id': trade_space_id,
                  'project_ships': project_ships, 'ships': ships, 'trade_elements': trade_elements,
                  'user_trade_elements': user_trade_elements, 'users': users, 'trade_space': trade_space,
                  'trade_building': trade_building, 'delivery_queues': delivery_queues}
        return render(request, "trade.html", output)