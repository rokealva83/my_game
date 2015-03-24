# -*- coding: utf-8 -*-

import random
from datetime import datetime, timedelta

from django.utils import timezone

from my_game.models import Planet
from my_game.models import MyUser, User_city, User_scientic
from my_game.models import Turn_scientic, Turn_building, Turn_assembly_pieces, \
    Turn_production
from my_game.models import Factory_pattern, Factory_installed, Building_pattern, Building_installed
from my_game.models import Warehouse_factory, Warehouse_element, Warehouse
from knowledge import scientic_func
from my_game.models import Project_ship, Turn_ship_build, Ship, Fleet, Element_ship, Hold
from my_game.models import Flightplan, Flightplan_flight
from my_game.models import Trade_flight, Trade_teleport
from my_game.models import User_variables


def check_scientific_verification_queue(request):
    user = int(request)
    time = timezone.now()
    turn_scientics = Turn_scientic.objects.filter(user=user)
    user_variables = User_variables.objects.filter(id=1).first()
    if turn_scientics:
        for turn_scientic in turn_scientics:
            scin_id = turn_scientic.id
            time_start = turn_scientic.start_time_science
            delta_time = time - time_start
            new_delta = delta_time.seconds
            delta_time = turn_scientic.finish_time_science - turn_scientic.start_time_science
            delta = delta_time.seconds
            if new_delta > delta:
                scientic = User_scientic.objects.filter(user=user).first()
                all_scient = scientic.mathematics_up + scientic.phisics_up + scientic.biologic_chimics_up + \
                             scientic.energetics_up + scientic.radionics_up + scientic.nanotech_up + \
                             scientic.astronomy_up + scientic.logistic_up
                user_scientic = User_scientic.objects.filter(user=user).update(
                    mathematics_up=scientic.mathematics_up + turn_scientic.mathematics_up,
                    phisics_up=scientic.phisics_up + turn_scientic.phisics_up,
                    biologic_chimics_up=scientic.biologic_chimics_up + turn_scientic.biologic_chimics_up,
                    energetics_up=scientic.energetics_up + turn_scientic.energetics_up,
                    radionics_up=scientic.radionics_up + turn_scientic.radionics_up,
                    nanotech_up=scientic.nanotech_up + turn_scientic.nanotech_up,
                    astronomy_up=scientic.astronomy_up + turn_scientic.astronomy_up,
                    logistic_up=scientic.logistic_up + turn_scientic.logistic_up,
                )
                Turn_scientic.objects.filter(id=scin_id).delete()
                user_scientic = User_scientic.objects.filter(user=user).first()
                all_scient = user_scientic.mathematics_up + user_scientic.phisics_up + user_scientic.biologic_chimics_up + \
                             user_scientic.energetics_up + user_scientic.radionics_up + user_scientic.nanotech_up + \
                             user_scientic.astronomy_up + user_scientic.logistic_up
                user_scientic = User_scientic.objects.filter(user=user).update(all_scientic=all_scient)

    # the addition of new technology
    my_user = MyUser.objects.filter(user_id=user).first()
    table_scan_time = my_user.last_time_scan_scient
    delta = time - table_scan_time
    delta_time = delta.seconds

    if delta_time > user_variables.time_check_new_technology:
        all_scientic = User_scientic.objects.filter(user=user).first()
        if all_scientic.all_scientic > 10:
            new_technology = random.random()

            if 0 <= new_technology < 0.125:
                scientic_func.hull_upgrade(user)

            if 0.125 <= new_technology < 0.250:
                scientic_func.armor_upgrade(user)

            if 0.250 <= new_technology < 0.375:
                scientic_func.shield_upgrade(user)

            if 0.375 <= new_technology < 0.5:
                scientic_func.engine_upgrade(user)

            if 0.5 <= new_technology < 0.625:
                scientic_func.generator_upgrade(user)

            if 0.625 <= new_technology < 0.750:
                scientic_func.weapon_upgrade(user)

            if 0.750 <= new_technology < 0.875:
                scientic_func.shell_upgrade(user)

            if 0.875 <= new_technology <= 1:
                scientic_func.module_upgrade(user)


