# -*- coding: utf-8 -*-

from django.shortcuts import render
from datetime import datetime, timedelta
import math
from my_game.models import MyUser, UserCity
from my_game import function
from my_game.trade import trade_function
from my_game.models import Fleet
from my_game.models import DeliveryQueue, BuildingInstalled, TradeTeleport, TradeFlight
from my_game.trade.create_trade_output import create_trade_output


def delivery(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        function.check_all_queues(session_user)
        message = ''

        full_request = request.POST
        my_dictionary = dict(full_request.iterlists())

        trade_space_id = my_dictionary.get('trade_space_id')
        trade_space_id = int(trade_space_id[0])
        method = my_dictionary.get('method')
        method = int(method[0])
        id_element = my_dictionary.get('deliver')
        id_element = int(id_element[0])
        delivery_element = DeliveryQueue.objects.filter(id=id_element).first()
        amount = delivery_element.amount
        user_city = UserCity.objects.filter(id=session_user_city).first()
        distance = math.sqrt(
            (delivery_element.x - user_city.x) ** 2 + (delivery_element.y - user_city.y) ** 2 + (
                delivery_element.z - user_city.z) ** 2)

        if method == 1:
            mass_element = delivery_element.mass_element
            mass = amount * mass_element
            energy = math.sqrt(mass * distance / 20000)
            trade_building = BuildingInstalled.objects.filter(user=session_user, user_city=session_user_city,
                                                              production_class=21).first()
            if trade_building.warehouse >= energy:
                time = math.sqrt(mass * distance * energy / 10000)
                start_time = datetime.now()
                finish_time = start_time + timedelta(seconds=time)
                trade_teleport = TradeTeleport(
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
                DeliveryQueue.objects.filter(id=id_element).delete()
                new_energy = trade_building.warehouse - energy
                BuildingInstalled.objects.filter(user=session_user, user_city=session_user_city,
                                                 production_class=21).update(warehouse=new_energy)
            else:
                message = 'Нехватает энергии'
        elif method == 2:
            user_city = UserCity.objects.filter(id=session_user_city).first()
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
                    DeliveryQueue.objects.filter(id=id_element).delete()
                else:
                    DeliveryQueue.objects.filter(id=id_element).update(amount=new_amount)
                Fleet.objects.filter(id=id_fleet).update(status=1, planet_status=0, planet=0, system=0)
                trade_fligth = TradeFlight.objects.filter(id_fleet=id_fleet).first()
                TradeFlight.objects.filter(id=trade_fligth.id).update(status=1)

            else:
                message = 'Ваши флота все заняты.'
        elif method == 3:
            user_city = UserCity.objects.filter(id=session_user_city).first()
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
                DeliveryQueue.objects.filter(id=id_element).update(amount=new_amount)
                Fleet.objects.filter(id=id_fleet).update(status=1, planet_status=0, planet=0, system=0)
                trade_fligth = TradeFlight.objects.filter(id_fleet=id_fleet).first()
                TradeFlight.objects.filter(id=trade_fligth.id).update(status=1)

            else:
                message = 'Флота продавца все заняты.'
        request.session['user'] = session_user.id
        request.session['user_city'] = session_user_city.id
        request.session['live'] = True

        output = create_trade_output(session_user, session_user_city, output, trade_space_id, message)
        return render(request, "trade.html", output)
