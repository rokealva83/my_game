# -*- coding: utf-8 -*-

from my_game.models import ElementShip
from my_game.models import Fleet, ModulePattern
from my_game.space_forces.fleet_parametr import fleet_engine_parametr, fleet_parametr_resource_extraction
from my_game.space_forces.fleet_parametr import fleet_acceleration, fleet_build_repair_parametr
from my_game.space_forces.fleet_parametr import fleet_energy_power, ship_module_hold, fleet_scan_parametr


def fleet_parametr(*args):
    fleet_id = args[0]
    ship = args[1]
    amount_ship = args[2]
    added_remove = args[3]
    fleet = Fleet.objects.filter(id=fleet_id).first()
    ship_empty_mass = fleet.ship_empty_mass + ship.project_ship.ship_mass * amount_ship * added_remove
    free_fuel_tank = fleet.free_fuel_tank + ship.project_ship.hull_pattern.fuel_tank * amount_ship * added_remove

    ship_elements = ElementShip.objects.filter(project_ship=ship.project_ship).all()
    module_hold = ship_module_hold(ship_elements)
    empty_hold = fleet.empty_hold + (
                                    ship.project_ship.hull_pattern.hold_size + module_hold) * amount_ship * added_remove

    setattr(fleet, 'empty_hold', empty_hold)
    setattr(fleet, 'ship_empty_mass', ship_empty_mass)
    setattr(fleet, 'free_fuel_tank', free_fuel_tank)
    fleet.save()

    fleet_energy_power(fleet, ship, ship_elements, amount_ship, added_remove)
    fleet_engine_parametr(fleet)
    ship_scan_elements=[]
    ship_extraction_elements = []
    ship_repair_elements =[]
    ship_acceleration_elements = []
    for ship_element in ship_elements:
        if ship_element.class_element == 8:
            element_pattern = ModulePattern.objects.filter(id=ship_element.element_pattern_id).first()
            if element_pattern.module_class == 1:
                ship_acceleration_elements.append(element_pattern)
            if element_pattern.module_class == 3:
                ship_extraction_elements.append(element_pattern)
            if element_pattern.module_class == 5:
                ship_repair_elements.append(element_pattern)
            if element_pattern.module_class == 6:
                ship_scan_elements.append(element_pattern)
    if ship_repair_elements:
        fleet_build_repair_parametr(fleet, ship_repair_elements, amount_ship, added_remove)
    if ship_scan_elements:
        fleet_scan_parametr(fleet, ship_scan_elements, added_remove)
    if ship_extraction_elements:
        fleet_parametr_resource_extraction(fleet, ship_extraction_elements, amount_ship, added_remove)
    if ship_acceleration_elements:
        fleet_acceleration(fleet)
    return fleet