def verification_phase_of_construction(request):
    user = int(request)
    my_user = MyUser.objects.filter(user_id=user).first()
    turn_buildings = Turn_building.objects.filter(user=user)
    time = timezone.now()
    for turn_building in turn_buildings:
        time_start = turn_building.start_time_deployment
        delta_time = time - time_start
        new_delta = delta_time.seconds
        delta_time = turn_building.finish_time_deployment - turn_building.start_time_deployment
        delta = delta_time.seconds
        user_city = User_city.objects.filter(user=user, id=turn_building.user_city).first()
        if new_delta > delta:
            elapsed_time = turn_building.finish_time_deployment - my_user.last_time_check
            elapsed_time_seconds = elapsed_time.seconds
            time_update = turn_building.finish_time_deployment
            verification_of_resources(user, elapsed_time_seconds, time_update)
            if turn_building.class_id < 13:
                factory_pattern = Factory_pattern.objects.filter(id=turn_building.factory_id).first()
                factory_installed = Factory_installed(
                    user=user,
                    user_city=user_city.id,
                    factory_pattern_id=turn_building.factory_id,
                    name=factory_pattern.name,
                    time_deployment=factory_pattern.time_deployment,
                    production_class=factory_pattern.production_class,
                    production_id=factory_pattern.production_id,
                    time_production=factory_pattern.time_production,
                    size=factory_pattern.size,
                    mass=factory_pattern.mass,
                    power_consumption=factory_pattern.power_consumption,
                )
                factory_installed.save()
            else:
                factory_pattern = Building_pattern.objects.filter(id=turn_building.factory_id).first()
                factory_installed = Building_installed(
                    user=user,
                    user_city=user_city.id,
                    building_pattern_id=turn_building.factory_id,
                    name=factory_pattern.name,
                    time_deployment=factory_pattern.time_deployment,
                    production_class=factory_pattern.production_class,
                    production_id=factory_pattern.production_id,
                    time_production=factory_pattern.time_production,
                    warehouse=0,
                    max_warehouse=factory_pattern.max_warehouse,
                    size=factory_pattern.size,
                    mass=factory_pattern.mass,
                    power_consumption=factory_pattern.power_consumption,
                )
                factory_installed.save()
            if factory_pattern.production_class == 12:
                new_power = user_city.power + factory_installed.power_consumption
                user_city = User_city.objects.filter(id=user_city.id).update(power=new_power)
            else:
                new_energy = user_city.use_energy + factory_installed.power_consumption
                user_city = User_city.objects.filter(id=user_city.id).update(use_energy=new_energy)

            if factory_pattern.production_class == 10:
                user_city = User_city.objects.filter(user=user, id=turn_building.user_city).first()
                new_max_population = user_city.max_population + 100 * factory_pattern.production_id
                user_city = User_city.objects.filter(id=user_city.id).update(max_population=new_max_population)

            turn_building = Turn_building.objects.filter(id=turn_building.id).delete()


