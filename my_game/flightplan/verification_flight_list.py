# -*- coding: utf-8 -*-

from datetime import timedelta
from django.utils import timezone
import math
from my_game.models import Planet, Warehouse, Warehouse_element, Warehouse_factory, Warehouse_ship
from my_game.models import System, Asteroid_field, Flightplan_scan, Fleet_parametr_resource_extraction
from my_game.models import Fleet, Fuel_pattern, Fuel_tank, Armor_pattern, Shield_pattern, Weapon_pattern, \
    Engine_pattern, Generator_pattern, Shell_pattern, Module_pattern, Device_pattern
from my_game.models import Flightplan, Flightplan_flight, Fleet_parametr_scan, Flightplan_production, Flightplan_hold
from my_game.models import Mail, Hold, Ship, Project_ship, Hull_pattern, User_city, Factory_pattern
from my_game.flightplan.start import start_flight, start_colonization, start_extraction, start_refill, \
    start_repair_build, start_scaning, start_unload_hold, start_upload_hold
from my_game.flightplan.veryfication.flight_verification import verification_flight
from my_game.flightplan.veryfication.scan_veryfication import scan_veryfication
from my_game.flightplan.veryfication.extraction_veryficate import extraction_veryfication
from my_game.flightplan import fuel


def verification_flight_list(request):
    user = request
    fleets = Fleet.objects.filter(user=user)
    finish_time = timezone.now()
    for fleet in fleets:
        flightplans = Flightplan.objects.filter(id_fleet=fleet.id)
        flightplan_len = len(flightplans)
        lens = 0
        for flightplan in flightplans:
            flightplan_id = flightplan.id
            if flightplan.status == 1:
                if flightplan.class_command == 1:
                    finish_time = verification_flight(fleet)
                    flightplan = Flightplan.objects.filter(id_fleet=fleet.id, status=0).first()

                elif flightplan.class_command == 2:

                    city = User_city.objects.filter(user=user, x=fleet.x, y=fleet.y, z=fleet.z).first()
                    if city:
                        mass = 0
                        flightplan_hold = Flightplan_hold.objects.filter(id_fleetplan=flightplan_id).first()
                        if flightplan_hold:
                            time = timezone()
                            time_start = flightplan_hold.start_time
                            time_upload = flightplan_hold.time
                            delta_time = time - time_start
                            new_delta = delta_time.seconds

                            if new_delta > time_upload:
                                class_element = flightplan_hold.class_element
                                if flightplan.id_command == 1:
                                    upload_hold_element(fleet, flightplan_hold, city)
                                else:
                                    unload_hold_element(fleet, flightplan, flightplan_hold, city)

                elif flightplan.class_command == 3:
                    finish_time = extraction_veryfication(fleet)
                    flightplan = Flightplan.objects.filter(id_fleet=fleet.id, status=0).first()

                elif flightplan.class_command == 6:
                    finish_time = scan_veryfication(fleet)
                    flightplan = Flightplan.objects.filter(id_fleet=fleet.id, status=0).first()

                if flightplan:
                    if flightplan.class_command == 1:
                        start_flight.start_flight(fleet.id, finish_time)
                    elif flightplan.class_command == 2:
                        if flightplan.id_command == 1:
                            start_upload_hold.start_upload(fleet.id, finish_time)
                        else:
                            start_unload_hold.start_unload(fleet.id, finish_time)
                    elif flightplan.class_command == 3:
                        start_extraction.start_extraction(fleet.id, finish_time)
                    elif flightplan.class_command == 6:
                        start_scaning.start_scaning(fleet.id, finish_time)
                else:
                    fleet_up = Fleet.objects.filter(id=fleet.id).update(status=0)





                    # lens = lens + 1
                    # if lens == flightplan_len:
                    # fleet_up = Fleet.objects.filter(id=fleet.id).update(status=0)
                    # else:
                    # flightplan = Flightplan.objects.filter(id_fleet=fleet.id).first().update(status=1)
                    #
                    # flightplan = Flightplan.objects.filter(id=flightplan_id).delete()


