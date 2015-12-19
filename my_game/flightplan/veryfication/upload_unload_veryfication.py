# -*- coding: utf-8 -*-

from datetime import timedelta
from django.utils import timezone
from my_game.models import Warehouse, WarehouseElement, WarehouseFactory, WarehouseShip
from my_game.models import Fleet, ArmorPattern, ShieldPattern, WeaponPattern, \
    EnginePattern, GeneratorPattern, ShellPattern, ModulePattern, DevicePattern
from my_game.models import Flightplan, FlightplanHold
from my_game.models import Hold, Ship, ProjectShip, HullPattern, UserCity, FactoryPattern
from my_game.flightplan.fuel import need_fuel_process, minus_fuel


def upload_unload_veryfication(*args):
    fleet = args[0]
    user = fleet.user
    flightplan = Flightplan.objects.filter(id_fleet=fleet.id).first()
    city = UserCity.objects.filter(user=user, x=fleet.x, y=fleet.y, z=fleet.z).first()
    finish_time = timezone.now()
    if city:
        mass = 0
        flightplan_hold = FlightplanHold.objects.filter(id_fleetplan=flightplan.id).first()
        if flightplan_hold:
            time = timezone.now()
            time_start = flightplan_hold.start_time
            time_upload = flightplan_hold.time
            delta_time = time - time_start
            new_delta = delta_time.total_seconds()

            if new_delta > time_upload:
                finish_time = time_start + timedelta(seconds=time_upload)
                class_element = flightplan_hold.class_element
                if flightplan.id_command == 1:
                    upload_hold_element(fleet, flightplan_hold, city)
                else:
                    unload_hold_element(fleet, flightplan, flightplan_hold, city)

                ship_in_fleets = Ship.objects.filter(fleet_status=1, place_id=fleet.id)
                need_fuel = need_fuel_process(ship_in_fleets, flightplan, time_upload, fleet.id)
                minus_fuel(fleet, need_fuel)

                flightplan_del= Flightplan.objects.filter(id=flightplan.id).delete()
                flightplan_hold_del = FlightplanHold.objects.filter(id=flightplan_hold.id).delete()

    return finish_time


def search_pattern(*args):
    class_element = args[0]
    warehouse = args[1]
    if class_element == 1:
        pattern = HullPattern.objects.filter(id=warehouse.id_element).first()
    elif class_element == 2:
        pattern = ArmorPattern.objects.filter(id=warehouse.id_element).first()
    elif class_element == 3:
        pattern = ShieldPattern.objects.filter(id=warehouse.id_element).first()
    elif class_element == 4:
        pattern = EnginePattern.objects.filter(id=warehouse.id_element).first()
    elif class_element == 5:
        pattern = GeneratorPattern.objects.filter(id=warehouse.id_element).first()
    elif class_element == 6:
        pattern = WeaponPattern.objects.filter(id=warehouse.id_element).first()
    elif class_element == 7:
        pattern = ShellPattern.objects.filter(id=warehouse.id_element).first()
    elif class_element == 8:
        pattern = ModulePattern.objects.filter(id=warehouse.id_element).first()
    elif class_element == 9:
        pattern = DevicePattern.objects.filter(id=warehouse.id_element).first()

        return pattern


def warehouse_update(*args):
    class_element = args[0]
    city = args[1]
    flightplan_hold = args[2]
    new_amount = args[3]
    if class_element == 0:
        warehouse_up = Warehouse.objects.filter(user_city=city.id, id_resource=flightplan_hold.id_element).update(
            amount=new_amount)
    elif class_element == 10:
        warehouse_up = WarehouseFactory.objects.filter(user_city=city.id, id=flightplan_hold.id_element).update(
            amount=new_amount)
    elif class_element == 11:
        warehouse_up = WarehouseShip.objects.filter(user_city=city.id, id=flightplan_hold.id_element).update(
            amount=new_amount)
    else:
        warehouse_up = WarehouseElement.objects.filter(user_city=city.id, element_class=class_element,
                                                        element_id=flightplan_hold.id_element).update(amount=new_amount)


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
        factory = FactoryPattern.objects.filter(id=flightplan_hold.id_element).first()
        warehouse_up = WarehouseFactory(
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
        warehouse_up = WarehouseShip(
            user=city.user,
            user_city=city.id,
            ship_id=flightplan_hold.id_element,
            amount=new_amount
        )
        warehouse_up.save()
    else:
        warehouse_up = WarehouseElement(
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
        warehouse = Warehouse.objects.filter(user_city=city.id, id_resource=flightplan_hold.id_element).first()
        size = 1
        mass = 1
    elif class_element == 10:
        warehouse = WarehouseFactory.objects.filter(user_city=city.id, id=flightplan_hold.id_element).first()
        if warehouse:
            size = warehouse.size
            mass = warehouse.mass
    elif class_element == 11:
        warehouse = WarehouseShip.objects.filter(user_city=city.id, id=flightplan_hold.id_element).first()
        if warehouse:
            ship = Ship.objects.filter(id=warehouse.ship_id).first()
            project_ship = ProjectShip.objects.filter(id=ship.id_project_ship).first()
            hull = HullPattern.objects.filter(id=project_ship.hull_id).first()
            size = hull.size
            mass = project_ship.mass
    else:
        warehouse = WarehouseElement.objects.filter(user_city=city.id, element_class=class_element,
                                                     element_id=flightplan_hold.id_element).first()
        if warehouse:
            pattern = search_pattern(class_element, warehouse)
            if class_element != 2:
                size = pattern.size
            else:
                size = pattern.mass / 4
            mass = pattern.mass
    answer = [warehouse, size, mass]
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
    city = args[3]

    if flightplan.id_command == 2:
        hold = Hold.objects.filter(fleet_id=fleet.id, class_shipment=flightplan_hold.class_element,
                                   id_shipment=flightplan_hold.id_element).first()
        if hold:
            hold_unload(fleet, flightplan, flightplan_hold, city, hold)
        else:
            message = 'В трюме нет такого модуля'
    elif flightplan.id_command == 3:
        hold = Hold.objects.filter(fleet_id=fleet.id, class_shipment=flightplan_hold.class_element,
                                   id_shipment=flightplan_hold.id_element).first()
        if hold:
            hold_unload(fleet, flightplan, flightplan_hold, city, hold)
        else:
            message = 'В трюме нет такого модуля'
    elif flightplan.id_command == 4:
        holds = Hold.objects.filter(fleet_id=fleet.id)
        for hold in holds:
            hold_unload(fleet, flightplan, flightplan_hold, city, hold)


def hold_unload(*args):
    fleet = args[0]
    flightplan = args[1]
    flightplan_hold = args[2]
    class_element = flightplan_hold.class_element
    city = args[3]
    hold = args[4]
    if flightplan.id_command == 2:
        amount = flightplan_hold.amount
        if hold.amount_shipment < amount:
            amount = hold.amount_shipment
    else:
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

    if flightplan.id_command == 3:
        hold_delete = hold = Hold.objects.filter(fleet_id=fleet.id, class_shipment=flightplan_hold.class_element,
                                                 id_shipment=flightplan_hold.id_element).delete()
    elif flightplan.id_command == 2:
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
    fleet_up = Fleet.objects.filter(id=fleet.id).update(empty_hold=new_empty_hold, ship_empty_mass=new_fleet_mass)