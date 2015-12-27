# -*- coding: utf-8 -*-


from my_game.models import FleetEnergyPower
from my_game.models import ElementShip, ModulePattern, HullPattern, ProjectShip


def need_fuel_process(*args):
    ship_in_fleets = args[0]
    flightplan = args[1]
    time_process = args[2]
    fleet_id = args[3]
    fleet_energy_power = FleetEnergyPower.objects.filter(fleet_id=fleet_id).first()
    find = 0
    hull_energy = 0
    need_energy = 0

    for ship in ship_in_fleets:
        if flightplan.class_command == 3:
            element_ships = ElementShip.objects.filter(id_project_ship=ship.id_project_ship)
            for element_ship in element_ships:
                if element_ship.class_element == 8:
                    element_pattern = ModulePattern.objects.filter(id=element_ship.element_pattern_id).first()

                    if flightplan.class_command == 3:
                        if element_pattern.module_class == 3:
                            need_energy = element_pattern.power_consuption

                    elif flightplan.class_command == 6:
                        if element_pattern.module_class == 6 and element_pattern.param3 == flightplan.id_command and (
                                    find == 0):
                            find = 1
                        need_energy = element_pattern.power_consuption

        project = ProjectShip.objects.filter(id=ship.id_project_ship).first()
        hull = HullPattern.objects.filter(id=project.hull_id).first()
        hull_energy = hull_energy + hull.power_consuption * ship.amount_ship
        if flightplan.class_command != 6:
            need_energy = need_energy * ship.amount_ship

    need_energy = need_energy + hull_energy
    need_fuel = 1.0 * need_energy / (fleet_energy_power.produce_energy / fleet_energy_power.use_fuel_generator) * (
        time_process / 3600.0)

    return need_fuel
