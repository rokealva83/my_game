# -*- coding: utf-8 -*-

from django.shortcuts import render
from datetime import datetime, timedelta
import math
from my_game.models import MyUser, UserCity, Planet
from my_game import function
from my_game.trade import trade_function
from my_game.models import Fleet
from my_game.models import TradeElement, DeliveryQueue, BuildingInstalled, TradeFlight, TradeTeleport
from my_game.trade.create_trade_output import create_trade_output


def buy_trade(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        function.check_all_queues(session_user)
        message = ''
        price_element = 0
        new_price = 0
        full_request = request.POST
        my_dictionary = dict(full_request.iterlists())
        trade_space_id = int(my_dictionary.get('trade_space_id')[0])
        id_element = my_dictionary.get('trade_buy')
        id_element = int(id_element[0])
        amount = my_dictionary.get('amount')
        amount = int(amount[0])
        set_aside = my_dictionary.get('set_aside')
        method = my_dictionary.get('method')
        method = int(method[0])
        if amount > 0:
            trade_element = TradeElement.objects.filter(id=id_element).first()
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
                MyUser.objects.filter(user_id=session_user).update(foreigh_currency=new_foreigh_currency)
                seller = MyUser.objects.filter(user_id=trade_element.user).first()
                foreigh_currency = seller.foreigh_currency
                new_foreigh_currency = foreigh_currency + price_element
                MyUser.objects.filter(user_id=trade_element.user).update(foreigh_currency=new_foreigh_currency)
                TradeElement.objects.filter(id=id_element).update(cost=new_price)
                trade_element = TradeElement.objects.filter(id=id_element).first()
                if set_aside:
                    delivery_queue = DeliveryQueue(
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
                        TradeElement.objects.filter(id=id_element).delete()
                    else:
                        TradeElement.objects.filter(id=id_element).update(amount=new_amount)
                    message = 'Товар поставлено в очередь на доставку'
                else:
                    user_city = UserCity.objects.filter(id=session_user_city).first()
                    distance = math.sqrt(
                        (trade_element.x - user_city.x) ** 2 + (trade_element.y - user_city.y) ** 2 + (
                            trade_element.z - user_city.z) ** 2)
                    if method == 1:
                        mass_element = trade_element.mass_element
                        mass = amount * mass_element
                        energy = math.sqrt(mass * distance / 20000)
                        trade_building = BuildingInstalled.objects.filter(user=session_user,
                                                                          user_city=session_user_city,
                                                                          production_class=21).first()
                        if trade_building.warehouse >= energy:
                            time = math.sqrt(mass * distance * energy / 10000)
                            start_time = datetime.now()
                            finish_time = start_time + timedelta(seconds=time)

                            trade_teleport = TradeTeleport(
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
                                TradeElement.objects.filter(id=id_element).delete()
                            else:
                                TradeElement.objects.filter(id=id_element).update(amount=new_amount)
                            new_energy = trade_building.warehouse - energy
                            BuildingInstalled.objects.filter(user=session_user,
                                                             user_city=session_user_city,
                                                             production_class=21).update(
                                warehouse=new_energy)
                        else:
                            message = 'Нехватает энергии'

                    elif method == 2:
                        user_city = UserCity.objects.filter(id=session_user_city).first()
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
                            TradeElement.objects.filter(id=id_element).update(amount=new_amount)
                            Fleet.objects.filter(id=id_fleet).update(status=1, planet_status=0, planet=0,
                                                                     system=0)
                            trade_fligth = TradeFlight.objects.filter(id_fleet=id_fleet).first()
                            TradeFlight.objects.filter(id=trade_fligth.id).update(status=1)
                        else:
                            delivery_queue = DeliveryQueue(
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
                                TradeElement.objects.filter(id=id_element).delete()
                            else:
                                TradeElement.objects.filter(id=id_element).update(amount=new_amount)
                            message = 'Ваши флота все заняты. Товар поставлено в очередь на доставку'
                    elif method == 3:
                        user_city = UserCity.objects.filter(id=session_user_city).first()
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
                            TradeElement.objects.filter(id=id_element).update(amount=new_amount)
                            Fleet.objects.filter(id=id_fleet).update(status=1, planet_status=0, planet=0,
                                                                     system=0)
                            trade_fligth = TradeFlight.objects.filter(id_fleet=id_fleet).first()
                            TradeFlight.objects.filter(id=trade_fligth.id).update(status=1)
                        else:
                            delivery_queue = DeliveryQueue(
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
                                TradeElement.objects.filter(id=id_element).delete()

                            else:
                                TradeElement.objects.filter(id=id_element).update(amount=new_amount)
                            message = 'Флота продавца все заняты. Товар поставлено в очередь на доставку'
        else:
            message = 'Неверное количество товара'
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = create_trade_output(session_user, session_user_city, trade_space_id, message)
        return render(request, "trade.html", output)
