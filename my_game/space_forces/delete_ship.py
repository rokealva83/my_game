# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import ElementShip, ModulePattern, GeneratorPattern, EnginePattern, \
    WeaponPattern, ShieldPattern
from my_game.models import MyUser, UserCity
from my_game.models import ProjectShip, Ship, Fleet, FleetParametrScan, FleetEnergyPower, FleetEngine, \
    FleetParametrResourceExtraction, FleetParametrBuildRepair

from my_game import function


def delete_ship(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        function.check_all_queues(session_user)
        flightplans = flightplan_flights = warehouse_factorys = {}
        fleet_id = ship_id = command = hold = fuel_tank = 0
        message = 'Корабль уже не приписан к флоту'

        full_request = request.POST
        my_dictionary = dict(full_request.iterlists())
        amount_ship_dict = my_dictionary.get('amount_ship')
        fleet_id_dict = my_dictionary.get('hidden_fleet')
        ship_id_dict = my_dictionary.get('hidden_del_ship')
        len_amount_ship_dict = len(amount_ship_dict)
        for i in range(len_amount_ship_dict):
            if int(amount_ship_dict[i]) != 0:
                amount_ship = int(amount_ship_dict[i])
                fleet_id = int(fleet_id_dict[i])
                ship_id = int(ship_id_dict[i])

        fleet = Fleet.objects.filter(id=fleet_id).first()
        user_city = UserCity.objects.filter(user=session_user, x=fleet.x, y=fleet.y, z=fleet.z).first()
        if user_city:
            if fleet.hold == fleet.empty_hold:
                fleet_engine = FleetEngine.objects.filter(fleet=fleet).first()
                fleet_energy_power = FleetEnergyPower.objects.filter(fleet=fleet).first()
                project_ship = ProjectShip.objects.filter(id=ship_id).first()
                ship = Ship.objects.filter(user=session_user, project_ship=project_ship, place_id=fleet.id,
                                           fleet_status=1).first()
                ship_elements = ElementShip.objects.filter(id_project_ship=ship.id_project_ship)
                use_energy = project_ship.hull_pattern.power_consuption
                use_fuel_system = use_fuel_intersystem = use_energy_giper = use_energy_null = use_fuel_generator = 0
                produced_energy = 0
                for ship_element in ship_elements:
                    if ship_element.class_element == 3:
                        element_pattern = ShieldPattern.objects.filter(id=ship_element.element_pattern_id).first()
                        use_energy = use_energy + element_pattern.power_consuption

                    if ship_element.class_element == 4:
                        engine_pattern = EnginePattern.objects.filter(id=ship_element.element_pattern_id).first()
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
                        element_pattern = WeaponPattern.objects.filter(id=ship_element.element_pattern_id).first()
                        use_energy = use_energy + element_pattern.power_consuption

                    if ship_element.class_element == 7:
                        element_pattern = WeaponPattern.objects.filter(id=ship_element.element_pattern_id).first()
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
                            use_energy = use_energy + element_pattern.power_consuption
                            extraction_per_minute = fleet_parametr_resource_extraction.extraction_per_minute - \
                                                    element_pattern.param1 * amount_ship
                            FleetParametrResourceExtraction.objects.filter(fleet=fleet).update(
                                extraction_per_minute=extraction_per_minute)

                        element_pattern = ModulePattern.objects.filter(id=ship_element.element_pattern_id,
                                                                       module_class=5, param3=1).first()
                        if element_pattern:
                            fleet_parametr_build = FleetParametrBuildRepair.objects.filter(fleet=fleet,
                                                                                           class_process=1).first()
                            new_process_per_minute = fleet_parametr_build.process_per_minute -\
                                                     element_pattern.param2 * amount_ship
                            if new_process_per_minute == 0:
                                FleetParametrBuildRepair.objects.filter(fleet=fleet, class_process=1).delete()
                            else:
                                FleetParametrBuildRepair.objects.filter(fleet=fleet, class_process=1).update(
                                    process_per_minute=new_process_per_minute)

                        element_pattern = ModulePattern.objects.filter(id=ship_element.element_pattern_id,
                                                                       module_class=5, param3=2).first()
                        if element_pattern:
                            fleet_parametr_repqair = FleetParametrBuildRepair.objects.filter(fleet=fleet,
                                                                                             class_process=2).first()
                            new_process_per_minute = fleet_parametr_repqair.process_per_minute - \
                                                     element_pattern.param2 * amount_ship
                            if new_process_per_minute == 0:
                                FleetParametrBuildRepair.objects.filter(fleet=fleet,
                                                                        class_process=2).delete()
                            else:
                                FleetParametrBuildRepair.objects.filter(fleet=fleet,
                                                                        class_process=2).update(
                                    process_per_minute=new_process_per_minute)

                        element_pattern = ModulePattern.objects.filter(id=ship_element.element_pattern_id,
                                                                       module_class=6).first()
                        if element_pattern:
                            if amount_ship == ship.amount_ship:
                                FleetParametrScan.objects.filter(fleet=fleet,
                                                                 time_scanning=element_pattern.param2,
                                                                 method_scanning=element_pattern.param3,
                                                                 range_scanning=element_pattern.param1).delete()
                            use_energy = use_energy + element_pattern.power_consuption

                hold = hold + project_ship.hull_pattern.hold_size
                fuel_tank = fuel_tank + project_ship.hull_pattern.fuel_tank
                use_energy *= amount_ship
                use_fuel_system *= amount_ship
                use_fuel_intersystem *= amount_ship
                use_energy_giper *= amount_ship
                use_energy_null *= amount_ship
                use_fuel_generator *= amount_ship
                produced_energy *= amount_ship

                ship = Ship.objects.filter(user=session_user, project_ship=project_ship, place_id=session_user_city.id,
                                           fleet_status=0).first()
                if ship:
                    new_amount = int(ship.amount_ship) + int(amount_ship)
                    Ship.objects.filter(user=session_user, project_ship=project_ship, place_id=user_city.id,
                                        fleet_status=0).update(amount_ship=new_amount)
                    ship = Ship.objects.filter(user=session_user, project_ship=project_ship, place_id=fleet.id,
                                               fleet_status=1).first()
                    new_amount = int(ship.amount_ship) - int(amount_ship)
                    if new_amount == 0:
                        Ship.objects.filter(user=session_user, project_ship=project_ship, place_id=fleet.id,
                                            fleet_status=1).delete()
                    else:
                        Ship.objects.filter(user=session_user, project_ship=project_ship, place_id=fleet.id,
                                            fleet_status=1).update(amount_ship=new_amount)

                    fleet = Fleet.objects.filter(user=session_user, id=fleet.id).first()

                    project_ship = ProjectShip.objects.filter(id=ship_id).first()

                    system_power = int(fleet_engine.system_power) - int(project_ship.system_power) * amount_ship
                    intersystem_power = int(fleet_engine.intersystem_power) - int(
                        project_ship.intersystem_power) * amount_ship
                    giper_power = int(fleet_engine.giper_power) - int(project_ship.giper_power) * amount_ship
                    giper_accuracy = int(fleet_engine.giper_accuracy) - int(project_ship.giper_accuracy) * amount_ship
                    null_power = int(fleet_engine.null_power) - int(project_ship.null_power) * amount_ship
                    null_accuracy = int(fleet_engine.null_accuracy) - int(project_ship.null_accuracy) * amount_ship
                    ship_empty_mass = int(fleet.ship_empty_mass) - int(project_ship.mass) * amount_ship
                    hold = int(fleet.hold) - hold * amount_ship
                    fuel_tank = int(fleet.fuel_tank) - fuel_tank * amount_ship
                    use_energy = fleet_energy_power.use_energy - use_energy
                    use_fuel_system = fleet_energy_power.use_fuel_system - use_fuel_system
                    use_fuel_intersystem = fleet_energy_power.use_fuel_intersystem - use_fuel_intersystem
                    use_energy_giper = fleet_energy_power.use_energy_giper - use_energy_giper
                    use_energy_null = fleet_energy_power.use_energy_null - use_energy_null
                    use_fuel_generator = fleet_energy_power.use_fuel_generator - use_fuel_generator
                    produced_energy = fleet_energy_power.produce_energy - produced_energy

                    fleet = Fleet.objects.filter(user=session_user, id=fleet.id).update(
                        ship_empty_mass=ship_empty_mass,
                        hold=hold,
                        empty_hold=hold,
                        fuel_tank=fuel_tank,
                        free_fuel_tank=fuel_tank
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
                        use_energy=use_energy, use_fuel_system=use_fuel_system,
                        use_fuel_intersystem=use_fuel_intersystem, use_energy_giper=use_energy_giper,
                        use_energy_null=use_energy_null, use_fuel_generator=use_fuel_generator,
                        produce_energy=produced_energy
                    )

                else:
                    project_ship = ProjectShip.objects.filter(id=ship_id).first()

                    ship = Ship(
                        user=session_user,
                        project_ship=project_ship,
                        amount_ship=amount_ship,
                        fleet_status=0,
                        place_id=session_user_city.id,
                        name=project_ship.name
                    )
                    ship.save()
                    ship = Ship.objects.filter(user=session_user, id_project_ship=ship_id, place_id=fleet.id,
                                               fleet_status=1).first()
                    new_amount = int(ship.amount_ship) - int(amount_ship)

                    if new_amount == 0:
                        Ship.objects.filter(user=session_user, id_project_ship=ship_id, place_id=fleet.id,
                                            fleet_status=1).delete()
                    else:
                        Ship.objects.filter(user=session_user, id_project_ship=ship_id, place_id=fleet.id,
                                            fleet_status=1).update(amount_ship=new_amount)

                    fleet = Fleet.objects.filter(user=session_user, id=fleet.id).first()
                    project_ship = ProjectShip.objects.filter(id=ship_id).first()

                    system_power = int(fleet_engine.system_power) - int(project_ship.system_power) * amount_ship
                    intersystem_power = int(fleet_engine.intersystem_power) - int(
                        project_ship.intersystem_power) * amount_ship
                    giper_power = int(fleet_engine.giper_power) - int(project_ship.giper_power) * amount_ship
                    giper_accuracy = int(fleet_engine.giper_accuracy) - int(project_ship.giper_accuracy) * amount_ship
                    null_power = int(fleet_engine.null_power) - int(project_ship.null_power) * amount_ship
                    null_accuracy = int(fleet_engine.null_accuracy) - int(project_ship.null_accuracy) * amount_ship
                    ship_empty_mass = int(fleet.ship_empty_mass) - int(project_ship.mass) * amount_ship
                    hold = int(fleet.hold) - hold * amount_ship
                    fuel_tank = int(fleet.fuel_tank) - fuel_tank * amount_ship
                    use_energy = fleet_energy_power.use_energy - use_energy
                    use_fuel_system = fleet_energy_power.use_fuel_system - use_fuel_system
                    use_fuel_intersystem = fleet_energy_power.use_fuel_intersystem - use_fuel_intersystem
                    use_energy_giper = fleet_energy_power.use_energy_giper - use_energy_giper
                    use_energy_null = fleet_energy_power.use_energy_null - use_energy_null
                    use_fuel_generator = fleet_energy_power.use_fuel_generator - use_fuel_generator
                    produced_energy = fleet_energy_power.produce_energy - produced_energy

                    fleet = Fleet.objects.filter(user=session_user, id=fleet.id).update(
                        ship_empty_mass=ship_empty_mass,
                        hold=hold,
                        empty_hold=hold,
                        fuel_tank=fuel_tank,
                        free_fuel_tank=fuel_tank,
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
                        use_energy=use_energy, use_fuel_system=use_fuel_system,
                        use_fuel_intersystem=use_fuel_intersystem, use_energy_giper=use_energy_giper,
                        use_energy_null=use_energy_null, use_fuel_generator=use_fuel_generator,
                        produce_energy=produced_energy
                    )
            else:
                message = 'Трюмы не пусты'
        else:
            message = 'Флот не над планетой'

        user_citys = UserCity.objects.filter(user=session_user).all()
        user_fleets = Fleet.objects.filter(user=session_user).all()
        ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1).all()
        ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city.id).all()
        add_ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city.id).all()
        request.session['userid'] = session_user.id
        request.session['user_city'] = session_user_city.id
        request.session['live'] = True
        output = {'user': session_user, 'warehouses': session_user_city.warehouse, 'user_city': session_user_city,
                  'user_citys': user_citys, 'user_fleets': user_fleets, 'add_ships': add_ships, 'fleet_id': fleet_id,
                  'ship_fleets': ship_fleets, 'ships': ships, 'fleet': fleet, 'command': command,
                  'flightplans': flightplans, 'flightplan_flights': flightplan_flights,
                  'warehouse_factorys': warehouse_factorys, 'message': message}
        return render(request, "space_forces.html", output)