def search_pattern(*args):
    class_element = args[0]
    warehouse = args[1]
    if class_element == 1:
        pattern = Hull_pattern.objects.filter(id=warehouse.id_element).first()
    elif class_element == 2:
        pattern = Armor_pattern.objects.filter(id=warehouse.id_element).first()
    elif class_element == 3:
        pattern = Shield_pattern.objects.filter(id=warehouse.id_element).first()
    elif class_element == 4:
        pattern = Engine_pattern.objects.filter(id=warehouse.id_element).first()
    elif class_element == 5:
        pattern = Generator_pattern.objects.filter(
            id=warehouse.id_element).first()
    elif class_element == 6:
        pattern = Weapon_pattern.objects.filter(id=warehouse.id_element).first()
    elif class_element == 7:
        pattern = Shell_pattern.objects.filter(id=warehouse.id_element).first()
    elif class_element == 8:
        pattern = Module_pattern.objects.filter(id=warehouse.id_element).first()
    elif class_element == 9:
        pattern = Device_pattern.objects.filter(id=warehouse.id_element).first()

        return pattern


def warehouse_update(*args):
    class_element = args[0]
    city = args[1]
    flightplan_hold = args[2]
    new_amount = args[3]
    if class_element == 0:
        warehouse_up = Warehouse.objects.filter(user_city=city.id,
                                                id_resource=flightplan_hold.id_element).update(
            amount=new_amount)
    elif class_element == 10:
        warehouse_up = Warehouse_factory.objects.filter(user_city=city.id,
                                                        id=flightplan_hold.id_element).update(
            amount=new_amount)
    elif class_element == 11:
        warehouse_up = Warehouse_ship.objects.filter(user_city=city.id,
                                                     id=flightplan_hold.id_element).update(
            amount=new_amount)
    else:
        warehouse_up = Warehouse_element.objects.filter(user_city=city.id,
                                                        element_class=class_element,
                                                        element_id=flightplan_hold.id_element).update(
            amount=new_amount)


def new_warehouse_update(*args):
    class_element = args[0]
    city = args[1]
    flightplan_hold = args[2]
    new_amount = args[3]
    if class_element == 0:
        warehouse_up = Warehouse(
            user=city.user,
            user_city=city.id,
            id_resource=flightplan_hold.id_element,
            amount=new_amount
        )
        warehouse_up.save()
    elif class_element == 10:
        factory = Factory_pattern.objects.filter(id=flightplan_hold.id_element).first()
        warehouse_up = Warehouse_factory(
            user=city.user,
            user_city=city.id,
            factory_id=flightplan_hold.id_element,
            production_class=factory.production_class,
            production_id=factory.production_id,
            time_production=factory.time_production,
            amount=new_amount,
            size=factory.size,
            mass=factory.mass,
            power_consumption=factory.power_consumption
        )
        warehouse_up.save()
    elif class_element == 11:
        warehouse_up = Warehouse_ship(
            user=city.user,
            user_city=city.id,
            ship_id=flightplan_hold.id_element,
            amount=new_amount
        )
        warehouse_up.save()
    else:
        warehouse_up = Warehouse_element(
            user=city.user,
            user_city=city.id,
            element_class=flightplan_hold.class_element,
            element_id=flightplan_hold.id_element,
            amount=new_amount
        )
        warehouse_up.save()


def mass_size(*args):
    class_element = args[0]
    city = args[1]
    flightplan_hold = args[2]
    mass = 0
    size = 0
    if class_element == 0:
        warehouse = Warehouse.objects.filter(user_city=city.id,
                                             id_resource=flightplan_hold.id_element).first()
        size = 1
        mass = 1
    elif class_element == 10:
        warehouse = Warehouse_factory.objects.filter(user_city=city.id,
                                                     id=flightplan_hold.id_element).first()
        if warehouse:
            size = warehouse.size
            mass = warehouse.mass
    elif class_element == 11:
        warehouse = Warehouse_ship.objects.filter(user_city=city.id,
                                                  id=flightplan_hold.id_element).first()
        if warehouse:
            ship = Ship.objects.filter(id=warehouse.ship_id).first()
            project_ship = Project_ship.objects.filter(id=ship.id_project_ship).first()
            hull = Hull_pattern.objects.filter(id=project_ship.hull_id).first()
            size = hull.size
            mass = project_ship.mass
    else:
        warehouse = Warehouse_element.objects.filter(user_city=city.id,
                                                     element_class=class_element,
                                                     element_id=flightplan_hold.id_element).first()
        if warehouse:
            pattern = search_pattern(class_element, warehouse)
            if class_element != 2:
                size = pattern.size
            else:
                size = pattern.mass / 4
            mass = pattern.mass
    answer = {warehouse, size, mass}
    return answer


