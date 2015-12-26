# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity
from my_game.models import ElementShip, ModulePattern, EnginePattern, GeneratorPattern, \
    ShieldPattern, WeaponPattern
from my_game.models import ProjectShip, Ship, Fleet, FleetParametrScan, FleetEngine, FleetEnergyPower, \
    FleetParametrResourceExtraction, FleetParametrBuildRepair
from my_game import function


def add_ship(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        function.check_all_queues(session_user)
        flightplans = {}
        flightplan_flights = {}
        warehouse_factorys = {}
        command = 1
        hold = ship_id = amount_ship = 0
        message = ''
        fleet_id = 0
        full_request = request.POST
        my_dictionary = dict(full_request.iterlists())
        amount_ship_dict = my_dictionary.get('amount_ship')
        fleet_id_dict = my_dictionary.get('hidden_fleet')
        ship_id_dict = my_dictionary.get('hidden_ship')
        len_amount_ship_dict = int(len(amount_ship_dict))
        for i in range(len_amount_ship_dict):
            if int(amount_ship_dict[i]) != 0:
                amount_ship = int(amount_ship_dict[i])
                fleet_id = int(fleet_id_dict[i])
                ship_id = int(ship_id_dict[i])
        if amount_ship and fleet_id and ship_id:
            ship = Ship.objects.filter(id=ship_id, user=session_user, fleet_status=0,
                                       place_id=session_user_city.id).first()
            fleet = Fleet.objects.filter(id=fleet_id).first()
            fleet_engine = FleetEngine.objects.filter(fleet=fleet).first()
            fleet_energy_power = FleetEnergyPower.objects.filter(fleet=fleet).first()
            city_planet = int(session_user_city.planet.id)
            fleet_planet = int(fleet.planet_id)
            if fleet.status == 0 and city_planet == fleet_planet:
                if amount_ship > 0:
                    if int(ship.amount_ship) >= int(amount_ship):
                        ship_fleet = Ship.objects.filter(project_ship=ship.project_ship, user=session_user,
                                                         fleet_status=1,
                                                         place_id=fleet.id).first()
                        ship_elements = ElementShip.objects.filter(project_ship=ship.project_ship).all()
                        use_energy = ship.project_ship.hull_pattern.power_consuption
                        use_fuel_system = use_fuel_intersystem = use_energy_giper = 0
                        use_energy_null = use_fuel_generator = 0
                        produced_energy = 0
                        for ship_element in ship_elements:
                            if ship_element.class_element == 3:
                                element_pattern = ShieldPattern.objects.filter(
                                    id=ship_element.element_pattern_id).first()
                                use_energy = use_energy + element_pattern.power_consuption

                            if ship_element.class_element == 4:
                                engine_pattern = EnginePattern.objects.filter(
                                    id=ship_element.element_pattern_id).first()
                                if engine_pattern.system_power != 0:
                                    use_fuel_system = use_fuel_system + engine_pattern.power_consuption
                                if engine_pattern.intersystem_power != 0:
                                    use_fuel_intersystem = use_fuel_intersystem + engine_pattern.power_consuption
                                if engine_pattern.giper_power != 0:
                                    use_energy_giper = use_energy_giper + engine_pattern.power_consuption
                                if engine_pattern.nullT_power != 0:
                                    use_energy_null = use_energy_null + engine_pattern.power_consuption

                            if ship_element.class_element == 5:
                                element_pattern = GeneratorPattern.objects.filter(
                                    id=ship_element.element_pattern_id).first()
                                use_fuel_generator = use_fuel_generator + element_pattern.fuel_necessary
                                produced_energy = produced_energy + element_pattern.produced_energy

                            if ship_element.class_element == 6:
                                element_pattern = WeaponPattern.objects.filter(
                                    id=ship_element.element_pattern_id).first()
                                use_energy = use_energy + element_pattern.power_consuption

                            if ship_element.class_element == 7:
                                element_pattern = WeaponPattern.objects.filter(
                                    id=ship_element.element_pattern_id).first()
                                use_energy = use_energy + element_pattern.power_consuption

                            if ship_element.class_element == 8:
                                element_pattern = ModulePattern.objects.filter(id=ship_element.element_pattern_id,
                                                                               module_class=2).first()
                                if element_pattern:
                                    hold = hold + element_pattern.param1
                                    use_energy = use_energy + element_pattern.power_consuption

                                element_pattern = ModulePattern.objects.filter(id=ship_element.element_pattern_id,
                                                                               module_class=3).first()
                                if element_pattern:
                                    fleet_parametr_resource_extraction = FleetParametrResourceExtraction.objects.filter(
                                        fleet=fleet).first()
                                    if fleet_parametr_resource_extraction:
                                        extraction_per_minute = (
                                            fleet_parametr_resource_extraction.extraction_per_minute + (
                                                element_pattern.param1 * amount_ship))
                                        FleetParametrResourceExtraction.objects.filter(fleet=fleet).update(
                                            extraction_per_minute=extraction_per_minute)
                                    else:
                                        fleet_parametr_resource_extraction = FleetParametrResourceExtraction(
                                            fleet=fleet,
                                            extraction_per_minute=element_pattern.param1 * amount_ship
                                        )
                                        fleet_parametr_resource_extraction.save()
                                    use_energy = use_energy + element_pattern.power_consuption

                                element_pattern = ModulePattern.objects.filter(id=ship_element.element_pattern_id,
                                                                               module_class=5, param3=1).first()
                                if element_pattern:
                                    fleet_parametr_build = FleetParametrBuildRepair.objects.filter(fleet=fleet,
                                                                                                   class_process=1).first()
                                    if fleet_parametr_build:
                                        new_process_per_minute = fleet_parametr_build.process_per_minute + \
                                                                 element_pattern.param2 * amount_ship
                                        FleetParametrBuildRepair.objects.filter(fleet=fleet, class_process=1).update(
                                            process_per_minute=new_process_per_minute)
                                    else:
                                        fleet_parametr_build = FleetParametrBuildRepair(
                                            fleet=fleet,
                                            class_process=1,
                                            process_per_minute=element_pattern.param2 * amount_ship
                                        )
                                        fleet_parametr_build.save()

                                element_pattern = ModulePattern.objects.filter(id=ship_element.element_pattern_id,
                                                                               module_class=5, param3=2).first()
                                if element_pattern:
                                    fleet_parametr_repair = FleetParametrBuildRepair.objects.filter(fleet=fleet,
                                                                                                    class_process=2).first()
                                    if fleet_parametr_repair:
                                        new_process_per_minute = fleet_parametr_repair.process_per_minute + \
                                                                 element_pattern.param2 * amount_ship
                                        FleetParametrBuildRepair.objects.filter(fleet=fleet, class_process=2).update(
                                            process_per_minute=new_process_per_minute)
                                    else:
                                        fleet_parametr_repair = FleetParametrBuildRepair(
                                            fleet=fleet,
                                            class_process=2,
                                            process_per_minute=element_pattern.param2 * amount_ship
                                        )
                                        fleet_parametr_repair.save()

                                element_pattern = ModulePattern.objects.filter(id=ship_element.element_pattern_id,
                                                                               module_class=6).first()
                                if element_pattern:
                                    fleet_parametr_scan = FleetParametrScan(
                                        fleet=fleet,
                                        method_scanning=element_pattern.param3,
                                        time_scanning=element_pattern.param2,
                                        range_scanning=element_pattern.param1
                                    )
                                    fleet_parametr_scan.save()
                                    use_energy = use_energy + element_pattern.power_consuption

                        fuel_tank = ship.project_ship.hull_pattern.fuel_tank
                        hold = hold + ship.project_ship.hull_pattern.hold_size
                        use_energy *= amount_ship
                        use_fuel_system *= amount_ship
                        use_fuel_intersystem *= amount_ship
                        use_energy_giper *= amount_ship
                        use_energy_null *= amount_ship
                        use_fuel_generator *= amount_ship
                        produced_energy *= amount_ship

                        if ship_fleet:
                            if int(ship.amount_ship) == int(amount_ship):
                                new_amount = int(ship_fleet.amount_ship) + int(amount_ship)
                                Ship.objects.filter(project_ship=ship.project_ship, user=session_user, fleet_status=1,
                                                    place_id=fleet.id).update(amount_ship=new_amount)
                                Ship.objects.filter(id=ship_id, user=session_user, fleet_status=0,
                                                    place_id=session_user_city.id).delete()

                                ship = Ship.objects.filter(place_id=fleet.id, fleet_status=1, user=session_user).first()
                                project_ship = ProjectShip.objects.filter(id=ship.project_ship).first()

                                system_power = int(project_ship.system_power) * amount_ship + int(
                                    fleet_engine.system_power)
                                intersystem_power = int(
                                    project_ship.intersystem_power) * amount_ship + int(fleet_engine.intersystem_power)
                                giper_power = int(project_ship.giper_power) * amount_ship + int(
                                    fleet_engine.giper_power)
                                giper_accuracy = int(project_ship.giper_accuracy) * amount_ship + int(
                                    fleet_engine.giper_accuracy)
                                null_power = int(project_ship.null_power) * amount_ship + int(fleet_engine.null_power)
                                null_accuracy = int(project_ship.null_accuracy) * amount_ship + int(
                                    fleet_engine.null_accuracy)
                                ship_empty_mass = int(project_ship.mass) * amount_ship + int(fleet.ship_empty_mass)
                                hold_empty = hold * amount_ship + int(fleet.empty_hold)
                                hold = hold * amount_ship + int(fleet.hold)
                                free_fuel_tank = fuel_tank * amount_ship + int(fleet.free_fuel_tank)
                                fuel_tank = fuel_tank * amount_ship + int(fleet.fuel_tank)

                                use_energy += fleet_energy_power.use_energy
                                use_fuel_system += fleet_energy_power.use_fuel_system
                                use_fuel_intersystem += fleet_energy_power.use_fuel_intersystem
                                use_energy_giper += fleet_energy_power.use_energy_giper
                                use_energy_null += fleet_energy_power.use_energy_null
                                use_fuel_generator += fleet_energy_power.use_fuel_generator
                                produced_energy += fleet_energy_power.produce_energy

                                Fleet.objects.filter(id=fleet.id).update(
                                    ship_empty_mass=ship_empty_mass,
                                    hold=hold,
                                    empty_hold=hold_empty,
                                    fuel_tank=fuel_tank,
                                    free_fuel_tank=free_fuel_tank,
                                )

                                FleetEngine.objects.filter(fleet=fleet).update(
                                    system_power=system_power,
                                    intersystem_power=intersystem_power,
                                    giper_power=giper_power,
                                    giper_accuracy=giper_accuracy,
                                    null_power=null_power,
                                    null_accuracy=null_accuracy,
                                )

                                FleetEnergyPower.objects.filter(fleet=fleet).update(
                                    use_energy=use_energy,
                                    use_fuel_system=use_fuel_system,
                                    use_fuel_intersystem=use_fuel_intersystem,
                                    use_energy_giper=use_energy_giper,
                                    use_energy_null=use_energy_null,
                                    use_fuel_generator=use_fuel_generator,
                                    produce_energy=produced_energy)
                            else:
                                new_amount = int(ship_fleet.amount_ship) + int(amount_ship)
                                setattr(ship_fleet, 'amount_ship', new_amount)
                                ship_fleet.save()

                                ship = Ship.objects.filter(id=ship_id, user=session_user, fleet_status=0,
                                                           place_id=session_user_city.id).first()
                                new_amount = int(ship.amount_ship) - int(amount_ship)
                                setattr(ship, 'amount_ship', new_amount)
                                ship.save()

                                ship = Ship.objects.filter(place_id=fleet.id, fleet_status=1, user=session_user).first()

                                system_power = int(ship.project_ship.system_power) * amount_ship + int(
                                    fleet_engine.system_power)
                                intersystem_power = int(ship.project_ship.intersystem_power) * amount_ship + int(
                                    fleet_engine.intersystem_power)
                                giper_power = int(ship.project_ship.giper_power) * amount_ship + int(
                                    fleet_engine.giper_power)
                                giper_accuracy = int(ship.project_ship.giper_accuracy) * amount_ship + int(
                                    fleet_engine.giper_accuracy)
                                null_power = int(ship.project_ship.null_power) * amount_ship + int(
                                    fleet_engine.null_power)
                                null_accuracy = int(ship.project_ship.null_accuracy) * amount_ship + int(
                                    fleet_engine.null_accuracy)

                                ship_empty_mass = int(ship.project_ship.ship_mass) * (
                                    amount_ship) + int(fleet.ship_empty_mass)
                                hold_empty = hold * amount_ship + int(fleet.empty_hold)
                                hold = hold * amount_ship + int(fleet.fleet_hold)
                                free_fuel_tank = fuel_tank * amount_ship + int(fleet.free_fuel_tank)
                                fuel_tank = fuel_tank * amount_ship + int(fleet.fuel_tank)
                                use_energy = use_energy + fleet_energy_power.use_energy
                                use_fuel_system = use_fuel_system + fleet_energy_power.use_fuel_system
                                use_fuel_intersystem = use_fuel_intersystem + fleet_energy_power.use_fuel_intersystem
                                use_energy_giper = use_energy_giper + fleet_energy_power.use_energy_giper
                                use_energy_null = use_energy_null + fleet_energy_power.use_energy_null
                                use_fuel_generator = use_fuel_generator + fleet_energy_power.use_fuel_generator
                                produced_energy = produced_energy + fleet_energy_power.produce_energy
                                fleet_upd = Fleet.objects.filter(id=fleet.id).first()
                                setattr(fleet_upd, 'ship_empty_mass', ship_empty_mass)
                                setattr(fleet_upd, 'fleet_hold', hold)
                                setattr(fleet_upd, 'empty_hold', hold_empty)
                                setattr(fleet_upd, 'fuel_tank', fuel_tank)
                                setattr(fleet_upd, 'free_fuel_tank', free_fuel_tank)
                                fleet_upd.save()

                                FleetEngine.objects.filter(fleet=fleet).update(
                                    system_power=system_power,
                                    intersystem_power=intersystem_power,
                                    giper_power=giper_power,
                                    giper_accuracy=giper_accuracy,
                                    null_power=null_power,
                                    null_accuracy=null_accuracy,
                                )

                                FleetEnergyPower.objects.filter(fleet=fleet).update(
                                    use_energy=use_energy, use_fuel_system=use_fuel_system,
                                    use_fuel_intersystem=use_fuel_intersystem, use_energy_giper=use_energy_giper,
                                    use_energy_null=use_energy_null, use_fuel_generator=use_fuel_generator,
                                    produce_energy=produced_energy
                                )
                                message = 'Корабли добавлено во флот'
                        else:
                            if int(ship.amount_ship) == int(amount_ship):
                                Ship.objects.filter(id=ship_id, user=session_user, fleet_status=0,
                                                    place_id=session_user_city).update(fleet_status=1,
                                                                                       place_id=fleet.id)
                                ship = Ship.objects.filter(id=ship_id).first()
                                ship_in_fleet = Ship.objects.filter(place_id=fleet.id).first()
                                if ship_in_fleet:
                                    hold_empty = fleet.empty_hold + hold * amount_ship
                                    hold = fleet.hold + hold * amount_ship
                                    free_fuel_tank = fuel_tank * amount_ship + int(fleet.free_fuel_tank)
                                    fuel_tank = fuel_tank * amount_ship + int(fleet.fuel_tank)
                                    ship_empty_mass = fleet.ship_empty_mass + ship.project_ship.mass * amount_ship

                                    system_power = fleet_engine.system_power + int(
                                        ship.project_ship.system_power) * amount_ship
                                    intersystem_power = fleet_engine.intersystem_power + int(
                                        ship.project_ship.intersystem_power) * amount_ship
                                    giper_power = fleet_engine.giper_power + int(
                                        ship.project_ship.giper_power) * amount_ship
                                    null_power = fleet_engine.null_power + int(
                                        ship.project_ship.null_power) * amount_ship
                                else:
                                    hold_empty = hold * amount_ship
                                    hold *= amount_ship
                                    free_fuel_tank = fuel_tank * amount_ship
                                    fuel_tank *= amount_ship
                                    ship_empty_mass = ship.project_ship.mass * amount_ship
                                    system_power = int(ship.project_ship.system_power) * amount_ship
                                    intersystem_power = int(ship.project_ship.intersystem_power) * amount_ship
                                    giper_power = int(ship.project_ship.giper_power) * amount_ship
                                    null_power = int(ship.project_ship.null_power) * amount_ship

                                FleetEngine.objects.filter(fleet=fleet).update(
                                    system_power=system_power,
                                    intersystem_power=intersystem_power,
                                    giper_power=giper_power,
                                    giper_accuracy=int(ship.project_ship.giper_accuracy) * amount_ship,
                                    null_power=null_power,
                                    null_accuracy=int(ship.project_ship.null_accuracy) * amount_ship,
                                )
                                fleet_upd = Fleet.objects.filter(id=fleet.id).first()
                                setattr(fleet_upd, 'ship_empty_mass', ship_empty_mass)
                                setattr(fleet_upd, 'fleet_hold', hold)
                                setattr(fleet_upd, 'empty_hold', hold_empty)
                                setattr(fleet_upd, 'fuel_tank', fuel_tank)
                                setattr(fleet_upd, 'free_fuel_tank', free_fuel_tank)
                                fleet_upd.save()

                                FleetEnergyPower.objects.filter(fleet=fleet).update(
                                    use_energy=use_energy, use_fuel_system=use_fuel_system,
                                    use_fuel_intersystem=use_fuel_intersystem, use_energy_giper=use_energy_giper,
                                    use_energy_null=use_energy_null, use_fuel_generator=use_fuel_generator,
                                    produce_energy=produced_energy
                                )
                            else:
                                ship = Ship(
                                    user=session_user,
                                    project_ship=ship.project_ship,
                                    amount_ship=amount_ship,
                                    fleet_status=1,
                                    place_id=fleet.id,
                                    ship_name=ship.ship_name
                                )
                                ship.save()
                                ship = Ship.objects.filter(id=ship_id, user=session_user, fleet_status=0,
                                                           place_id=session_user_city.id).first()
                                new_amount = int(ship.amount_ship) - int(amount_ship)
                                Ship.objects.filter(id=ship_id, user=session_user, fleet_status=0,
                                                    place_id=session_user_city.id).update(amount_ship=new_amount)
                                ship = Ship.objects.filter(id=ship_id, user=session_user, fleet_status=0,
                                                           place_id=session_user_city.id).first()
                                project_ship = ProjectShip.objects.filter(id=ship.project_ship.id).first()
                                ship_in_fleet = Ship.objects.filter(place_id=fleet.id).first()

                                if ship_in_fleet:
                                    hold_empty = fleet.empty_hold + hold * amount_ship
                                    hold = fleet.fleet_hold + hold * amount_ship
                                    free_fuel_tank = fuel_tank * amount_ship + int(fleet.free_fuel_tank)
                                    fuel_tank = fuel_tank * amount_ship + int(fleet.fuel_tank)
                                    ship_empty_mass = fleet.ship_empty_mass + project_ship.ship_mass * amount_ship

                                    system_power = fleet_engine.system_power + int(
                                        project_ship.system_power) * amount_ship
                                    intersystem_power = fleet_engine.intersystem_power + int(
                                        project_ship.intersystem_power) * amount_ship
                                    giper_power = fleet_engine.giper_power + int(project_ship.giper_power) * amount_ship
                                    null_power = fleet_engine.null_power + int(project_ship.null_power) * amount_ship
                                else:
                                    hold_empty = hold * amount_ship
                                    hold *= amount_ship
                                    free_fuel_tank = fuel_tank * amount_ship
                                    fuel_tank *= amount_ship
                                    ship_empty_mass = project_ship.mass * amount_ship
                                    system_power = int(project_ship.system_power) * amount_ship
                                    intersystem_power = int(project_ship.intersystem_power) * amount_ship
                                    giper_power = int(project_ship.giper_power) * amount_ship
                                    null_power = int(project_ship.null_power) * amount_ship

                                FleetEngine.objects.filter(fleet=fleet).update(
                                    system_power=system_power,
                                    intersystem_power=intersystem_power,
                                    giper_power=giper_power,
                                    giper_accuracy=int(project_ship.giper_accuracy) * amount_ship,
                                    null_power=null_power,
                                    null_accuracy=int(project_ship.null_accuracy) * amount_ship,
                                )
                                fleet_upd = Fleet.objects.filter(id=fleet.id).first()
                                setattr(fleet_upd, 'ship_empty_mass', ship_empty_mass)
                                setattr(fleet_upd, 'fleet_hold', hold)
                                setattr(fleet_upd, 'empty_hold', hold_empty)
                                setattr(fleet_upd, 'fuel_tank', fuel_tank)
                                setattr(fleet_upd, 'free_fuel_tank', free_fuel_tank)
                                fleet_upd.save()

                                FleetEnergyPower.objects.filter(fleet=fleet).update(
                                    use_energy=use_energy, use_fuel_system=use_fuel_system,
                                    use_fuel_intersystem=use_fuel_intersystem, use_energy_giper=use_energy_giper,
                                    use_energy_null=use_energy_null, use_fuel_generator=use_fuel_generator,
                                    produce_energy=produced_energy
                                )
                            message = 'Корабли добавлено во флот'
                    else:
                        message = 'Недостаточно корблей'
                else:
                    message = 'Неверное количество кораблей'
            else:
                message = 'Флот не над планетой'

            request.session['user'] = session_user.id
            request.session['user_city'] = session_user_city.id
            request.session['live'] = True
            output = ship_output(session_user, session_user_city, fleet, flightplans, flightplan_flights,
                                 warehouse_factorys,
                                 command, message)
            return render(request, "space_forces.html", output)
        else:
            message = 'Error'
            user_citys = UserCity.objects.filter(user=session_user).all()
            user_fleets = Fleet.objects.filter(user=session_user).all()
            ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city.id).all()
            ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1).all()
            command = 0
            output = {'user': session_user, 'warehouses': session_user_city.warehouse,
                      'user_city': session_user_city, 'user_citys': user_citys, 'user_fleets': user_fleets,
                      'ships': ships, 'ship_fleets': ship_fleets, 'command': command, 'message': message}
            return render(request, "space_forces.html", output)


def ship_output(*args):
    session_user = args[0]
    session_user_city = args[1]
    fleet = args[2]
    flightplans = args[3]
    flightplan_flights = args[4]
    warehouse_factorys = args[5]
    command = args[6]
    message = args[7]

    warehouse = session_user_city.warehouse
    user_citys = UserCity.objects.filter(user=session_user).all()
    user_fleets = Fleet.objects.filter(user=session_user).all()
    ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city.id).all()
    add_ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city.id).all()
    ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1).all()

    return {'user': session_user, 'warehouse': warehouse, 'user_city': session_user_city, 'user_citys': user_citys,
            'user_fleets': user_fleets, 'add_ships': add_ships, 'fleet_id': fleet.id,
            'ship_fleets': ship_fleets, 'ships': ships, 'fleet': fleet,
            'command': command, 'flightplans': flightplans, 'flightplan_flights': flightplan_flights,
            'warehouse_factorys': warehouse_factorys, 'message': message}
