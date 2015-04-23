# -*- coding: utf-8 -*-

from django.shortcuts import render
from datetime import datetime, timedelta
import math
from my_game.models import MyUser, User_city, Warehouse, Basic_resource, Planet, System
from my_game.models import Hull_pattern, Shield_pattern, Generator_pattern, Engine_pattern, \
    Armor_pattern, Module_pattern, Weapon_pattern, Shell_pattern, Factory_pattern, Device_pattern
from my_game.models import Warehouse_element, Warehouse_factory
from my_game import function
from my_game.trade import trade_function
from my_game.models import Project_ship, Ship, Fleet, Fleet_parametr_scan
from my_game.models import Trade_element, Trade_space, Delivery_queue, Building_installed, Trade_flight, Trade_teleport


def buy_trade(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        message = ''
        full_request = request.POST
        myDict = dict(full_request.iterlists())
        trade_space_id = myDict.get('trade_space_id')
        trade_space_id = int(trade_space_id[0])
        id_element = myDict.get('trade_buy')
        id_element = int(id_element[0])
        amount = myDict.get('amount')
        amount = int(amount[0])
        set_aside = myDict.get('set_aside')
        method = myDict.get('method')
        method = int(method[0])
        if amount > 0:
            trade_element = Trade_element.objects.filter(id=id_element).first()
            if amount == trade_element.amount:
                price_element = trade_element.cost
                new_price = 0
            elif trade_element.amount > amount:
                min_amount = trade_element.min_amount * 1.0
                delta = amount / min_amount
                delta = math.ceil(delta)
                amount = min_amount * delta
                if amount == trade_element.amount:
                    price_element = trade_element.cost
                    new_price = 0
                else:
                    min_cost = trade_element.cost_element
                    price_element = delta * min_cost
                    new_price = trade_element.cost - trade_element.cost / (
                        trade_element.amount / trade_element.min_amount) * delta
            user = MyUser.objects.filter(user_id=session_user).first()
            if user.foreigh_currency >= price_element:
                foreigh_currency = user.foreigh_currency
                new_foreigh_currency = foreigh_currency - price_element
                user = MyUser.objects.filter(user_id=session_user).update(foreigh_currency=new_foreigh_currency)
                seller = MyUser.objects.filter(user_id=trade_element.user).first()
                foreigh_currency = seller.foreigh_currency
                new_foreigh_currency = foreigh_currency + price_element
                seller = MyUser.objects.filter(user_id=trade_element.user).update(foreigh_currency=new_foreigh_currency)
                trade_element = Trade_element.objects.filter(id=id_element).update(cost=new_price)
                trade_element = Trade_element.objects.filter(id=id_element).first()
                if set_aside:
                    delivery_queue = Delivery_queue(
                        user=session_user,
                        user_city=session_user_city,
                        name=trade_element.name,
                        class_element=trade_element.class_element,
                        id_element=trade_element.id_element,
                        amount=amount,
                        method=0,
                        status=0,
                        x=trade_element.x,
                        y=trade_element.y,
                        z=trade_element.z,
                        mass_element=trade_element.mass_element,
                        size_element=trade_element.size_element
                    )
                    delivery_queue.save()
                    new_amount = trade_element.amount - amount
                    if new_amount == 0:
                        trade_element = Trade_element.objects.filter(id=id_element).delete()
                    else:
                        trade_element = Trade_element.objects.filter(id=id_element).update(amount=new_amount)
                    message = 'Товар поставлено в очередь на доставку'
                else:
                    user_city = User_city.objects.filter(id=session_user_city).first()
                    planet = Planet.objects.filter(x=user_city.x, y=user_city.y, z=user_city.z).first()
                    system_id = planet.system_id
                    if planet:
                        planet = 1
                        system = System.objects.filter(id=system_id).first()
                        x2 = int(system.x) * 1000 + int(user_city.x)
                        y2 = int(system.y) * 1000 + int(user_city.y)
                        z2 = int(system.z) * 1000 + int(user_city.z)
                    else:
                        planet = 0
                        x2 = (user_city.x) * 1000
                        y2 = (user_city.y) * 1000
                        z2 = (user_city.z) * 1000
                    distance = math.sqrt(
                        (trade_element.x - x2) ** 2 + (trade_element.y - y2) ** 2 + (trade_element.z - z2) ** 2)
                    if method == 1:
                        mass_element = trade_element.mass_element
                        mass = amount * mass_element
                        energy = math.sqrt(mass * distance / 20000)
                        trade_building = Building_installed.objects.filter(user=session_user,
                                                                           user_city=session_user_city,
                                                                           production_class=13).first()
                        if trade_building.warehouse >= energy:
                            time = math.sqrt(mass * distance * energy / 10000)
                            start_time = datetime.now()
                            finish_time = start_time + timedelta(seconds=time)

                            trade_teleport = Trade_teleport(
                                user=session_user,
                                user_city=session_user_city,
                                name=trade_element.name,
                                class_element=trade_element.class_element,
                                id_element=trade_element.id_element,
                                amount=amount,
                                start_teleport=start_time,
                                finish_teleport=finish_time
                            )
                            trade_teleport.save()
                            new_amount = trade_element.amount - amount
                            if new_amount == 0:
                                trade_element = Trade_element.objects.filter(id=id_element).delete()
                            else:
                                trade_element = Trade_element.objects.filter(id=id_element).update(amount=new_amount)
                            new_energy = trade_building.warehouse - energy
                            trade_building = Building_installed.objects.filter(user=session_user,
                                                                               user_city=session_user_city,
                                                                               production_class=13).update(
                                warehouse=new_energy)
                        else:
                            message = 'Нехватает энергии'

                    elif method == 2:
                        user_city = User_city.objects.filter(id=session_user_city).first()
                        fleet = Fleet.objects.filter(user=session_user, name='Trade', status=0,
                                                     planet=user_city.planet_id).first()
                        if fleet:
                            id_fleet = fleet.id
                            fleet_empty_hold = fleet.empty_hold * 1.0
                            lot = int(fleet_empty_hold / trade_element.size_element)
                            quantity_goods = amount * trade_element.size_element / fleet_empty_hold
                            number_shipments = int(math.ceil(quantity_goods))
                            lot_amount = amount
                            for i in range(number_shipments):

                                if lot_amount < lot:
                                    lot = lot_amount
                                trade_function.flight_record_sheet_flight(session_user, session_user_city, user_city,
                                                                          id_fleet,
                                                                          trade_element, 0, fleet, 0, distance)
                                trade_function.flight_record_sheet_loading_holds(session_user, session_user_city,
                                                                                 id_fleet,
                                                                                 trade_element, lot)
                                lot_amount = lot_amount - lot
                                trade_function.flight_record_sheet_flight(session_user, session_user_city, user_city,
                                                                          id_fleet,
                                                                          trade_element, lot, fleet, lot_amount,
                                                                          distance)
                                trade_function.flight_record_sheet_unloading_holds(session_user, session_user_city,
                                                                                   user_city, id_fleet,
                                                                                   trade_element, lot)
                            new_amount = trade_element.amount - amount
                            trade_element = Trade_element.objects.filter(id=id_element).update(amount=new_amount)
                            fleet = Fleet.objects.filter(id=id_fleet).update(status=1, planet_status=0, planet=0,
                                                                             system=0)
                            trade_fligth = Trade_flight.objects.filter(id_fleet=id_fleet).first()
                            trade_fligth = Trade_flight.objects.filter(id=trade_fligth.id).update(status=1)
                        else:
                            delivery_queue = Delivery_queue(
                                user=session_user,
                                user_city=session_user_city,
                                name=trade_element.name,
                                class_element=trade_element.class_element,
                                id_element=trade_element.id_element,
                                amount=amount,
                                method=0,
                                status=0,
                                x=trade_element.x,
                                y=trade_element.y,
                                z=trade_element.z,
                                mass_element=trade_element.mass_element,
                                size_element=trade_element.size_element
                            )
                            delivery_queue.save()
                            new_amount = trade_element.amount - amount
                            if new_amount == 0:
                                trade_element = Trade_element.objects.filter(id=id_element).delete()
                            else:
                                trade_element = Trade_element.objects.filter(id=id_element).update(amount=new_amount)
                            message = 'Ваши флота все заняты. Товар поставлено в очередь на доставку'
                    elif method == 3:
                        user_city = User_city.objects.filter(id=session_user_city).first()
                        fleet = Fleet.objects.filter(user=trade_element.user, name='Trade', status=0,
                                                     planet=trade_element.user_city).first()
                        if fleet:
                            id_fleet = fleet.id
                            fleet_empty_hold = fleet.empty_hold * 1.0
                            lot = int(fleet_empty_hold / trade_element.size_element)
                            quantity_goods = amount * trade_element.size_element / fleet_empty_hold
                            number_shipments = int(math.ceil(quantity_goods))
                            lot_amount = amount
                            for i in range(number_shipments):
                                if lot_amount < lot:
                                    lot = lot_amount
                                lot_amount = lot_amount - lot
                                trade_function.flight_record_sheet_loading_holds(session_user, session_user_city,
                                                                                 id_fleet,
                                                                                 trade_element, lot)
                                trade_function.flight_record_sheet_flight(session_user, session_user_city, user_city,
                                                                          id_fleet,
                                                                          trade_element, lot, fleet, lot_amount,
                                                                          distance)
                                trade_function.flight_record_sheet_unloading_holds(session_user, session_user_city,
                                                                                   user_city, id_fleet,
                                                                                   trade_element, lot)
                                trade_function.flight_record_sheet_flight(session_user, session_user_city, user_city,
                                                                          id_fleet,
                                                                          trade_element, 0, fleet, 0, distance)
                            new_amount = trade_element.amount - amount
                            trade_element = Trade_element.objects.filter(id=id_element).update(amount=new_amount)
                            fleet = Fleet.objects.filter(id=id_fleet).update(status=1, planet_status=0, planet=0,
                                                                             system=0)
                            trade_fligth = Trade_flight.objects.filter(id_fleet=id_fleet).first()
                            trade_fligth = Trade_flight.objects.filter(id=trade_fligth.id).update(status=1)
                        else:
                            delivery_queue = Delivery_queue(
                                user=session_user,
                                user_city=session_user_city,
                                name=trade_element.name,
                                class_element=trade_element.class_element,
                                id_element=trade_element.id_element,
                                amount=amount,
                                method=0,
                                status=0,
                                x=trade_element.x,
                                y=trade_element.y,
                                z=trade_element.z,
                                mass_element=trade_element.mass_element,
                                size_element=trade_element.size_element
                            )
                            delivery_queue.save()
                            new_amount = trade_element.amount - amount
                            if new_amount == 0:
                                trade_element = Trade_element.objects.filter(id=id_element).delete()

                            else:
                                trade_element = Trade_element.objects.filter(id=id_element).update(amount=new_amount)
                            message = 'Флота продавца все заняты. Товар поставлено в очередь на доставку'
        else:
            message = 'Неверное количество товара'
        trade_space_id = request.POST.get('trade_space_id')
        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('id_resource')
        basic_resources = Basic_resource.objects.filter()
        user_city = User_city.objects.filter(user=session_user).first()
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
        user_trade_elements = Trade_element.objects.filter(user=session_user)
        trade_building = Building_installed.objects.filter(user=session_user, user_city=session_user_city,
                                                           production_class=13).first()
        delivery_queues = Delivery_queue.objects.filter(user=session_user, user_city=session_user_city)
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
                  'trade_elements': trade_elements, 'users': users, 'user_trade_elements': user_trade_elements,
                  'trade_space': trade_space, 'message': message, 'trade_building': trade_building,
                  'delivery_queues': delivery_queues}
        return render(request, "trade.html", output)