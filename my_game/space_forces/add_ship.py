# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, User_city
from my_game.models import Warehouse
from my_game.models import Hull_pattern, Project_ship, Element_ship, Module_pattern, Engine_pattern, Generator_pattern, \
    Shield_pattern, Weapon_pattern
from my_game.models import Project_ship, Ship, Fleet, Fleet_parametr_scan, Fleet_engine, Fleet_energy_power, \
    Fleet_parametr_resource_extraction, Fleet_parametr_build_repair
from my_game import function


def add_ship(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        add_ships = {}
        flightplans = {}
        flightplan_flights = {}
        warehouse_factorys = {}
        warehouse_elements = {}
        command = 1
        hold = 0
        fuel_tank = 0
        passive_scan = 0
        active_scan = 0
        giper_scan = 0
        message = 'Hui'
        ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1)
        full_request = request.POST
        myDict = dict(full_request.iterlists())

        amount_ship_dict = myDict.get('amount_ship')
        fleet_id_dict = myDict.get('hidden_fleet')
        ship_id_dict = myDict.get('hidden_ship')
        len_amount_ship_dict = len(amount_ship_dict)
        for i in range(len_amount_ship_dict):
            if int(amount_ship_dict[i]) != 0:
                amount_ship = int(amount_ship_dict[i])
                fleet_id = int(fleet_id_dict[i])
                ship_id = int(ship_id_dict[i])

        ship = Ship.objects.filter(id=ship_id, user=session_user, fleet_status=0,
                                   place_id=session_user_city).first()
        fleet = Fleet.objects.filter(id=fleet_id).first()
        fleet_engine = Fleet_engine.objects.filter(fleet_id=fleet_id).first()
        fleet_energy_power = Fleet_energy_power.objects.filter(fleet_id=fleet_id).first()
        if fleet.status == 0 and fleet.planet == session_user_city:
            if amount_ship > 0:
                if int(ship.amount_ship) >= int(amount_ship):
                    ship_fleet = Ship.objects.filter(id_project_ship=ship.id_project_ship, user=session_user,
                                                     fleet_status=1, place_id=fleet_id).first()
                    ship_pattern = Project_ship.objects.filter(id=ship.id_project_ship).first()
                    hull_pattern = Hull_pattern.objects.filter(id=ship_pattern.hull_id).first()
                    ship_elements = Element_ship.objects.filter(id_project_ship=ship.id_project_ship)
                    use_energy = hull_pattern.power_consuption
                    use_fuel_system = 0
                    use_fuel_intersystem = 0
                    use_energy_giper = 0
                    use_energy_null = 0
                    use_fuel_generator = 0
                    produced_energy = 0
                    for ship_element in ship_elements:
                        if ship_element.class_element == 3:
                            element_pattern = Shield_pattern.objects.filter(id=ship_element.id_element_pattern).first()
                            use_energy = use_energy + element_pattern.power_consuption

                        if ship_element.class_element == 4:
                            engine_pattern = Engine_pattern.objects.filter(id=ship_element.id_element_pattern).first()
                            if engine_pattern.system_power != 0:
                                use_fuel_system = use_fuel_system + engine_pattern.power_consuption
                            if engine_pattern.intersystem_power != 0:
                                use_fuel_intersystem = use_fuel_intersystem + engine_pattern.power_consuption
                            if engine_pattern.giper_power != 0:
                                use_energy_giper = use_energy_giper + engine_pattern.power_consuption
                            if engine_pattern.nullT_power != 0:
                                use_energy_null = use_energy_null + engine_pattern.power_consuption

                        if ship_element.class_element == 5:
                            element_pattern = Generator_pattern.objects.filter(
                                id=ship_element.id_element_pattern).first()
                            use_fuel_generator = use_fuel_generator + element_pattern.fuel_necessary
                            produced_energy = produced_energy + element_pattern.produced_energy

                        if ship_element.class_element == 6:
                            element_pattern = Weapon_pattern.objects.filter(id=ship_element.id_element_pattern).first()
                            use_energy = use_energy + element_pattern.power_consuption

                        if ship_element.class_element == 7:
                            element_pattern = Weapon_pattern.objects.filter(id=ship_element.id_element_pattern).first()
                            use_energy = use_energy + element_pattern.power_consuption

                        if ship_element.class_element == 8:
                            element_pattern = Module_pattern.objects.filter(id=ship_element.id_element_pattern,
                                                                            module_class=2).first()
                            if element_pattern:
                                hold = hold + element_pattern.param1
                                use_energy = use_energy + element_pattern.power_consuption

                            element_pattern = Module_pattern.objects.filter(id=ship_element.id_element_pattern,
                                                                            module_class=3).first()
                            if element_pattern:
                                fleet_parametr_resource_extraction = Fleet_parametr_resource_extraction.objects.filter(
                                    fleet_id=fleet_id).first()
                                if fleet_parametr_resource_extraction:
                                    extraction_per_minute = fleet_parametr_resource_extraction.extraction_per_minute + element_pattern.param1 * amount_ship
                                    fleet_parametr_resource_extraction = Fleet_parametr_resource_extraction.objects.filter(
                                        fleet_id=fleet_id).update(extraction_per_minute=extraction_per_minute)
                                else:
                                    fleet_parametr_resource_extraction = Fleet_parametr_resource_extraction(
                                        fleet_id=fleet_id,
                                        extraction_per_minute=element_pattern.param1 * amount_ship
                                    )
                                    fleet_parametr_resource_extraction.save()
                                use_energy = use_energy + element_pattern.power_consuption

                            element_pattern = Module_pattern.objects.filter(id=ship_element.id_element_pattern,
                                                                            module_class=5, param3=1).first()
                            if element_pattern:
                                fleet_parametr_build = Fleet_parametr_build_repair.objects.filter(fleet_id=fleet_id,
                                                                                                  class_process=1).first()
                                if fleet_parametr_build:
                                    new_process_per_minute = fleet_parametr_build.process_per_minute + element_pattern.param2 * amount_ship
                                    fleet_parametr_build = Fleet_parametr_build_repair.objects.filter(fleet_id=fleet_id,
                                                                                                      class_process=1).update(
                                        process_per_minute=new_process_per_minute)
                                else:
                                    fleet_parametr_build = Fleet_parametr_build_repair(
                                        fleet_id=fleet_id,
                                        class_process=1,
                                        process_per_minute=element_pattern.param2 * amount_ship
                                    )
                                    fleet_parametr_build.save()

                            element_pattern = Module_pattern.objects.filter(id=ship_element.id_element_pattern,
                                                                            module_class=5, param3=2).first()
                            if element_pattern:
                                fleet_parametr_repair = Fleet_parametr_build_repair.objects.filter(fleet_id=fleet_id,
                                                                                                   class_process=2).first()
                                if fleet_parametr_repair:
                                    new_process_per_minute = fleet_parametr_repair.process_per_minute + element_pattern.param2 * amount_ship
                                    fleet_parametr_repair = Fleet_parametr_build_repair.objects.filter(
                                        fleet_id=fleet_id,
                                        class_process=2).update(
                                        process_per_minute=new_process_per_minute)
                                else:
                                    fleet_parametr_repair = Fleet_parametr_build_repair(
                                        fleet_id=fleet_id,
                                        class_process=2,
                                        process_per_minute=element_pattern.param2 * amount_ship
                                    )
                                    fleet_parametr_repair.save()

                            element_pattern = Module_pattern.objects.filter(id=ship_element.id_element_pattern,
                                                                            module_class=6).first()
                            if element_pattern:
                                fleet_parametr_scan = Fleet_parametr_scan(
                                    fleet_id=fleet_id,
                                    method_scanning=element_pattern.param3,
                                    time_scanning=element_pattern.param2,
                                    range_scanning=element_pattern.param1
                                )
                                fleet_parametr_scan.save()
                                use_energy = use_energy + element_pattern.power_consuption

                    fuel_tank = hull_pattern.fuel_tank
                    hold = hold + hull_pattern.hold_size
                    use_energy = use_energy * amount_ship
                    use_fuel_system = use_fuel_system * amount_ship
                    use_fuel_intersystem = use_fuel_intersystem * amount_ship
                    use_energy_giper = use_energy_giper * amount_ship
                    use_energy_null = use_energy_null * amount_ship
                    use_fuel_generator = use_fuel_generator * amount_ship
                    produced_energy = produced_energy * amount_ship

                    if ship_fleet:
                        if int(ship.amount_ship) == int(amount_ship):
                            new_amount = int(ship_fleet.amount_ship) + int(amount_ship)
                            ship_fleet = Ship.objects.filter(id_project_ship=ship.id_project_ship, user=session_user,
                                                             fleet_status=1, place_id=fleet_id).update(
                                amount_ship=new_amount)
                            delete_ship = Ship.objects.filter(id=ship_id, user=session_user, fleet_status=0,
                                                              place_id=session_user_city).delete()

                            ship = Ship.objects.filter(place_id=fleet_id, fleet_status=1, user=session_user).first()
                            project_ship = Project_ship.objects.filter(id=ship.id_project_ship).first()

                            system_power = int(project_ship.system_power) * amount_ship + int(fleet_engine.system_power)
                            intersystem_power = int(
                                project_ship.intersystem_power) * amount_ship + int(fleet_engine.intersystem_power)
                            giper_power = int(project_ship.giper_power) * amount_ship + int(fleet_engine.giper_power)
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

                            use_energy = use_energy + fleet_energy_power.use_energy
                            use_fuel_system = use_fuel_system + fleet_energy_power.use_fuel_system
                            use_fuel_intersystem = use_fuel_intersystem + fleet_energy_power.use_fuel_intersystem
                            use_energy_giper = use_energy_giper + fleet_energy_power.use_energy_giper
                            use_energy_null = use_energy_null + fleet_energy_power.use_energy_null
                            use_fuel_generator = use_fuel_generator + fleet_energy_power.use_fuel_generator
                            produced_energy = produced_energy + fleet_energy_power.produce_energy

                            fleet = Fleet.objects.filter(user=session_user, id=fleet_id).update(
                                ship_empty_mass=ship_empty_mass,
                                hold=hold,
                                empty_hold=hold_empty,
                                fuel_tank=fuel_tank,
                                free_fuel_tank=free_fuel_tank,
                            )

                            fleet_engine = Fleet_engine.objects.filter(fleet_id=fleet_id).update(
                                system_power=system_power,
                                intersystem_power=intersystem_power,
                                giper_power=giper_power,
                                giper_accuracy=giper_accuracy,
                                null_power=null_power,
                                null_accuracy=null_accuracy,
                            )

                            fleet_energy_power = Fleet_energy_power.objects.filter(fleet_id=fleet_id).update(
                                use_energy=use_energy, use_fuel_system=use_fuel_system,
                                use_fuel_intersystem=use_fuel_intersystem, use_energy_giper=use_energy_giper,
                                use_energy_null=use_energy_null, use_fuel_generator=use_fuel_generator,
                                produce_energy=produced_energy
                            )
                        else:
                            new_amount = int(ship_fleet.amount_ship) + int(amount_ship)
                            ship_fleet = Ship.objects.filter(id_project_ship=ship.id_project_ship, user=session_user,
                                                             fleet_status=1, place_id=fleet_id).update(
                                amount_ship=new_amount)
                            ship = Ship.objects.filter(id=ship_id, user=session_user, fleet_status=0,
                                                       place_id=session_user_city).first()
                            new_amount = int(ship.amount_ship) - int(amount_ship)
                            update_ship = Ship.objects.filter(id=ship_id, user=session_user, fleet_status=0,
                                                              place_id=session_user_city).update(amount_ship=new_amount)

                            ship = Ship.objects.filter(place_id=fleet_id, fleet_status=1, user=session_user).first()
                            project_ship = Project_ship.objects.filter(id=ship.id_project_ship).first()

                            system_power = int(project_ship.system_power) * amount_ship + int(fleet_engine.system_power)
                            intersystem_power = int(
                                project_ship.intersystem_power) * amount_ship + int(fleet_engine.intersystem_power)
                            giper_power = int(project_ship.giper_power) * amount_ship + int(fleet_engine.giper_power)
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
                            use_energy = use_energy + fleet_energy_power.use_energy
                            use_fuel_system = use_fuel_system + fleet_energy_power.use_fuel_system
                            use_fuel_intersystem = use_fuel_intersystem + fleet_energy_power.use_fuel_intersystem
                            use_energy_giper = use_energy_giper + fleet_energy_power.use_energy_giper
                            use_energy_null = use_energy_null + fleet_energy_power.use_energy_null
                            use_fuel_generator = use_fuel_generator + fleet_energy_power.use_fuel_generator
                            produced_energy = produced_energy + fleet_energy_power.produce_energy

                            fleet = Fleet.objects.filter(user=session_user, id=fleet_id).update(
                                ship_empty_mass=ship_empty_mass,
                                hold=hold,
                                empty_hold=hold_empty,
                                fuel_tank=fuel_tank,
                                free_fuel_tank=free_fuel_tank
                            )

                            fleet_engine = Fleet_engine.objects.filter(fleet_id=fleet_id).update(
                                system_power=system_power,
                                intersystem_power=intersystem_power,
                                giper_power=giper_power,
                                giper_accuracy=giper_accuracy,
                                null_power=null_power,
                                null_accuracy=null_accuracy,
                            )

                            fleet_energy_power = Fleet_energy_power.objects.filter(fleet_id=fleet_id).update(
                                use_energy=use_energy, use_fuel_system=use_fuel_system,
                                use_fuel_intersystem=use_fuel_intersystem, use_energy_giper=use_energy_giper,
                                use_energy_null=use_energy_null, use_fuel_generator=use_fuel_generator,
                                produce_energy=produced_energy
                            )
                            message = 'Корабли добавлено во флот'
                    else:
                        if int(ship.amount_ship) == int(amount_ship):
                            ship = Ship.objects.filter(id=ship_id, user=session_user, fleet_status=0,
                                                       place_id=session_user_city).update(fleet_status=1,
                                                                                          place_id=fleet_id)
                            ship = Ship.objects.filter(id=ship_id).first()
                            project_ship = Project_ship.objects.filter(id=ship.id_project_ship).first()
                            ship_in_fleet = Ship.objects.filter(place_id=fleet_id).first()
                            if ship_in_fleet:
                                hold_empty = fleet.empty_hold + hold * amount_ship
                                hold = fleet.hold + hold * amount_ship
                                free_fuel_tank = fuel_tank * amount_ship + int(fleet.free_fuel_tank)
                                fuel_tank = fuel_tank * amount_ship + int(fleet.fuel_tank)
                                ship_empty_mass = fleet.ship_empty_mass + project_ship.mass * amount_ship

                                system_power = fleet_engine.system_power + int(project_ship.system_power) * amount_ship
                                intersystem_power = fleet_engine.intersystem_power + int(
                                    project_ship.intersystem_power) * amount_ship
                                giper_power = fleet_engine.giper_power + int(project_ship.giper_power) * amount_ship
                                null_power = fleet_engine.null_power + int(project_ship.null_power) * amount_ship
                            else:
                                hold_empty = hold * amount_ship
                                hold = hold * amount_ship
                                free_fuel_tank = fuel_tank * amount_ship
                                fuel_tank = fuel_tank * amount_ship
                                ship_empty_mass = project_ship.mass * amount_ship
                                system_power = int(project_ship.system_power) * amount_ship
                                intersystem_power = int(project_ship.intersystem_power) * amount_ship
                                giper_power = int(project_ship.giper_power) * amount_ship
                                null_power = int(project_ship.null_power) * amount_ship

                            fleet_engine = Fleet_engine.objects.filter(fleet_id=fleet_id).update(
                                system_power=system_power,
                                intersystem_power=intersystem_power,
                                giper_power=giper_power,
                                giper_accuracy=int(project_ship.giper_accuracy) * amount_ship,
                                null_power=null_power,
                                null_accuracy=int(project_ship.null_accuracy) * amount_ship,
                            )
                            fleet = Fleet.objects.filter(user=session_user, id=fleet_id).update(
                                ship_empty_mass=ship_empty_mass,
                                hold=hold,
                                empty_hold=hold_empty,
                                fuel_tank=fuel_tank,
                                free_fuel_tank=free_fuel_tank
                            )

                            fleet_energy_power = Fleet_energy_power.objects.filter(fleet_id=fleet_id).update(
                                use_energy=use_energy, use_fuel_system=use_fuel_system,
                                use_fuel_intersystem=use_fuel_intersystem, use_energy_giper=use_energy_giper,
                                use_energy_null=use_energy_null, use_fuel_generator=use_fuel_generator,
                                produce_energy=produced_energy
                            )
                        else:
                            ship = Ship(
                                user=session_user,
                                id_project_ship=ship.id_project_ship,
                                amount_ship=amount_ship,
                                fleet_status=1,
                                place_id=fleet_id,
                                name=ship.name
                            )
                            ship.save()
                            ship = Ship.objects.filter(id=ship_id, user=session_user, fleet_status=0,
                                                       place_id=session_user_city).first()
                            new_amount = int(ship.amount_ship) - int(amount_ship)
                            ship = Ship.objects.filter(id=ship_id, user=session_user, fleet_status=0,
                                                       place_id=session_user_city).update(amount_ship=new_amount)
                            ship = Ship.objects.filter(id=ship_id, user=session_user, fleet_status=0,
                                                       place_id=session_user_city).first()
                            project_ship = Project_ship.objects.filter(id=ship.id_project_ship).first()
                            ship_in_fleet = Ship.objects.filter(place_id=fleet_id).first()

                            if ship_in_fleet:
                                hold_empty = fleet.empty_hold + hold * amount_ship
                                hold = fleet.hold + hold * amount_ship
                                free_fuel_tank = fuel_tank * amount_ship + int(fleet.free_fuel_tank)
                                fuel_tank = fuel_tank * amount_ship + int(fleet.fuel_tank)
                                ship_empty_mass = fleet.ship_empty_mass + project_ship.mass * amount_ship

                                system_power = fleet_engine.system_power + int(project_ship.system_power) * amount_ship
                                intersystem_power = fleet_engine.intersystem_power + int(
                                    project_ship.intersystem_power) * amount_ship
                                giper_power = fleet_engine.giper_power + int(project_ship.giper_power) * amount_ship
                                null_power = fleet_engine.null_power + int(project_ship.null_power) * amount_ship
                            else:
                                hold_empty = hold * amount_ship
                                hold = hold * amount_ship
                                free_fuel_tank = fuel_tank * amount_ship
                                fuel_tank = fuel_tank * amount_ship
                                ship_empty_mass = project_ship.mass * amount_ship
                                system_power = int(project_ship.system_power) * amount_ship
                                intersystem_power = int(project_ship.intersystem_power) * amount_ship
                                giper_power = int(project_ship.giper_power) * amount_ship
                                null_power = int(project_ship.null_power) * amount_ship

                            fleet_engine = Fleet_engine.objects.filter(fleet_id=fleet_id).update(
                                system_power=system_power,
                                intersystem_power=intersystem_power,
                                giper_power=giper_power,
                                giper_accuracy=int(project_ship.giper_accuracy) * amount_ship,
                                null_power=null_power,
                                null_accuracy=int(project_ship.null_accuracy) * amount_ship,
                            )
                            fleet = Fleet.objects.filter(user=session_user, id=fleet_id).update(
                                ship_empty_mass=ship_empty_mass,
                                hold=hold,
                                empty_hold=hold_empty,
                                fuel_tank=fuel_tank,
                                free_fuel_tank=free_fuel_tank
                            )

                            fleet_energy_power = Fleet_energy_power.objects.filter(fleet_id=fleet_id).update(
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

        ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1)

        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('id_resource')
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = User_city.objects.filter(user=int(session_user))
        user_fleets = Fleet.objects.filter(user=session_user)
        ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city)
        add_ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city)
        ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1)
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouses': warehouses, 'user_city': user_city, 'user_citys': user_citys,
                  'user_fleets': user_fleets, 'add_ships': add_ships, 'fleet_id': fleet_id,
                  'ship_fleets': ship_fleets, 'ships': ships, 'fleet': fleet,
                  'command': command, 'flightplans': flightplans, 'flightplan_flights': flightplan_flights,
                  'warehouse_factorys': warehouse_factorys, 'message': message}
        return render(request, "space_forces.html", output)