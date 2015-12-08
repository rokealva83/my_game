# -*- coding: utf-8 -*-


from django.shortcuts import render
from my_game.models import MyUser, UserCity, Warehouse
from my_game.models import FactoryPattern
from my_game.models import WarehouseElement, WarehouseFactory
from my_game import function
from my_game.models import ProjectShip, Ship
from my_game.models import TradeElement
from my_game.trade.create_trade_output import create_trade_output


def del_trade(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        function.check_all_queues(session_user)

        full_request = request.POST
        my_dictionary = dict(full_request.iterlists())
        trade_space_id = my_dictionary.get('trade_space_id')
        trade_space_id = int(trade_space_id[0])
        id_element = my_dictionary.get('trade_del')
        id_element = int(id_element[0])

        trade_element = TradeElement.objects.filter(id=id_element).first()
        if trade_element.user_city != session_user_city:
            message = 'Ставка из другого поселения'
        else:
            if trade_element.class_element == 0:
                warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city,
                                                     id_resource=trade_element.id_element).first()

                new_amount = warehouse.amount + trade_element.amount
                Warehouse.objects.filter(user=session_user, user_city=session_user_city,
                                         id_resource=trade_element.id_element).update(amount=new_amount)

            elif 0 < trade_element.class_element < 10:
                warehouse_element = WarehouseElement.objects.filter(user=session_user, user_city=session_user_city,
                                                                    element_class=trade_element.class_element,
                                                                    element_id=trade_element.id_element).first()
                if warehouse_element:
                    new_amount = warehouse_element.amount + trade_element.amount
                    WarehouseElement.objects.filter(user=session_user, user_city=session_user_city,
                                                    element_class=trade_element.class_element,
                                                    element_id=trade_element.id_element).update(amount=new_amount)
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
                    WarehouseFactory.objects.filter(user=session_user, user_city=session_user_city,
                                                    factory_id=trade_element.id_element).update(amount=new_amount)
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
                    Ship.objects.filter(user=session_user, place_id=session_user_city, id_ship_project=id_element,
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
            TradeElement.objects.filter(id=id_element).delete()

        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = create_trade_output(session_user, session_user_city, output, trade_space_id, message)
        return render(request, "trade.html", output)
