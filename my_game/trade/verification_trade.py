# -*- coding: utf-8 -*-

from django.utils import timezone
from my_game.models import Planet
from my_game.models import UserCity
from my_game.models import FactoryPattern
from my_game.models import WarehouseFactory, WarehouseElement, Warehouse
from my_game.models import Fleet, Hold
from my_game.models import TradeFlight, TradeTeleport


def verification_trade(request):
    user = request
    time = timezone.now()
    fleets = Fleet.objects.filter(user=user, name='Trade', status=1)
    for fleet in fleets:
        trade_flights = TradeFlight.objects.filter(fleet=fleet)
        flightplan_len = len(trade_flights)
        lens = 0
        for trade_flight in trade_flights:
            user_city = UserCity.objects.filter(id=trade_flight.user_city.id).first()
            if trade_flight.status == 1:
                if trade_flight.flightplan == 1:
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
                elif trade_flight.flightplan == 2:
                    time_start = trade_flight.start_time
                    delta_time = time - time_start
                    new_delta = delta_time.seconds
                    delta = trade_flight.flight_time
                    if new_delta > delta:
                        hold = Hold(
                            fleet=trade_flight.fleet,
                            class_shipment=trade_flight.class_element,
                            shipment_id=trade_flight.element_id,
                            amount_shipment=trade_flight.amount,
                            mass_shipment=trade_flight.mass,
                            size_shipment=trade_flight.size
                        )
                        hold.save()

                        new_mass = fleet.ship_empty_mass + trade_flight.mass
                        empty_hold = fleet.empty_hold - trade_flight.size
                        fleet_up = Fleet.objects.filter(id=fleet.id).update(empty_hold=empty_hold,
                                                                            ship_empty_mass=new_mass)
                        trade_flight = TradeFlight.objects.filter(fleet=fleet).first()
                        trade_flight = TradeFlight.objects.filter(id=trade_flight.id).delete()
                        trade_flight = TradeFlight.objects.filter(fleet=fleet).first()
                        if trade_flight:
                            trade_flight = TradeFlight.objects.filter(id=trade_flight.id).update(status=1)
                        else:
                            planet = Planet.objects.filter(x=fleet.x, y=fleet.y, z=fleet.z).first()
                            if planet:
                                planet_status = 1
                            else:
                                planet_status = 0
                            fleet_update = Fleet.objects.filter(id=fleet.id).update(planet=user_city.planet,
                                                                             system=user_city.system, status=0,
                                                                             planet_status=planet_status)

                elif trade_flight.flightplan == 3:
                    time_start = trade_flight.start_time
                    delta_time = time - time_start
                    new_delta = delta_time.seconds
                    delta = trade_flight.flight_time
                    if new_delta > delta:
                        hold = Hold.objects.filter(fleet_id=fleet.id).first()

                        if hold.class_shipment == 0:
                            warehouse = Warehouse.objects.filter(user=user, user_city=trade_flight.user_city,
                                                                 resource_id=trade_flight.element_id).first()
                            new_amount = warehouse.amount + trade_flight.amount
                            warehouse = Warehouse.objects.filter(user=user, user_city=trade_flight.user_city,
                                                                 resource_id=trade_flight.element_id).update(
                                amount=new_amount)

                        elif 0 < hold.class_shipment < 10:
                            warehouse = WarehouseElement.objects.filter(user=user, user_city=trade_flight.user_city,
                                                                         element_class=trade_flight.class_element,
                                                                         element_id=trade_flight.element_id).first()
                            if warehouse:
                                new_amount = warehouse.amount + trade_flight.amount
                                warehouse = WarehouseElement.objects.filter(user=user,
                                                                             user_city=trade_flight.user_city,
                                                                             element_class=trade_flight.class_element,
                                                                             element_id=trade_flight.element_id).update(
                                    amount=new_amount)
                            else:
                                warehouse = WarehouseElement(
                                    user=user,
                                    user_city=trade_flight.user_city,
                                    element_class=trade_flight.class_element,
                                    element_id=trade_flight.element_id,
                                    amount=trade_flight.amount
                                )
                        elif hold.class_shipment > 10:
                            warehouse = WarehouseFactory.objects.filter(user=user, user_city=trade_flight.user_city,
                                                                         production_class__lt=13,
                                                                         factory_id=trade_flight.element_id).first()
                            if warehouse:
                                new_amount = warehouse.amount + trade_flight.amount
                                warehouse = WarehouseFactory.objects.filter(user=user,
                                                                             user_city=trade_flight.user_city,
                                                                             production_class__lt=13,
                                                                             factory_id=trade_flight.element_id).update(
                                    amount=new_amount)
                            else:
                                factory_pattern = FactoryPattern.objects.filter(id=trade_flight.element_id).first()

                                warehouse = WarehouseFactory(
                                    user=user,
                                    user_city=trade_flight.user_city,
                                    factory=trade_flight.element_id,
                                    amount=trade_flight.amount,
                                )

                        hold = Hold.objects.filter(fleet=fleet).delete()
                        new_mass = fleet.ship_empty_mass - trade_flight.mass
                        empty_hold = fleet.empty_hold + trade_flight.size
                        fleet_up = Fleet.objects.filter(id=fleet.id).update(empty_hold=empty_hold,
                                                                            ship_empty_mass=new_mass)
                        trade_flight = TradeFlight.objects.filter(fleet=fleet).first()
                        trade_flight = TradeFlight.objects.filter(id=trade_flight.id).delete()
                        trade_flight = TradeFlight.objects.filter(fleet=fleet).first()
                        if trade_flight:
                            trade_flight = TradeFlight.objects.filter(id=trade_flight.id).update(status=1)
                        else:
                            planet = Planet.objects.filter(x=fleet.x, y=fleet.y, z=fleet.z).first()
                            if planet:
                                planet_status = 1
                            else:
                                planet_status = 0
                            fleet_update = Fleet.objects.filter(id=fleet.id).update(planet=user_city.planet,
                                                                             system=user_city.system, status=0,
                                                                             planet_status=planet_status)

    teleports = TradeTeleport.objects.filter(user=user)
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
                                                     resource_id=teleport.element_id).first()
                new_amount = warehouse.amount + teleport.amount
                warehouse = Warehouse.objects.filter(user=user, user_city=teleport.user_city,
                                                     resource_id=teleport.element_id).update(amount=new_amount)

            elif 0 < teleport.class_element < 10:
                warehouse = WarehouseElement.objects.filter(user=user, user_city=teleport.user_city,
                                                             element_class=teleport.class_element,
                                                             element_id=teleport.element_id).first()
                if warehouse:
                    new_amount = warehouse.amount + teleport.amount
                    warehouse = WarehouseElement.objects.filter(user=user, user_city=teleport.user_city,
                                                                 element_class=teleport.class_element,
                                                                 element_id=teleport.element_id).update(
                        amount=new_amount)
                else:
                    warehouse = WarehouseElement(
                        user=user,
                        user_city=teleport.user_city,
                        element_class=teleport.class_element,
                        element_id=teleport.element_id,
                        amount=teleport.amount
                    )
            elif teleport.class_shipment > 10:
                warehouse = WarehouseFactory.objects.filter(user=user, user_city=teleport.user_city,
                                                             production_class__lt=13,
                                                             factory_id=teleport.element_id).first()
                if warehouse:
                    new_amount = warehouse.amount + teleport.amount
                    warehouse = WarehouseFactory.objects.filter(user=user, user_city=teleport.user_city,
                                                                 production_class__lt=13,
                                                                 factory=teleport.element_id).update(
                        amount=new_amount)
                else:
                    factory_pattern = FactoryPattern.objects.filter(id=teleport.element_id).first()

                    warehouse = WarehouseFactory(
                        user=user,
                        user_city=teleport.user_city,
                        factory_id=teleport.element_id,
                        production_class=factory_pattern.production_class,
                        production_id=factory_pattern.production_id,
                        time_production=factory_pattern.time_production,
                        amount=teleport.amount,
                        size=factory_pattern.size,
                        mass=factory_pattern.mass,
                        power_consuption=factory_pattern.power_consuption,
                    )
            teleport = TradeTeleport.objects.filter(id=teleport_id).delete()