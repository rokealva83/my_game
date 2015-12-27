# -*- coding: utf-8 -*-

from my_game.models import FuelPattern
from my_game.models import BasicFuel, UserScientic
from my_game.knowledge.new_factory_pattern import new_factory_pattern
import random


def open_fuel(*args):
    user = args[0]
    engine_scient = args[1]
    generator_scient = args[2]
    if engine_scient:
        fuels = engine_scient.fuel.all()
        fuel_class = 2
    elif generator_scient:
        fuels = generator_scient.fuel.all()
        fuel_class = 1
    else:
        fuel_class = random.randint(1, 2)
        fuels = BasicFuel.objects.filter(fuel_class=fuel_class).all()

    all_scientic = UserScientic.objects.filter(user=user).first().all_scientic
    fuel_patterns = FuelPattern.objects.filter(user=user, fuel_class=fuel_class).all()
    if fuel_patterns:
        fuel_basics = []
        for fuel_pattern in fuel_patterns:
            fuel_basics.append(fuel_pattern.basic_pattern)
        for fuel in fuels:
            if all_scientic > fuel.min_all_scientic and fuel not in fuel_basics:
                new_fuel_pattern = new_fuel(user, fuel)
                new_factory_pattern(user, 14, new_fuel_pattern)
                break
    else:
        if all_scientic > fuels[0].min_all_scientic:
            new_fuel_pattern = new_fuel(user, fuels[0])
            new_factory_pattern(user, 14, new_fuel_pattern)


def new_fuel(*args):
    user = args[0]
    fuel = args[1]
    fuel_pattern = FuelPattern(
        user=user,
        element_name=fuel.fuel_name,
        basic_pattern=fuel,
        fuel_mass=fuel.fuel_mass,
        fuel_size=fuel.fuel_size,
        fuel_efficiency=fuel.fuel_efficiency,
        fuel_class=fuel.fuel_class,
        price_internal_currency=fuel.price_internal_currency,
        price_veriarit=fuel.price_veriarit,
        price_inneilit=fuel.price_inneilit,
        price_renniit=fuel.price_renniit,
        price_cobalt=fuel.price_cobalt,
        price_chemical=fuel.price_chemical,
    )
    fuel_pattern.save()
    return fuel_pattern.basic_pattern.pk