def verification_of_resources(*args):
    arg = args
    user = arg[0]
    elapsed_time_seconds = arg[1]
    time_update = arg[2]
    tax = 0.01
    user_citys = User_city.objects.filter(user=user)
    for user_city in user_citys:
        city_id = user_city.id
        check_user_factory_resourse_city = Factory_installed.objects.filter(user=user, user_city=city_id,
                                                                            production_class=11)
        attributes = ['resource1', 'resource2', 'resource3', 'resource4', 'mineral1', 'mineral2', 'mineral3',
                      'mineral4']
        prod_id = 1
        for attribute in attributes:
            check_factorys = check_user_factory_resourse_city.filter(production_id=prod_id)
            resourse = 0

            for check_factory in check_factorys:
                resourse = resourse + elapsed_time_seconds / check_factory.time_production
            warehouse = Warehouse.objects.filter(user=user, user_city=city_id, id_resource=prod_id).first()
            new_resourse = warehouse.amount + resourse
            warehouse = Warehouse.objects.filter(user=user, user_city=city_id, id_resource=prod_id).update(
                amount=new_resourse)
            prod_id = prod_id + 1

        population = 0
        population_buildings = Factory_installed.objects.filter(user=user, user_city=city_id, production_class=10)
        for population_building in population_buildings:
            population = population + elapsed_time_seconds / population_building.time_production

        new_population = user_city.population + population
        if new_population > user_city.max_population:
            new_population = user_city.max_population
        user_city = User_city.objects.filter(id=city_id).update(population=new_population)

        check_all_user_factorys = Factory_installed.objects.filter(user=user, user_city=city_id)
        total_number_specialists = 0
        for check_all_user_factory in check_all_user_factorys:
            install_factory = Factory_pattern.objects.filter(id=check_all_user_factory.factory_pattern_id).first()
            total_number_specialists = total_number_specialists + install_factory.cost_expert_deployment
        increase_internal_currency = total_number_specialists * elapsed_time_seconds * tax
        new_internal_currency = MyUser.objects.get(user_id=user).internal_currency + increase_internal_currency
        money = MyUser.objects.filter(user_id=user).update(internal_currency=new_internal_currency)

        trade_building = Building_installed.objects.filter(user=user, user_city=city_id, production_class=13).first()
        if trade_building:
            if trade_building.max_warehouse > trade_building.warehouse:
                energy = elapsed_time_seconds / trade_building.time_production
                stock_energy = trade_building.warehouse
                new_energy = stock_energy + energy
                if new_energy > trade_building.max_warehouse:
                    new_energy = trade_building.max_warehouse
                trade_building = Building_installed.objects.filter(user=user, user_city=city_id,
                                                                   production_class=13).update(warehouse=new_energy)

    last_time_update = time_update
    last_time_scan_scient = datetime(last_time_update.year, last_time_update.month, last_time_update.day, 0, 0, 0,
                                     0)
    MyUser.objects.filter(user_id=user).update(last_time_check=last_time_update,
                                               last_time_scan_scient=last_time_scan_scient)


def check_assembly_line_workpieces(request):
    user = int(request)
    my_user = MyUser.objects.filter(user_id=user).first()
    turn_assembly_piecess = Turn_assembly_pieces.objects.filter(user=user)
    time = timezone.now()
    for turn_assembly_pieces in turn_assembly_piecess:
        time_start = turn_assembly_pieces.start_time_assembly
        delta_time = time - time_start
        new_delta = delta_time.seconds
        delta_time = turn_assembly_pieces.finish_time_assembly - turn_assembly_pieces.start_time_assembly
        delta = delta_time.seconds
        user_city = User_city.objects.filter(user=user, id=turn_assembly_pieces.user_city).first()
        warehouse_factory = Warehouse_factory.objects.filter(factory_id=turn_assembly_pieces.pattern_id,
                                                             production_class=turn_assembly_pieces.class_id).first()
        if new_delta > delta:
            if warehouse_factory is not None:
                amount_assembly = turn_assembly_pieces.amount_assembly + warehouse_factory.amount
                warehouse_factory = Warehouse_factory.objects.filter(factory_id=turn_assembly_pieces.pattern_id,
                                                                     production_class=turn_assembly_pieces.class_id).update(
                    amount=amount_assembly)
            else:
                factory_pattern = Building_pattern.objects.filter(id=turn_assembly_pieces.pattern_id,
                                                                  production_class=turn_assembly_pieces.class_id).first()
                new_factory = Warehouse_factory(
                    user=turn_assembly_pieces.user,
                    user_city=turn_assembly_pieces.user_city,
                    factory_id=turn_assembly_pieces.pattern_id,
                    production_class=factory_pattern.production_class,
                    production_id=factory_pattern.production_id,
                    time_production=factory_pattern.time_production,
                    amount=turn_assembly_pieces.amount_assembly,
                    size=factory_pattern.size,
                    mass=factory_pattern.mass,
                    power_consumption=factory_pattern.power_consumption
                )
                new_factory.save()
            end_turn_assembly_pieces = Turn_assembly_pieces.objects.filter(id=turn_assembly_pieces.id).delete()


