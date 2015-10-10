# -*- coding: utf-8 -*-

from datetime import datetime
from my_game.models import Fleet, FuelTank, FuelPattern
from my_game.models import Flightplan, FlightplanColonization
from my_game.models import Planet, MyUser
from my_game.models import Hold, DevicePattern
from my_game.flightplan.fuel import fuel_process


def start_colonization(*args):
    fleet_id = args[0]

    fleet = Fleet.objects.filter(id=fleet_id).first()
    user = MyUser.objects.filter(id=fleet.user).first()
    flightplan = Flightplan.objects.filter(id_fleet=fleet_id).first()
    flightplan_colonization = FlightplanColonization.objects.filter(id_fleet=fleet_id).first()
    hold_modules = Hold.objects.filter(fleet_id=fleet_id, class_shipment=9)
    error = 1
    message = 'В трюме нет необходимого колонизационного устройства'
    planet = Planet.objects.filter(global_x=fleet.x, global_y=fleet.y, global_z=fleet.z, planet_type=user.race_id,
                                   planet_free=1).first()
    if planet:
        if fleet.planet != 0 and flightplan.id_command == 1:
            for hold_module in hold_modules:
                device = int(DevicePattern.objects.filter(id=hold_module.id_shipment).first().param3)
                if device == 1:
                    error = 0
                    message = 'Колонизация начата'
    else:
        message = 'По координатам нет планеты, она занята или же не пригодна для колонизации'

    if fleet.planet == 0 and flightplan.id_command == 2:
        for hold_module in hold_modules:
            device = int(DevicePattern.objects.filter(id=hold_module.id_shipment).first().param3)
            if device == 2:
                error = 0
                message = 'Развертка основы базы начата'

    need_fuel = fuel_process(fleet_id, flightplan_colonization, flightplan)
    fuel_tank = FuelTank.objects.filter(fleet_id=fleet_id).first()
    if fuel_tank:
        fuel_pattern = FuelPattern.objects.filter(user=fleet.user, fuel_class=fuel_tank.fuel_class).first()
        if need_fuel > fuel_tank.amount_fuel * fuel_pattern.efficiency:
            error = 1
            message = 'Нет топлива'

        if error == 0:
            if len(args) == 1:
                start_time = datetime.now()
            else:
                start_time = args[1]

            id_flightplan = flightplan.pk
            flightplan_colonization = FlightplanColonization.objects.filter(id_fleet=fleet_id).first()
            flightplan_colonization = FlightplanColonization.objects.filter(id=flightplan_colonization.pk).update(
                start_time=start_time)
            flightplan = Flightplan.objects.filter(id=id_flightplan).update(status=1)
            fleet = Fleet.objects.filter(id=fleet_id).update(status=True, planet_status=0)
    else:
        message = 'Нет топлива'

    return message
