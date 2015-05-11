# -*- coding: utf-8 -*-


from datetime import datetime
from my_game.models import User_city
from my_game.models import Fleet
from my_game.models import Flightplan, Warehouse_element, Flightplan_refill, Hold


def start_refill(*args):
    session_user = args[0]
    fleet_id = args[1]
    flightplan = Flightplan.objects.filter(id_fleet=fleet_id).first()
    id_flightplan = flightplan.pk
    flightplan_refill = Flightplan_refill.objects.filter(id_fleet=fleet_id).first()
    id_command = flightplan_refill.id_command
    fleet = Fleet.objects.filter(id=fleet_id).first()
    error = 0
    start_time = 0

    # Проверка наличия необходимого количества товара. Проверка наличия места.

    if id_command == 1:
        user_city = User_city.objects.filter(user=session_user, x=fleet.x, y=fleet.y, z=fleet.z).first()
        free_fuel_tank = fleet.free_fuel_tank

        if user_city:
            fuel = Warehouse_element.objects.filter(user_city=user_city.id, element_class=14,
                                                    element_id=flightplan_refill.id_element).first()
            if fuel is None:
                message = 'Нет топлива на складе'
                error = 1
        else:
            fuel = Hold.objects.filter(fleet_id=fleet_id, class_shipment=14,
                                       id_shipment=flightplan_refill.id_element).first()
            if fuel is None:
                message = 'Нет топлива в трюме флота'
                error = 1

    elif id_command == 2:
        fleet_refill = Fleet.objects.filter(id=flightplan_refill.id_fleet_refill).first()
        if fleet_refill.x != fleet.x or fleet_refill.y != fleet.y or fleet_refill.z != fleet.z:
            message = 'Нет флота для заправки на координатах'
            error = 1
        else:
            fuel = Hold.objects.filter(fleet_id=fleet_id, class_shipment=14,
                                       id_shipment=flightplan_refill.id_element).first()
            if fuel is None:
                message = 'Нет топлива в трюме флота'
                error = 1

    elif id_command == 3:
        fleet_refill = Fleet.objects.filter(id=flightplan_refill.id_fleet_refill).first()
        if fleet_refill.x != fleet.x or fleet_refill.y != fleet.y or fleet_refill.z != fleet.z:
            message = 'Нет флота для перегрузки товара'
            error = 1
        else:
            element = Hold.objects.filter(fleet_id=fleet_id, class_shipment=flightplan_refill.class_element,
                                          id_shipment=flightplan_refill.id_element).first()
            if element is None:
                message = 'Нет товара в трюме флота'
                error = 1

    if len(args) == 1:
        start_time = datetime.now()

    if error == 0:
        flightplan_refill = Flightplan_refill.objects.filter(id_fleet=fleet_id).first()
        flightplan_refill = Flightplan_refill.objects.filter(id=flightplan_refill.pk).update(start_time=start_time)
        flightplan = Flightplan.objects.filter(id=id_flightplan).update(status=1)
        fleet = Fleet.objects.filter(id=fleet_id).update(status=True, planet_status=0)