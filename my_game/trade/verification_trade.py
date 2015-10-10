# -*- coding: utf-8 -*-

from django.utils import timezone
from my_game.models import Planet
from my_game.models import UserCity
from my_game.models import FactoryPattern
from my_game.models import WarehouseFactory, WarehouseElement, Warehouse
from my_game.models import Fleet, Hold
from my_game.models import TradeFlight, TradeReleport


def verification_trade(request):
    user = request
    time = timezone.now()
    fleets = Fleet.objects.filter(user=user, name='Trade', status=1)
    for fleet in fleets:
        trade_flights = TradeFlight.objects.filter(id_fleet=fleet.id)
        flightplan_len = len(trade_flights)
        lens = 0
        for trade_flight in trade_flights:
            user_city = UserCity.objects.filter(id=trade_flight.user_city).first()
            if trade_flight.status == 1:
                if trade_flight.id_flight == 1:
                    time_start = trade_flight.start_time
                    delta_time = time - time_start
                    new_delta = delta_time.seconds
                    delta = trade_flight.flight_time
                    if new_delta > delta:
                        x = trade_flight.finish_x
                        y = trade_flight.finish_y
                        z = trade_flight.finish_z
                        fleet_up = Fleet.objects.filter(id=fleet.id).update(x=x, y=y, z=z)
                        trade_flight = TradeFlight.objects.filter(id_fleet=fleet.id).first()
                        trade_flight = TradeFlight.objects.filter(id=trade_flight.id).delete()
                        trade_flight = TradeFlight.objects.filter(id_fleet=fleet.id).first()
                        trade_flight = TradeFlight.objects.filter(id=trade_flight.id).update(status=1)
                elif trade_flight.id_flight == 2:
                    time_start = trade_flight.start_time
                    delta_time = time - time_start
                    new_delta = delta_time.seconds
                    delta = trade_flight.flight_time
                    if new_delta > delta:
                        hold = Hold(
                            fleet_id=trade_flight.id_fleet,
                            class_shipment=trade_flight.class_element,
                            id_shipment=trade_flight.id_element,
                            amount_shipment=trade_flight.amount,
                            mass_shipment=trade_flight.mass,
                            size_shipment=trade_flight.size
                        )
                        hold.save()

                        new_mass = fleet.ship_empty_mass + trade_flight.mass
                        empty_hold = fleet.empty_hold - trade_flight.size
                        fleet_up = Fleet.objects.filter(id=fleet.id).update(empty_hold=empty_hold,
                                                                            ship_empty_mass=new_mass)
                        trade_flight = TradeFlight.objects.filter(id_fleet=fleet.id).first()
                        trade_flight = TradeFlight.objects.filter(id=trade_flight.id).delete()
                        trade_flight = TradeFlight.objects.filter(id_fleet=fleet.id).first()
                        if trade_flight:
                            trade_flight = TradeFlight.objects.filter(id=trade_flight.id).update(status=1)
                        else:
                            planet = Planet.objects.filter(x=fleet.x, y=fleet.y, z=fleet.z).first()
                            if planet:
                                planet_status = 1
                            else:
                                planet_status = 0
                            fleet = Fleet.objects.filter(id=fleet.id).update(planet=user_city.planet_id,
                                                                             system=user_city.system_id, status=0,
                                                                             planet_status=planet_status)

                elif trade_flight.id_flight == 3:
                    time_start = trade_flight.start_time
                    delta_time = time - time_start
                    new_delta = delta_time.seconds
                    delta = trade_flight.flight_time
                    if new_delta > delta:
                        hold = Hold.objects.filter(fleet_id=fleet.id).first()

                        if hold.class_shipment == 0:
                            warehouse = Warehouse.objects.filter(user=user, user_city=trade_flight.user_city,
                                                                 id_resource=trade_flight.id_element).first()
                            new_amount = warehouse.amount + trade_flight.amount
                            warehouse = Warehouse.objects.filter(user=user, user_city=trade_flight.user_city,
                                                                 id_resource=trade_flight.id_element).update(
                                amount=new_amount)

                        elif 0 < hold.class_shipment < 10:
                            warehouse = WarehouseElement.objects.filter(user=user, user_city=trade_flight.user_city,
                                                                         element_class=trade_flight.class_element,
                                                                         element_id=trade_flight.id_element).first()
                            if warehouse:
                                new_amount = warehouse.amount + trade_flight.amount
                                warehouse = WarehouseElement.objects.filter(user=user,
                                                                             user_city=trade_flight.user_city,
                                                                             element_class=trade_flight.class_element,
                                                                             element_id=trade_flight.id_element).update(
                                    amount=new_amount)
                            else:
                                warehouse = WarehouseElement(
                                    user=user,
                                    user_city=trade_flight.user_city,
                                    element_class=trade_flight.class_element,
                                    element_id=trade_flight.id_element,
                                    amount=trade_flight.amount
                                )
                        elif hold.class_shipment > 10:
                            warehouse = WarehouseFactory.objects.filter(user=user, user_city=trade_flight.user_city,
                                                                         production_class__lt=13,
                                                                         factory_id=trade_flight.id_element).first()
                            if warehouse:
                                new_amount = warehouse.amount + trade_flight.amount
                                warehouse = WarehouseFactory.objects.filter(user=user,
                                                                             user_city=trade_flight.user_city,
                                                                             production_class__lt=13,
                                                                             factory_id=trade_flight.id_element).update(
                                    amount=new_amount)
                            else:
                                factory_rattern = FactoryPattern.objects.filter(id=trade_flight.id_element).first()

                                warehouse = WarehouseFactory(
                                    user=user,
                                    user_city=trade_flight.user_city,
                                    factory_id=trade_flight.id_element,
                                    production_class=factory_rattern.production_class,
                                    production_id=factory_rattern.production_id,
                                    time_production=factory_rattern.time_production,
                                    amount=trade_flight.amount,
                                    size=factory_rattern.size,
                                    mass=factory_rattern.mass,
                                    power_consuption=factory_rattern.power_consuption,
                                )

                        hold = Hold.objects.filter(fleet_id=fleet.id).delete()
                        new_mass = fleet.ship_empty_mass - trade_flight.mass
                        empty_hold = fleet.empty_hold + trade_flight.size
                        fleet_up = Fleet.objects.filter(id=fleet.id).update(empty_hold=empty_hold,
                                                                            ship_empty_mass=new_mass)
                        trade_flight = TradeFlight.objects.filter(id_fleet=fleet.id).first()
                        trade_flight = TradeFlight.objects.filter(id=trade_flight.id).delete()
                        trade_flight = TradeFlight.objects.filter(id_fleet=fleet.id).first()
                        if trade_flight:
                            trade_flight = TradeFlight.objects.filter(id=trade_flight.id).update(status=1)
                        else:
                            planet = Planet.objects.filter(x=fleet.x, y=fleet.y, z=fleet.z).first()
                            if planet:
                                planet_status = 1
                            else:
                                planet_status = 0
                            fleet = Fleet.objects.filter(id=fleet.id).update(planet=user_city.planet_id,
                                                                             system=user_city.system_id, status=0,
                                                                             planet_status=planet_status)

    teleports = TradeReleport.objects.filter(user=user)
    for teleport in teleports:
        teleport_id = teleport.id
        time_start = teleport.start_teleport
        delta_time = time - time_start
        new_delta = delta_time.seconds
        delta = teleport.finish_teleport - teleport.start_teleport
        delta = delta.seconds
        if new_delta > delta:

            if teleport.class_element == 0:
                warehouse = Warehouse.objects.filter(user=user, user_city=teleport.user_city,
                                                     id_resource=teleport.id_element).first()
                new_amount = warehouse.amount + teleport.amount
                warehouse = Warehouse.objects.filter(user=user, user_city=teleport.user_city,
                                                     id_resource=teleport.id_element).update(amount=new_amount)

            elif 0 < teleport.class_element < 10:
                warehouse = WarehouseElement.objects.filter(user=user, user_city=teleport.user_city,
                                                             element_class=teleport.class_element,
                                                             element_id=teleport.id_element).first()
                if warehouse:
                    new_amount = warehouse.amount + teleport.amount
                    warehouse = WarehouseElement.objects.filter(user=user, user_city=teleport.user_city,
                                                                 element_class=teleport.class_element,
                                                                 element_id=teleport.id_element).update(
                        amount=new_amount)
                else:
                    warehouse = WarehouseElement(
                        user=user,
                        user_city=teleport.user_city,
                        element_class=teleport.class_element,
                        element_id=teleport.id_element,
                        amount=teleport.amount
                    )
            elif teleport.class_shipment > 10:
                warehouse = WarehouseFactory.objects.filter(user=user, user_city=teleport.user_city,
                                                             production_class__lt=13,
                                                             factory_id=teleport.id_element).first()
                if warehouse:
                    new_amount = warehouse.amount + teleport.amount
                    warehouse = WarehouseFactory.objects.filter(user=user, user_city=teleport.user_city,
                                                                 production_class__lt=13,
                                                                 factory_id=teleport.id_element).update(
                        amount=new_amount)
                else:
                    factory_rattern = FactoryPattern.objects.filter(id=teleport.id_element).first()

                    warehouse = WarehouseFactory(
                        user=user,
                        user_city=teleport.user_city,
                        factory_id=teleport.id_element,
                        production_class=factory_rattern.production_class,
                        production_id=factory_rattern.production_id,
                        time_production=factory_rattern.time_production,
                        amount=teleport.amount,
                        size=factory_rattern.size,
                        mass=factory_rattern.mass,
                        power_consuption=factory_rattern.power_consuption,
                    )
            teleport = TradeReleport.objects.filter(id=teleport_id).delete()