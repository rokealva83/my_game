# -*- coding: utf-8 -*-


from django.shortcuts import render
from my_game.models import MyUser, UserCity, Warehouse
from my_game.models import HullPattern, ShieldPattern, GeneratorPattern, EnginePattern, \
    ArmorPattern, ModulePattern, WeaponPattern, ShellPattern, FactoryPattern, DevicePattern
from my_game.models import WarehouseElement, WarehouseFactory
from my_game import function
from my_game.models import ProjectShip, Ship
from my_game.models import TradeElement, TradeSpace, BuildingInstalled, DeliveryQueue


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

        trade_element = TradeElement.objects.filter(id=id_element).first()
        if trade_element.user_city != session_user_city:
            message = 'Ставка из другого поселения'
        else:
            if trade_element.class_element == 0:
                warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city,
                                                     id_resource=trade_element.id_element).first()

                new_amount = warehouse.amount + trade_element.amount
                warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city,
                                                     id_resource=trade_element.id_element).update(amount=new_amount)

            elif 0 < trade_element.class_element < 10:
                warehouse_element = WarehouseElement.objects.filter(user=session_user, user_city=session_user_city,
                                                                     element_class=trade_element.class_element,
                                                                     element_id=trade_element.id_element).first()
                if warehouse_element:
                    new_amount = warehouse_element.amount + trade_element.amount
                    warehouse_element = WarehouseElement.objects.filter(user=session_user, user_city=session_user_city,
                                                                         element_class=trade_element.class_element,
                                                                         element_id=trade_element.id_element).update(
                        amount=new_amount)
                else:
                    warehouse_element = WarehouseElement(
                        user=session_user,
                        user_city=session_user_city,
                        element_class=trade_element.class_element,
                        element_id=trade_element.id_element
                    )
                    warehouse_element.save()

            elif trade_element.class_element == 10:
                warehouse_factory = WarehouseFactory.objects.filter(user=session_user, user_city=session_user_city,
                                                                     factory_id=trade_element.id_element).first()
                if warehouse_factory:
                    new_amount = warehouse_factory.amount + trade_element.amount
                    warehouse_factory = WarehouseFactory.objects.filter(user=session_user, user_city=session_user_city,
                                                                         factory_id=trade_element.id_element).update(
                        amount=new_amount)
                else:
                    factory_pattern = FactoryPattern.objects.filter(id=trade_element.id_element).first()
                    warehouse_factory = WarehouseFactory(
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
                    ship = Ship.objects.filter(user=session_user, place_id=session_user_city,
                                               id_ship_project=id_element,
                                               fleet_status=0).update(amount_ship=new_amount)
                else:
                    project_ship = ProjectShip.objects.filter(id=id_element).first()
                    ship = Ship(
                        user=session_user,
                        id_project_ship=id_element,
                        amount_ship=trade_element.amount,
                        fleet_status=0,
                        place_id=session_user_city,
                        name=project_ship.name
                    )
                    ship.save()
            trade_element = TradeElement.objects.filter(id=id_element).delete()

        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('resource_id')
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