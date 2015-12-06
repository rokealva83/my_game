# -*- coding: utf-8 -*-

from my_game.models import FuelPattern
from my_game.models import BasicFuel
from my_game.knowledge.new_factory_pattern import new_factory_pattern


def open_fuel(*args):
    user = args[0]
    system = args[1]
    inter = args[2]
    fuel_class = 0
    if system != 0 and inter != 0:
        fuel_class = 3
    elif system != 0 and inter == 0:
        fuel_class = 1
    elif system == 0 and inter != 0:
        fuel_class = 2
    fuel_pattern = FuelPattern.objects.filter(user=user, fuel_class=fuel_class).first()
    if fuel_pattern is None:
        basic_fuel = BasicFuel.objects.filter(fuel_class=fuel_class).first()
        fuel_pattern = FuelPattern(
            user=user,
            element_name=basic_fuel.element_name,
            basic_fuel=basic_fuel,
            fuel_mass=basic_fuel.fuel_mass,
            fuel_size=basic_fuel.fuel_size,
            fuel_efficiency=basic_fuel.fuel_efficiency,
            fuel_class=basic_fuel.fuel_class,
            fuel_id=basic_fuel.fuel_id,
            price_internal_currency=basic_fuel.price_internal_currency,
            price_veriarit=basic_fuel.price_veriarit,
            price_inneilit=basic_fuel.price_inneilit,
            price_renniit=basic_fuel.price_renniit,
            price_cobalt=basic_fuel.price_cobalt,
            price_chemical=basic_fuel.price_chemical,
        )
        new_factory_pattern(user, 14, fuel_pattern)
