# -*- coding: utf-8 -*-


from django.shortcuts import render
from datetime import datetime, timedelta
import math
from my_game.models import MyUser, User_city, Warehouse, Basic_resource, Planet, System
from my_game.models import Hull_pattern, Shield_pattern, Generator_pattern, Engine_pattern, \
    Armor_pattern, Module_pattern, Weapon_pattern, Shell_pattern, Factory_pattern
from my_game.models import Warehouse_element, Warehouse_factory
from my_game import function
from my_game.trade import trade_function
from my_game.models import Project_ship, Ship, Fleet
from my_game.models import Trade_space, Delivery_queue, Building_installed, Trade_teleport, Trade_element, Trade_flight


def delivery(request):
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
        method = myDict.get('method')
        method = int(method[0])
        id_element = myDict.get('deliver')
        id_element = int(id_element[0])
        delivery_element = Delivery_queue.objects.filter(id=id_element).first()
        amount = delivery_element.amount
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
            (delivery_element.x - x2) ** 2 + (delivery_element.y - y2) ** 2 + (delivery_element.z - z2) ** 2)

        if method == 1:
            mass_element = delivery_element.mass_element
            mass = amount * mass_element
            energy = math.sqrt(mass * distance / 20000)
            trade_building = Building_installed.objects.filter(user=session_user, user_city=session_user_city,
                                                               production_class=13).first()
            if trade_building.warehouse >= energy:
                time = math.sqrt(mass * distance * energy / 10000)
                start_time = datetime.now()
                finish_time = start_time + timedelta(seconds=time)
                trade_teleport = Trade_teleport(
                    user=session_user,
                    user_city=session_user_city,
                    name=delivery_element.name,
                    class_element=delivery_element.class_element,
                    id_element=delivery_element.id_element,
                    amount=amount,
                    start_teleport=start_time,
                    finish_teleport=finish_time
                )
                trade_teleport.save()
                delivery_element = Delivery_queue.objects.filter(id=id_element).delete()
                new_energy = trade_building.warehouse - energy
                trade_building = Building_installed.objects.filter(user=session_user, user_city=session_user_city,
                                                                   production_class=13).update(warehouse=new_energy)
            else:
                message = 'Нехватает энергии'
            time = mass * energy / 20000 * distance
        elif method == 2:
            user_city = User_city.objects.filter(id=session_user_city).first()
            fleet = Fleet.objects.filter(user=session_user, name='Trade', status=0,
                                         planet=user_city.planet_id).first()
            if fleet:
                id_fleet = fleet.id

                fleet_empty_hold = fleet.empty_hold * 1.0
                lot = int(fleet_empty_hold / delivery_element.size_element)
                quantity_goods = amount * delivery_element.size_element / fleet_empty_hold
                number_shipments = int(math.ceil(quantity_goods))
                lot_amount = amount

                for i in range(number_shipments):

                    if lot_amount < lot:
                        lot = lot_amount

                    trade_function.flight_record_sheet_flight(session_user, session_user_city, user_city, id_fleet,
                                                              delivery_element, 0, fleet, 0, distance)

                    trade_function.flight_record_sheet_loading_holds(session_user, session_user_city, id_fleet,
                                                                     delivery_element, lot)

                    lot_amount = lot_amount - lot

                    trade_function.flight_record_sheet_flight(session_user, session_user_city, user_city, id_fleet,
                                                              delivery_element, lot, fleet, lot_amount, distance)

                    trade_function.flight_record_sheet_unloading_holds(session_user, session_user_city, user_city,
                                                                       id_fleet,
                                                                       delivery_element, lot)
                new_amount = delivery_element.amount - amount
                if new_amount == 0:
                    delivery_element = Delivery_queue.objects.filter(id=id_element).delete()
                else:
                    delivery_element = Delivery_queue.objects.filter(id=id_element).update(amount=new_amount)
                fleet = Fleet.objects.filter(id=id_fleet).update(status=1, planet_status=0, planet=0, system=0)
                trade_fligth = Trade_flight.objects.filter(id_fleet=id_fleet).first()
                trade_fligth = Trade_flight.objects.filter(id=trade_fligth.id).update(status=1)

            else:
                message = 'Ваши флота все заняты.'
        elif method == 3:
            user_city = User_city.objects.filter(id=session_user_city).first()
            fleet = Fleet.objects.filter(user=delivery_element.user, name='Trade', status=0,
                                         planet=delivery_element.user_city).first()
            if fleet:
                id_fleet = fleet.id

                fleet_empty_hold = fleet.empty_hold * 1.0
                lot = int(fleet_empty_hold / delivery_element.size_element)
                quantity_goods = amount * delivery_element.size_element / fleet_empty_hold
                number_shipments = int(math.ceil(quantity_goods))
                lot_amount = amount

                for i in range(number_shipments):

                    if lot_amount < lot:
                        lot = lot_amount

                    lot_amount = lot_amount - lot

                    trade_function.flight_record_sheet_loading_holds(session_user, session_user_city, id_fleet,
                                                                     delivery_element, lot)

                    trade_function.flight_record_sheet_flight(session_user, session_user_city, user_city, id_fleet,
                                                              delivery_element, lot, fleet, lot_amount, distance)

                    trade_function.flight_record_sheet_unloading_holds(session_user, session_user_city, user_city,
                                                                       id_fleet,
                                                                       delivery_element, lot)

                    trade_function.flight_record_sheet_flight(session_user, session_user_city, user_city, id_fleet,
                                                              delivery_element, 0, fleet, 0, distance)
                new_amount = delivery_element.amount - amount
                delivery_element = Delivery_queue.objects.filter(id=id_element).update(amount=new_amount)
                fleet = Fleet.objects.filter(id=id_fleet).update(status=1, planet_status=0, planet=0, system=0)
                trade_fligth = Trade_flight.objects.filter(id_fleet=id_fleet).first()
                trade_fligth = Trade_flight.objects.filter(id=trade_fligth.id).update(status=1)

            else:
                message = 'Флота продавца все заняты.'
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
                  'module_patterns': module_patterns, 'trade_spaces': trade_spaces, 'trade_space_id': trade_space_id,
                  'project_ships': project_ships, 'ships': ships, 'trade_elements': trade_elements, 'users': users,
                  'user_trade_elements': user_trade_elements, 'trade_space': trade_space, 'message': message,
                  'trade_building': trade_building, 'delivery_queues': delivery_queues}
        return render(request, "trade.html", output)