def upload_hold_element(*args):
    fleet = args[0]
    flightplan_hold = args[1]
    class_element = flightplan_hold.class_element
    city = args[2]

    answer = mass_size(class_element, city, flightplan_hold)
    warehouse = answer[0]
    size = answer[1]
    mass = answer[2]

    if warehouse:
        need_amount = flightplan_hold.amount
        if need_amount > warehouse.amount:
            need_amount = warehouse.amount

        need_size = need_amount * size

        hold_size_free = fleet.empty_hold
        if need_size > hold_size_free:
            need_size = hold_size_free
            need_amount = int(need_size / size) - 1

        new_amount = warehouse.amount - need_amount

        warehouse_update(class_element, city, flightplan_hold, new_amount)

        fleet_hold = Hold.objects.filter(fleet_id=fleet.id, class_shipment=class_element,
                                         id_shipment=flightplan_hold.id_element).first()
        if fleet_hold:
            new_amount = fleet_hold.amount_shipment + need_amount
            new_size = fleet_hold.size_shipment + need_size
            new_mass = fleet_hold.mass_shipment + mass * need_amount
            fleet_hold_up = Hold.objects.filter(fleet_id=fleet.id, class_shipment=class_element,
                                                id_shipment=flightplan_hold.id_element).update(
                amount_shipment=new_amount, mass_shipment=new_mass, size_shipment=new_size)
        else:
            hold = Hold(
                fleet_id=fleet.id,
                class_shipment=class_element,
                id_shipment=flightplan_hold.id_element,
                amount_shipment=need_amount,
                mass_shipment=mass * need_amount,
                size_shipment=need_size
            )
            hold.save()

        new_fleet_mass = fleet.ship_empty_mass + mass * need_amount
        new_empty_hold = fleet.empty_hold - need_size
        fleet_up = Fleet.objects.filter(id=fleet.id).update(empty_hold=new_empty_hold, ship_empty_mass=new_fleet_mass)
        message = ''
    else:
        message = 'На складе нет такого модуля'

    return message


def unload_hold_element(*args):
    fleet = args[0]
    flightplan = args[1]
    flightplan_hold = args[2]
    class_element = flightplan_hold.class_element
    city = args[3]

    if flightplan.id_command == 2:
        hold = Hold.objects.filter(fleet_id=fleet.id, class_shipment=flightplan_hold.class_element,
                                   id_shipment=flightplan_hold.id_element).first()
        if hold:
            amount = flightplan_hold.amount
            if hold.amount_shipment < amount:
                amount = hold.amount_shipment

            answer = mass_size(class_element, city, flightplan_hold)
            warehouse = answer[0]
            delete_size = answer[1] * amount
            delete_mass = answer[2] * amount

            if warehouse:
                new_amount = warehouse.amount + amount
                warehouse_update(class_element, city, flightplan_hold, new_amount)
            else:
                new_warehouse_update(class_element, city, flightplan_hold, amount)

            amount = flightplan_hold.amount
            if amount < hold.amount_shipment:
                new_amount = hold.amount_shipment - amount
                hold_up = Hold.objects.filter(fleet_id=fleet.id, class_shipment=flightplan_hold.class_element,
                                              id_shipment=flightplan_hold.id_element).update(amount_shipment=new_amount)
            else:
                hold_delete = hold = Hold.objects.filter(fleet_id=fleet.id,
                                                         class_shipment=flightplan_hold.class_element,
                                                         id_shipment=flightplan_hold.id_element).delete()
            new_fleet_mass = fleet.ship_empty_mass - delete_mass
            new_empty_hold = fleet.empty_hold - delete_size
            fleet_up = Fleet.objects.filter(id=fleet.id).update(empty_hold=new_empty_hold,
                                                                ship_empty_mass=new_fleet_mass)
        else:
            message = 'В трюме нет такого модуля'

    elif flightplan.id_command == 3:
        hold = Hold.objects.filter(fleet_id=fleet.id, class_shipment=flightplan_hold.class_element,
                                   id_shipment=flightplan_hold.id_element).first()
        if hold:
            amount = hold.amount_shipment



    elif flightplan.id_command == 4:
        t = 1


        #   3. выгрузка всех елементов из трюма. ИД команды 3
        #   4. разгрузка всего трюма. ИД команды 4
        #   5. перерасчет трюма, веса корабля
        #   6. перерасчет склада