def verification_stage_production(request):
    user = request
    user_citys = User_city.objects.filter(user=user)
    for user_city in user_citys:
        city_id = user_city.id
        turn_productions = Turn_production.objects.filter(user=user, user_city=user_city.id).order_by(
            'start_time_production')
        for turn_production in turn_productions:
            time = timezone.now()
            time_start = turn_production.start_time_production
            delta_time = time - time_start
            new_delta = delta_time.seconds
            delta_time = turn_production.finish_time_production - turn_production.start_time_production
            delta = delta_time.seconds
            if new_delta > delta:
                work_factory = Factory_installed.objects.filter(id=turn_production.factory_id).first()
                warehouse = Warehouse_element.objects.filter(element_id=turn_production.element_id,
                                                             element_class=work_factory.production_class).first()
                if warehouse is not None:
                    new_amount = warehouse.amount + turn_production.amount_element
                    warehouse = Warehouse_element.objects.filter(element_id=turn_production.element_id).update(
                        amount=new_amount)
                else:
                    warehouse = Warehouse_element(
                        user=user,
                        user_city=user_city.id,
                        element_class=work_factory.production_class,
                        element_id=turn_production.element_id,
                        amount=turn_production.amount_element
                    )
                    warehouse.save()
                turn_production_delete = Turn_production.objects.filter(id=turn_production.id).delete()


def verification_turn_ship_build(request):
    user = request
    user_citys = User_city.objects.filter(user=user)
    for user_city in user_citys:
        city_id = int(user_city.id)
        turn_ship_build = Turn_ship_build.objects.filter(user=user, user_city=user_city.id).first()
        if turn_ship_build:
            time = timezone.now()
            time_start = turn_ship_build.start_time_build
            delta_time = time - time_start
            new_delta = delta_time.seconds
            delta_time = turn_ship_build.finish_time_build - turn_ship_build.start_time_build
            delta = delta_time.seconds
            if new_delta > delta:
                if turn_ship_build.process_id == 1:
                    dock = Ship.objects.filter(id_project_ship=turn_ship_build.ship_pattern, fleet_status=0).first()
                    create_ship = Project_ship.objects.filter(user=user, id=turn_ship_build.ship_pattern).first()
                    if dock is not None:
                        new_amount = dock.amount_ship + turn_ship_build.amount
                        dock = Ship.objects.filter(id_project_ship=turn_ship_build.ship_pattern, fleet_status=0).update(
                            amount_ship=new_amount)
                    else:
                        dock = Ship(
                            user=user,
                            id_project_ship=turn_ship_build.ship_pattern,
                            name=create_ship.name,
                            amount_ship=turn_ship_build.amount,
                            fleet_status=0,
                            place_id=city_id
                        )
                        dock.save()
                    turn_ship_build_delete = Turn_ship_build.objects.filter(id=turn_ship_build.id).delete()

                elif turn_ship_build.process_id == 2:
                    element_ships = Element_ship.objects.filter(id_project_ship=turn_ship_build.ship_pattern)
                    for element_ship in element_ships:
                        warehouse_element = Warehouse_element.objects.filter(element_class=element_ship.class_element,
                                                                             element_id=element_ship.id_element_pattern).first()
                        new_amount = warehouse_element.amount + (1 * turn_ship_build.amount)
                        warehouse_element = Warehouse_element.objects.filter(element_class=element_ship.class_element,
                                                                             element_id=element_ship.id_element_pattern).update(
                            amount=new_amount)

                elif turn_ship_build.process_id == 3:
                    element_ships = Element_ship.objects.filter(id_project_ship=turn_ship_build.ship_pattern)
                    for element_ship in element_ships:
                        if element_ship.class_element == 7:
                            class_element = 6
                        else:
                            class_element = element_ship.class_element
                        warehouse_element = Warehouse_element.objects.filter(element_class=class_element,
                                                                             element_id=element_ship.id_element_pattern).first()

                        new_amount = warehouse_element.amount + (1 * turn_ship_build.amount)
                        warehouse_element = Warehouse_element.objects.filter(element_class=class_element,
                                                                             element_id=element_ship.id_element_pattern).update(
                            amount=new_amount)
                    dock = Ship.objects.filter(id_project_ship=turn_ship_build.ship_pattern).first()
                    create_ship = Project_ship.objects.filter(user=user, id=turn_ship_build.ship_pattern).first()
                    if dock is not None:
                        new_amount = dock.amount_ship + turn_ship_build.amount
                        dock = Ship.objects.filter(id_project_ship=turn_ship_build.ship_pattern).update(
                            amount_ship=new_amount)
                    else:
                        dock = Ship(
                            user=user,
                            id_project_ship=turn_ship_build.ship_pattern,
                            name=create_ship.name,
                            amount_ship=turn_ship_build.amount,
                            fleet_status=0,
                            place_id=city_id
                        )
                        dock.save()
                    turn_ship_build_delete = Turn_ship_build.objects.filter(id=turn_ship_build.id).delete()


