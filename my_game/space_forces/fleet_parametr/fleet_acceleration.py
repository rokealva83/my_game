# -*- coding: utf-8 -*-

from my_game.models import ElementShip, Ship, FleetParametrAcceleration, ModulePattern


def fleet_acceleration(*args):
    fleet = args[0]
    fleet_ships = Ship.objects.filter(fleet_status=1, place_id=fleet.id).all()
    fl_acceleration = fl_braking = fl_reverse = acceleration = braking = reverse = 0

    ship_fleet_project = len(fleet_ships)
    for fleet_ship in fleet_ships:
        ship_elements = ElementShip.objects.filter(project_ship=fleet_ship.project_ship, class_element=8).all()

        if ship_elements:
            acceleration = braking = reverse = 0
            for ship_element in ship_elements:
                element_pattern = ModulePattern.objects.filter(id=ship_element.element_pattern_id).first()
                if element_pattern.module_class == 1:
                    acceleration += ship_element.param1
                    braking += ship_element.param2
                    reverse += ship_element.param3

        fl_acceleration += acceleration * fleet_ship.amount_ship
        fl_braking += braking * fleet_ship.amount_ship
        fl_reverse += reverse * fleet_ship.amount_ship
    if ship_fleet_project:
        acceleration = fl_acceleration / ship_fleet_project
        braking = fl_braking / ship_fleet_project
        reverse = fl_reverse / ship_fleet_project
    if acceleration or reverse or braking:
        fleet_parametr_acceleration = FleetParametrAcceleration.objects.filter(fleet=fleet).first()
        if fleet_parametr_acceleration:
            setattr(fleet_parametr_acceleration, 'acceleration', acceleration)
            setattr(fleet_parametr_acceleration, 'braking', braking)
            setattr(fleet_parametr_acceleration, 'reverse', reverse)
            fleet_parametr_acceleration.save()
        else:
            fleet_parametr_acceleration = FleetParametrAcceleration(
                fleet=fleet,
                acceleration=acceleration,
                braking=braking,
                reverse=reverse
            )
            fleet_parametr_acceleration.save()

    return True
