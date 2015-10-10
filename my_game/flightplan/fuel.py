# -*- coding: utf-8 -*-


from my_game.flightplan.create.flight import calculation
import math
from my_game.models import FleetEnergyPower
from my_game.models import FlightplanFlight
from my_game.models import FleetEngine
from my_game.models import Ship, ElementShip, ModulePattern, HullPattern, ProjectShip
from my_game.models import Fleet, FuelPattern, FuelTank


def fuel(*args):
    fleet_id = args[0]
    flightplan_flight = args[1]
    fleet = args[2]

    fleet_engine = FleetEngine.objects.filter(fleet_id=fleet_id).first()
    fleet_energy_power = FleetEnergyPower.objects.filter(fleet_id=fleet_id).first()

    x1 = int(flightplan_flight.start_x)
    y1 = int(flightplan_flight.start_y)
    z1 = int(flightplan_flight.start_z)
    x2 = int(flightplan_flight.finish_x)
    y2 = int(flightplan_flight.finish_y)
    z2 = int(flightplan_flight.finish_z)

    distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)

    coordinate_giper = ''
    coordinate_null = ''
    flight_time = 600
    need_energy = 1

    if flightplan_flight.id_command == 1:
        flight_time = int(math.sqrt(distance / 2 * (int(fleet.ship_empty_mass)) / int(fleet_engine.system_power)) * 2)
        need_energy = fleet_energy_power.use_fuel_system
    elif flightplan_flight.id_command == 2:
        coordinate_giper = ''
        coordinate_null = ''
        need_energy = fleet_energy_power.use_fuel_intersystem
    elif flightplan_flight.id_command == 3:
        coordinate_giper = 1
        coordinate_null = ''
        need_energy = fleet_energy_power.use_energy_giper
    elif flightplan_flight.id_command == 4:
        coordinate_giper = ''
        coordinate_null = 1
        need_energy = fleet_energy_power.use_energy_null
    if flightplan_flight.id_command == 2 or flightplan_flight.id_command == 3 or flightplan_flight.id_command == 4:
        answer = calculation(fleet_id, coordinate_giper, coordinate_null, distance)
        flight_time = int(answer['flight_time'])

    if flightplan_flight.flight_time != flight_time:
        new_time = FlightplanFlight.objects.filter(id=flightplan_flight.pk).update(flight_time=flight_time)

    ship_in_fleets = Ship.objects.filter(fleet_status=1, place_id=fleet_id)
    hull_energy = 0
    for ship in ship_in_fleets:
        project = ProjectShip.objects.filter(id=ship.project_ship).first()
        hull = HullPattern.objects.filter(id=project.hull_id).first()
        hull_energy = hull_energy + hull.power_consuption * ship.amount_ship

    need_energy = need_energy + hull_energy
    need_fuel = 1.0 * need_energy / (fleet_energy_power.produce_energy / fleet_energy_power.use_fuel_generator) * (
        flight_time / 3600.0)
    return need_fuel


def fuel_process(*args):
    fleet_id = args[0]
    flightplan_process = args[1]
    flightplan = args[2]
    time_process = 0
    ship_in_fleets = Ship.objects.filter(fleet_status=1, place_id=fleet_id)

    if flightplan.class_command == 3:
        time_process = flightplan_process.time_extraction
    elif flightplan.class_command == 4:
        time_process = flightplan_process.time_refill
    elif flightplan.class_command == 6:
        time_process = flightplan_process.time_scanning
    elif flightplan.class_command == 8:
        time_process = flightplan_process.time

    need_fuel = need_fuel_process(ship_in_fleets, flightplan, time_process, fleet_id)

    return need_fuel


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
                        if element_pattern.module_class == 6 and element_pattern.param3 == flightplan.id_command and find == 0:
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

    fuel_tank = FuelTank.objects.filter(id=fuel_tank.id, fleet_id=fleet.id).update(amount_fuel=new_fuel,
                                                                                    mass_fuel=new_mass,
                                                                                    size_fuel=new_size)
    fleet_up = Fleet.objects.filter(id=fleet.id).update(free_fuel_tank=new_fleet_tank,
                                                        ship_empty_mass=new_fleet_mass)