def verification_flight_list(request):
    user = request
    fleets = Fleet.objects.filter(user=user)
    for fleet in fleets:
        flightplans = Flightplan.objects.filter(id_fleet=fleet.id)
        flightplan_len = len(flightplans)
        lens = 0
        for flightplan in flightplans:
            if flightplan.status == 1:
                if flightplan.class_command == 1:
                    flightplan_flight = Flightplan_flight.objects.filter(id_fleetplan=flightplan.id).first()
                    flightplan_id = int(flightplan.id)
                    time = timezone.now()
                    time_start = flightplan_flight.start_time
                    delta_time = time - time_start
                    new_delta = delta_time.seconds
                    delta = flightplan_flight.flight_time
                    if new_delta > delta:
                        if flightplan_flight.planet != 0:
                            planet_status = 1
                            planet = Planet.objects.filter(system_id=flightplan_flight.system,
                                                           planet_num=flightplan_flight.planet).first()
                            x = planet.x
                            y = planet.y
                            z = planet.z

                        else:
                            planet_status = 0
                            x = flightplan_flight.finish_x / 1000.0
                            y = flightplan_flight.finish_y / 1000.0
                            z = flightplan_flight.finish_z / 1000.0

                        fleet_up = Fleet.objects.filter(id=fleet.id).update(x=x, y=y, z=z, planet_status=planet_status,
                                                                            planet=flightplan_flight.planet,
                                                                            system=flightplan_flight.system)

                        old_flightplan_flight = flightplan_flight
                        flightplan_flight = Flightplan_flight.objects.filter(id_fleetplan=flightplan.id).delete()
                        flightplan_flight = Flightplan_flight.objects.filter(id_fleet=flightplan.id_fleet).first()

                        if flightplan_flight:
                            finish_time = old_flightplan_flight.start_time + timedelta(
                                seconds=flightplan_flight.flight_time)

                            start_x = old_flightplan_flight.finish_x
                            start_y = old_flightplan_flight.finish_y
                            start_z = old_flightplan_flight.finish_z
                            flightplan_flight = Flightplan_flight.objects.filter(id_fleet=flightplan.id_fleet).update(
                                start_x=start_x, start_y=start_y, start_z=start_z,
                                start_time=old_flightplan_flight.finish_time)

                        flightplan = Flightplan.objects.filter(id=flightplan_id).delete()
            lens = lens + 1
            if lens == flightplan_len:
                fleet_up = Fleet.objects.filter(id=fleet.id).update(status=0)
            else:
                flightplan = Flightplan.objects.filter(id_fleet=fleet.id).first().update(status=1)


