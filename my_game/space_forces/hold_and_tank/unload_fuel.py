# -*- coding: utf-8 -*-

from my_game.models import WarehouseElement
from my_game.models import FuelTank


def unload_fuel(*args):
    session_user = args[0]
    session_user_city = args[1]
    fleet = args[2]
    amount = args[3]
    fuel_tank_id = args[4]

    if amount != 0:
        if fleet.planet_status == 1:
            fuel_tank = FuelTank.objects.filter(id=fuel_tank_id).first()
            fuel = fuel_tank.fuel_pattern
            if int(fuel_tank.amount_fuel) <= int(amount):
                amount = fuel_tank.amount_fuel
                FuelTank.objects.filter(id=fuel_tank_id).delete()
            else:
                new_amount = int(fuel_tank.amount_fuel) - int(amount)
                new_fuel_mass = int(fuel_tank.mass_fuel) - int(fuel.fuel_mass * amount)
                new_fuel_size = int(fuel_tank.size_fuel) - int(fuel.fuel_size * amount)
                FuelTank.objects.filter(id=fuel_tank_id).update(amount_fuel=new_amount,
                                                                mass_fuel=new_fuel_mass,
                                                                size_fuel=new_fuel_size)
            warehouse_element = WarehouseElement.objects.filter(user=session_user, user_city=session_user_city,
                                                                element_class=14,
                                                                element_id=fuel_tank.fuel_pattern.id).first()

            if warehouse_element:
                new_amount = int(warehouse_element.amount) + amount
                WarehouseElement.objects.filter(user=session_user, user_city=session_user_city, element_class=14,
                                                element_id=fuel.id).update(amount=new_amount)
            else:
                WarehouseElement(
                    user=session_user,
                    user_city=session_user_city,
                    element_class=14,
                    element_id=fuel.id,
                    amount=amount
                )
            new_fleet_mass = int(fleet.ship_empty_mass) - int(fuel.fuel_mass * amount)
            new_free_fuel_tank = int(fleet.free_fuel_tank) + int(fuel.fuel_size * amount)
            setattr(fleet, 'ship_empty_mass', new_fleet_mass)
            setattr(fleet, 'free_fuel_tank', new_free_fuel_tank)
            fleet.save()

            message = 'Топливо выгружено'
        else:
            message = 'Флот не над планетой'
    else:
        message = 'Топливо не выбрано'
    return message
