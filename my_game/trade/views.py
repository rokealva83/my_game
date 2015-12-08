# -*- coding: utf-8 -*-


from django.shortcuts import render
from my_game.models import MyUser, UserCity, Warehouse, BasicResource
from my_game.models import Race, Planet
from my_game.models import HullPattern, ShieldPattern, GeneratorPattern, EnginePattern, \
    ArmorPattern, ModulePattern, WeaponPattern, ShellPattern, FactoryPattern, DevicePattern
from my_game.models import WarehouseElement, WarehouseFactory
from my_game import function
from my_game.models import ProjectShip, Ship
from my_game.models import TradeElement, TradeSpace, BuildingInstalled, DeliveryQueue


def trade(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['user'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        trade_building = BuildingInstalled.objects.filter(user=session_user, user_city=session_user_city,
                                                           production_class=21).first()
        if trade_building:
            message = ''
            trade_space_id = 1
            warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by(
                'resource_id')
            basic_resources = BasicResource.objects.filter()
            user_city = UserCity.objects.filter(user=session_user).first()
            user = MyUser.objects.filter(user_id=session_user).first()
            user_citys = UserCity.objects.filter(user=int(session_user))
            warehouse_elements = WarehouseElement.objects.filter(user=session_user,
                                                                  user_city=session_user_city).order_by(
                'element_class', 'element_id')
            warehouse_factorys = WarehouseFactory.objects.filter(user=session_user,
                                                                  user_city=session_user_city).order_by(
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
            trade_building = BuildingInstalled.objects.filter(user=session_user, user_city=session_user_city,
                                                               production_class=21).first()
            delivery_queues = DeliveryQueue.objects.filter(user=session_user, user_city=session_user_city)
            ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city)
            project_ships = ProjectShip.objects.filter(user=session_user)
            users = MyUser.objects.filter()
            trade_id = request.POST.get('trade_space_id')
            if trade_id is not None:
                password = request.POST.get('password')
                trade_space = TradeSpace.objects.filter(id=trade_id).first()
                trade_pass = trade_space.password
                if password == trade_space.password:
                    message = 'Правильный пароль'
                    trade_space_id = trade_id
                    trade_elements = TradeElement.objects.filter(trade_space=trade_space_id)
                    user_trade_elements = TradeElement.objects.filter(trade_space=trade_space_id, user=session_user)
                else:
                    message = 'Неправильный пароль'
                    trade_elements = TradeElement.objects.filter(trade_space=1)
                    user_trade_elements = TradeElement.objects.filter(trade_space=trade_space_id, user=session_user)

                request.session['userid'] = session_user
                request.session['user_city'] = session_user_city
                request.session['live'] = True
                output = {'user': user, 'warehouses': warehouses, 'basic_resources': basic_resources,
                          'user_city': user_city, 'user_citys': user_citys, 'warehouse_factorys': warehouse_factorys,
                          'factory_patterns': factory_patterns, 'warehouse_elements': warehouse_elements,
                          'hull_patterns': hull_patterns, 'armor_patterns': armor_patterns,
                          'shield_patterns': shield_patterns, 'engine_patterns': engine_patterns,
                          'generator_patterns': generator_patterns, 'weapon_patterns': weapon_patterns,
                          'shell_patterns': shell_patterns, 'module_patterns': module_patterns,
                          'device_patterns': device_patterns,
                          'trade_spaces': trade_spaces, 'trade_space_id': trade_space_id,
                          'project_ships': project_ships, 'ships': ships, 'trade_elements': trade_elements,
                          'user_trade_elements': user_trade_elements, 'users': users, 'message': message,
                          'trade_building': trade_building, 'delivery_queues': delivery_queues}
                return render(request, "trade.html", output)

            trade_space = TradeSpace.objects.filter(id=trade_space_id).first()
            trade_elements = TradeElement.objects.filter(trade_space=trade_space_id)
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
                      'device_patterns': device_patterns, 'module_patterns': module_patterns,
                      'trade_spaces': trade_spaces, 'trade_space_id': trade_space_id, 'project_ships': project_ships,
                      'ships': ships, 'trade_elements': trade_elements, 'users': users,
                      'user_trade_elements': user_trade_elements, 'trade_building': trade_building,
                      'trade_space': trade_space, 'delivery_queues': delivery_queues}
            return render(request, "trade.html", output)
        else:
            warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by(
                'resource_id')
            user = MyUser.objects.filter(user_id=session_user).first()
            user_city = UserCity.objects.filter(user=int(session_user)).first()
            user_citys = UserCity.objects.filter(user=int(session_user))
            planet = Planet.objects.filter(id=user_city.planet_id).first()
            race = Race.objects.filter(id=user.race_id).first()
            planets = Planet.objects.filter(id=user_city.planet_id)
            len_planet = len(planets)
            request.session['userid'] = session_user
            request.session['user_city'] = session_user_city
            request.session['live'] = True
            output = {'user': user, 'race': race, 'warehouses': warehouses, 'user_city': user_city,
                      'user_citys': user_citys,
                      'planet': planet, 'len_planet': len_planet}
            return render(request, "civilization.html", output)


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
        trade_space = TradeSpace(
            name=name,
            user=session_user,
            password=password,
            tax=tax
        )

        trade_space.save()
        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('resource_id')
        basic_resources = BasicResource.objects.filter()
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
        trade_elements = TradeElement.objects.filter(trade_space=trade_space_id)
        user_trade_elements = TradeElement.objects.filter(trade_space=trade_space_id, user=session_user)
        ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city)
        project_ships = ProjectShip.objects.filter(user=session_user)
        users = MyUser.objects.filter()
        trade_spaces = TradeSpace.objects.filter()
        trade_space = TradeSpace.objects.filter(id=trade_space_id).first()
        trade_building = BuildingInstalled.objects.filter(user=session_user, user_city=session_user_city,
                                                           production_class=21).first()
        delivery_queues = DeliveryQueue.objects.filter(user=session_user, user_city=session_user_city)
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
                  'device_patterns': device_patterns, 'module_patterns': module_patterns, 'trade_spaces': trade_spaces,
                  'trade_space_id': trade_space_id, 'project_ships': project_ships, 'ships': ships,
                  'trade_elements': trade_elements, 'user_trade_elements': user_trade_elements, 'users': users,
                  'trade_space': trade_space, 'trade_building': trade_building, 'delivery_queues': delivery_queues}
        return render(request, "trade.html", output)