def verification_trade(request):
    user = request
    time = timezone.now()
    fleets = Fleet.objects.filter(user=user, name='Trade', status=1)
    for fleet in fleets:
        trade_flights = Trade_flight.objects.filter(id_fleet=fleet.id)
        flightplan_len = len(trade_flights)
        lens = 0
        for trade_flight in trade_flights:
            user_city = User_city.objects.filter(id=trade_flight.user_city).first()
            if trade_flight.status == 1:
                if trade_flight.id_flight == 1:
                    time_start = trade_flight.start_time
                    delta_time = time - time_start
                    new_delta = delta_time.seconds
                    delta = trade_flight.flight_time
                    if new_delta > delta:
                        x = trade_flight.finish_x
                        y = trade_flight.finish_y
                        z = trade_flight.finish_z
                        fleet_up = Fleet.objects.filter(id=fleet.id).update(x=x, y=y, z=z)
                        trade_flight = Trade_flight.objects.filter(id_fleet=fleet.id).first()
                        trade_flight = Trade_flight.objects.filter(id=trade_flight.id).delete()
                        trade_flight = Trade_flight.objects.filter(id_fleet=fleet.id).first()
                        trade_flight = Trade_flight.objects.filter(id=trade_flight.id).update(status=1)
                elif trade_flight.id_flight == 2:
                    time_start = trade_flight.start_time
                    delta_time = time - time_start
                    new_delta = delta_time.seconds
                    delta = trade_flight.flight_time
                    if new_delta > delta:
                        hold = Hold(
                            fleet_id=trade_flight.id_fleet,
                            class_shipment=trade_flight.class_element,
                            id_shipment=trade_flight.id_element,
                            amount_shipment=trade_flight.amount,
                            mass_shipment=trade_flight.mass,
                            size_shipment=trade_flight.size
                        )
                        hold.save()

                        new_mass = fleet.ship_empty_mass + trade_flight.mass
                        empty_hold = fleet.empty_hold - trade_flight.size
                        fleet_up = Fleet.objects.filter(id=fleet.id).update(empty_hold=empty_hold,
                                                                            ship_empty_mass=new_mass)
                        trade_flight = Trade_flight.objects.filter(id_fleet=fleet.id).first()
                        trade_flight = Trade_flight.objects.filter(id=trade_flight.id).delete()
                        trade_flight = Trade_flight.objects.filter(id_fleet=fleet.id).first()
                        if trade_flight:
                            trade_flight = Trade_flight.objects.filter(id=trade_flight.id).update(status=1)
                        else:
                            planet = Planet.objects.filter(x=fleet.x, y=fleet.y, z=fleet.z).first()
                            if planet:
                                planet_status = 1
                            else:
                                planet_status = 0
                            fleet = Fleet.objects.filter(id=fleet.id).update(planet=user_city.planet_id,
                                                                             system=user_city.system_id, status=0,
                                                                             planet_status=planet_status)

                elif trade_flight.id_flight == 3:
                    time_start = trade_flight.start_time
                    delta_time = time - time_start
                    new_delta = delta_time.seconds
                    delta = trade_flight.flight_time
                    if new_delta > delta:
                        hold = Hold.objects.filter(fleet_id=fleet.id).first()

                        if hold.class_shipment == 0:
                            warehouse = Warehouse.objects.filter(user=user, user_city=trade_flight.user_city,
                                                                 id_resource=trade_flight.id_element).first()
                            new_amount = warehouse.amount + trade_flight.amount
                            warehouse = Warehouse.objects.filter(user=user, user_city=trade_flight.user_city,
                                                                 id_resource=trade_flight.id_element).update(
                                amount=new_amount)

                        elif 0 < hold.class_shipment < 9:
                            warehouse = Warehouse_element.objects.filter(user=user, user_city=trade_flight.user_city,
                                                                         element_class=trade_flight.class_element,
                                                                         element_id=trade_flight.id_element).first()
                            if warehouse:
                                new_amount = warehouse.amount + trade_flight.amount
                                warehouse = Warehouse_element.objects.filter(user=user,
                                                                             user_city=trade_flight.user_city,
                                                                             element_class=trade_flight.class_element,
                                                                             element_id=trade_flight.id_element).update(
                                    amount=new_amount)
                            else:
                                warehouse = Warehouse_element(
                                    user=user,
                                    user_city=trade_flight.user_city,
                                    element_class=trade_flight.class_element,
                                    element_id=trade_flight.id_element,
                                    amount=trade_flight.amount
                                )
                        elif hold.class_shipment > 9:
                            warehouse = Warehouse_factory.objects.filter(user=user, user_city=trade_flight.user_city,
                                                                         production_class__lt=13,
                                                                         factory_id=trade_flight.id_element).first()
                            if warehouse:
                                new_amount = warehouse.amount + trade_flight.amount
                                warehouse = Warehouse_factory.objects.filter(user=user,
                                                                             user_city=trade_flight.user_city,
                                                                             production_class__lt=13,
                                                                             factory_id=trade_flight.id_element).update(
                                    amount=new_amount)
                            else:
                                factory_rattern = Factory_pattern.objects.filter(id=trade_flight.id_element).first()

                                warehouse = Warehouse_factory(
                                    user=user,
                                    user_city=trade_flight.user_city,
                                    factory_id=trade_flight.id_element,
                                    production_class=factory_rattern.production_class,
                                    production_id=factory_rattern.production_id,
                                    time_production=factory_rattern.time_production,
                                    amount=trade_flight.amount,
                                    size=factory_rattern.size,
                                    mass=factory_rattern.mass,
                                    power_consuption=factory_rattern.power_consuption,
                                )

                        hold = Hold.objects.filter(fleet_id=fleet.id).delete()
                        new_mass = fleet.ship_empty_mass - trade_flight.mass
                        empty_hold = fleet.empty_hold + trade_flight.size
                        fleet_up = Fleet.objects.filter(id=fleet.id).update(empty_hold=empty_hold,
                                                                            ship_empty_mass=new_mass)
                        trade_flight = Trade_flight.objects.filter(id_fleet=fleet.id).first()
                        trade_flight = Trade_flight.objects.filter(id=trade_flight.id).delete()
                        trade_flight = Trade_flight.objects.filter(id_fleet=fleet.id).first()
                        if trade_flight:
                            trade_flight = Trade_flight.objects.filter(id=trade_flight.id).update(status=1)
                        else:
                            planet = Planet.objects.filter(x=fleet.x, y=fleet.y, z=fleet.z).first()
                            if planet:
                                planet_status = 1
                            else:
                                planet_status = 0
                            fleet = Fleet.objects.filter(id=fleet.id).update(planet=user_city.planet_id,
                                                                             system=user_city.system_id, status=0,
                                                                             planet_status=planet_status)

    teleports = Trade_teleport.objects.filter(user=user)
    for teleport in teleports:
        teleport_id = teleport.id
        time_start = teleport.start_teleport
        delta_time = time - time_start
        new_delta = delta_time.seconds
        delta = teleport.finish_teleport - teleport.start_teleport
        delta = delta.seconds
        if new_delta > delta:

            if teleport.class_element == 0:
                warehouse = Warehouse.objects.filter(user=user, user_city=teleport.user_city,
                                                     id_resource=teleport.id_element).first()
                new_amount = warehouse.amount + teleport.amount
                warehouse = Warehouse.objects.filter(user=user, user_city=teleport.user_city,
                                                     id_resource=teleport.id_element).update(amount=new_amount)

            elif 0 < teleport.class_element < 9:
                warehouse = Warehouse_element.objects.filter(user=user, user_city=teleport.user_city,
                                                             element_class=teleport.class_element,
                                                             element_id=teleport.id_element).first()
                if warehouse:
                    new_amount = warehouse.amount + teleport.amount
                    warehouse = Warehouse_element.objects.filter(user=user, user_city=teleport.user_city,
                                                                 element_class=teleport.class_element,
                                                                 element_id=teleport.id_element).update(
                        amount=new_amount)
                else:
                    warehouse = Warehouse_element(
                        user=user,
                        user_city=teleport.user_city,
                        element_class=teleport.class_element,
                        element_id=teleport.id_element,
                        amount=teleport.amount
                    )
            elif teleport.class_shipment > 9:
                warehouse = Warehouse_factory.objects.filter(user=user, user_city=teleport.user_city,
                                                             production_class__lt=13,
                                                             factory_id=teleport.id_element).first()
                if warehouse:
                    new_amount = warehouse.amount + teleport.amount
                    warehouse = Warehouse_factory.objects.filter(user=user, user_city=teleport.user_city,
                                                                 production_class__lt=13,
                                                                 factory_id=teleport.id_element).update(
                        amount=new_amount)
                else:
                    factory_rattern = Factory_pattern.objects.filter(id=teleport.id_element).first()

                    warehouse = Warehouse_factory(
                        user=user,
                        user_city=teleport.user_city,
                        factory_id=teleport.id_element,
                        production_class=factory_rattern.production_class,
                        production_id=factory_rattern.production_id,
                        time_production=factory_rattern.time_production,
                        amount=teleport.amount,
                        size=factory_rattern.size,
                        mass=factory_rattern.mass,
                        power_consuption=factory_rattern.power_consuption,
                    )
            teleport = Trade_teleport.objects.filter(id=teleport_id).delete()



































