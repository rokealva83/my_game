# -*- coding: utf-8 -*-


from my_game.models import Fleet, FuelPattern, FuelTank


def minus_fuel(*args):
    fleet = args[0]
    need_fuel = args[1]

    fuel_tank = FuelTank.objects.filter(fleet_id=fleet.id).first()
    fuel_pattern = FuelPattern.objects.filter(user=fleet.user, fuel_class=fuel_tank.fuel_class).first()

    need_fuel = need_fuel / fuel_pattern.efficiency

    new_fuel = int(fuel_tank.amount_fuel - need_fuel)
    new_mass = int(fuel_tank.mass_fuel - need_fuel * fuel_pattern.mass)
    new_size = int(fuel_tank.size_fuel - need_fuel * fuel_pattern.size)
    new_fleet_tank = int(fleet.free_fuel_tank + need_fuel)
    new_fleet_mass = int(fleet.ship_empty_mass - need_fuel * fuel_pattern.mass)

    FuelTank.objects.filter(id=fuel_tank.id, fleet_id=fleet.id).update(amount_fuel=new_fuel, mass_fuel=new_mass,
                                                                       size_fuel=new_size)
    Fleet.objects.filter(id=fleet.id).update(free_fuel_tank=new_fleet_tank, ship_empty_mass=new_fleet_mass)
