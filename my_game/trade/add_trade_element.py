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
from my_game.models import TradeElement
from my_game.trade.create_trade_output import create_trade_output


def add_trade_element(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
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
        else:
            notify = ''
        ban = myDict.get('ban')
        ban = int(ban[0])

        if class_element == 0:
            warehouse = session_user_city.warehouse





            resource = BasicResource.objects.filter(id=id_warehouse_element).first()
            if warehouse.amount >= amount:
                amount = amount
            else:
                amount = warehouse.amount

            name = resource.name
            new_amount = warehouse.amount - amount
            Warehouse.objects.filter(user=session_user, user_city=session_user_city,
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
            WarehouseElement.objects.filter(id=id_warehouse_element).update(amount=new_amount)
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
            WarehouseElement.objects.filter(id=id_warehouse_element).update(amount=new_amount)
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
            WarehouseElement.objects.filter(id=id_warehouse_element).update(amount=new_amount)
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
            WarehouseElement.objects.filter(id=id_warehouse_element).update(amount=new_amount)
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
            WarehouseElement.objects.filter(id=id_warehouse_element).update(amount=new_amount)
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
            WarehouseElement.objects.filter(id=id_warehouse_element).update(amount=new_amount)
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
            WarehouseElement.objects.filter(id=id_warehouse_element).update(amount=new_amount)
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
            WarehouseElement.objects.filter(id=id_warehouse_element).update(amount=new_amount)
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
            WarehouseElement.objects.filter(id=id_warehouse_element).update(amount=new_amount)
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
            WarehouseFactory.objects.filter(id=id_warehouse_element).update(amount=new_amount)
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
        request.session['user'] = session_user.id
        request.session['user_city'] = session_user_city.id
        request.session['live'] = True
        output = create_trade_output(session_user, session_user_city, output, trade_space_id, message='')
        return render(request, "trade.html", output)
