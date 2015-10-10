# -*- coding: utf-8 -*-


from my_game.models import BasicResource
from my_game.models import ShieldPattern, GeneratorPattern, EnginePattern, ArmorPattern, WeaponPattern, \
    ShellPattern, FactoryPattern, DevicePattern
from my_game.models import WarehouseElement, WarehouseFactory
from my_game.models import TradeElement, TradeSpace, BuildingInstalled, DeliveryQueue
from django.shortcuts import render
from my_game.models import MyUser, UserCity
from my_game.models import Warehouse
from my_game.models import HullPattern, ElementShip, ModulePattern
from my_game.models import ProjectShip, Ship, Fleet, FleetParametrScan, FleetEnergyPower, FleetEngine
from my_game import function


def create_trade_fleet(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        ship_id = 0
        amount_ship = 0
        hold = 0

        full_request = request.POST
        myDict = dict(full_request.iterlists())
        amount_ship_dict = myDict.get('amount_ship')
        ship_id_dict = myDict.get('hidden_ship')
        trade_space_id = request.POST.get('trade_space_id')
        len_amount_ship_dict = len(amount_ship_dict)
        for i in range(len_amount_ship_dict):
            if int(amount_ship_dict[i]) != 0:
                amount_ship = int(amount_ship_dict[i])
                ship_id = int(ship_id_dict[i])

        ship = Ship.objects.filter(id=ship_id, user=session_user, fleet_status=0,
                                   place_id=session_user_city).first()

        if int(ship.amount_ship) >= int(amount_ship):
            user_city = UserCity.objects.filter(id=session_user_city).first()
            fleet = Fleet(
                user=session_user,
                name='Trade',
                x=user_city.x,
                y=user_city.y,
                z=user_city.z,
                system=user_city.system_id,
                planet=user_city.planet_id
            )
            fleet.save()
            fleet_id = fleet.pk

            fleet_energy = FleetEnergyPower(
                fleet_id=fleet_id
            )
            fleet_energy.save()

            fleet_engine = FleetEngine(
                fleet_id=fleet_id
            )
            fleet_engine.save()

            ship_pattern = ProjectShip.objects.filter(id=ship.id_project_ship).first()
            hull_pattern = HullPattern.objects.filter(id=ship_pattern.hull_id).first()
            fleet_engine = FleetEngine.objects.filter(fleet_id=fleet_id).first()
            fleet_energy_power = FleetEnergyPower.objects.filter(fleet_id=fleet_id).first()
            ship_elements = ElementShip.objects.filter(id_project_ship=ship.id_project_ship)
            use_energy = hull_pattern.power_consuption
            use_fuel_system = 0
            use_fuel_intersystem = 0
            use_energy_giper = 0
            use_energy_null = 0
            use_fuel_generator = 0
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
                                                                    module_class=6).first()
                    if element_pattern:
                        fleet_parametr_scan = FleetParametrScan(
                            fleet_id=fleet_id,
                            method_scanning=element_pattern.param3,
                            time_scanning=element_pattern.param2,
                            range_scanning=element_pattern.param1
                        )
                        use_energy = use_energy + element_pattern.power_consuption

            hold = hold + hull_pattern.hold_size
            use_energy = use_energy * amount_ship
            use_fuel_system = use_fuel_system * amount_ship
            use_fuel_intersystem = use_fuel_intersystem * amount_ship
            use_energy_giper = use_energy_giper * amount_ship
            use_energy_null = use_energy_null * amount_ship
            use_fuel_generator = use_fuel_generator * amount_ship
            produced_energy = produced_energy * amount_ship

            if int(ship.amount_ship) == int(amount_ship):
                ship = Ship.objects.filter(id=ship_id, user=session_user, fleet_status=0,
                                           place_id=session_user_city).update(fleet_status=1,
                                                                              place_id=fleet_id)
                ship = Ship.objects.filter(id=ship_id).first()
                project_ship = ProjectShip.objects.filter(id=ship.id_project_ship).first()
                ship_in_fleet = Ship.objects.filter(place_id=fleet_id).first()
                if ship_in_fleet:
                    hold_empty = fleet.empty_hold + hold * amount_ship
                    hold = fleet.fleet_hold + hold * amount_ship
                    ship_empty_mass = fleet.ship_empty_mass + project_ship.mass * amount_ship

                    system_power = fleet_engine.system_power + int(project_ship.system_power) * amount_ship
                    intersystem_power = fleet_engine.intersystem_power + int(
                        project_ship.intersystem_power) * amount_ship
                    giper_power = fleet_engine.giper_power + int(project_ship.giper_power) * amount_ship
                    null_power = fleet_engine.null_power + int(project_ship.null_power) * amount_ship
                else:
                    hold_empty = hold * amount_ship
                    hold = hold * amount_ship
                    ship_empty_mass = project_ship.mass * amount_ship
                    system_power = int(project_ship.system_power) * amount_ship
                    intersystem_power = int(project_ship.intersystem_power) * amount_ship
                    giper_power = int(project_ship.giper_power) * amount_ship
                    null_power = int(project_ship.null_power) * amount_ship

                fleet_engine = FleetEngine.objects.filter(fleet_id=fleet_id).update(
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
                    empty_hold=hold_empty
                )

                fleet_energy_power = FleetEnergyPower.objects.filter(fleet_id=fleet_id).update(
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
                project_ship = ProjectShip.objects.filter(id=ship.id_project_ship).first()
                ship_in_fleet = Ship.objects.filter(place_id=fleet_id).first()

                if ship_in_fleet:
                    hold_empty = fleet.empty_hold + hold * amount_ship
                    hold = fleet.fleet_hold + hold * amount_ship
                    ship_empty_mass = fleet.ship_empty_mass + project_ship.mass * amount_ship

                    system_power = fleet_engine.system_power + int(project_ship.system_power) * amount_ship
                    intersystem_power = fleet_engine.intersystem_power + int(
                        project_ship.intersystem_power) * amount_ship
                    giper_power = fleet_engine.giper_power + int(project_ship.giper_power) * amount_ship
                    null_power = fleet_engine.null_power + int(project_ship.null_power) * amount_ship
                else:
                    hold_empty = hold * amount_ship
                    hold = hold * amount_ship
                    ship_empty_mass = project_ship.mass * amount_ship
                    system_power = int(project_ship.system_power) * amount_ship
                    intersystem_power = int(project_ship.intersystem_power) * amount_ship
                    giper_power = int(project_ship.giper_power) * amount_ship
                    null_power = int(project_ship.null_power) * amount_ship

                fleet_engine = FleetEngine.objects.filter(fleet_id=fleet_id).update(
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
                    empty_hold=hold_empty
                )

                fleet_energy_power = FleetEnergyPower.objects.filter(fleet_id=fleet_id).update(
                    use_energy=use_energy, use_fuel_system=use_fuel_system,
                    use_fuel_intersystem=use_fuel_intersystem, use_energy_giper=use_energy_giper,
                    use_energy_null=use_energy_null, use_fuel_generator=use_fuel_generator,
                    produce_energy=produced_energy
                )
            message = 'Корабли добавлено во флот'
        else:
            message = 'Недостаточно корблей'

        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('id_resource')
        basic_resources = BasicResource.objects.filter()
        user_city = UserCity.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = UserCity.objects.filter(user=int(session_user))
        warehouse_elements = WarehouseElement.objects.filter(user=session_user, user_city=session_user_city).order_by(
            'element_class', 'element_id')
        warehouse_factorys = WarehouseFactory.objects.filter(user=session_user, user_city=session_user_city).order_by(
            'production_class', 'production_id')
        factory_patterns = FactoryPattern.objects.filter(user=session_user)
        hull_patterns = HullPattern.objects.filter(user=session_user)
        armor_patterns = ArmorPattern.objects.filter(user=session_user)
        shield_patterns = ShieldPattern.objects.filter(user=session_user)
        engine_patterns = EnginePattern.objects.filter(user=session_user)
        generator_patterns = GeneratorPattern.objects.filter(user=session_user)
        weapon_patterns = WeaponPattern.objects.filter(user=session_user)
        shell_patterns = ShellPattern.objects.filter(user=session_user)
        module_patterns = ModulePattern.objects.filter(user=session_user)
        device_patterns = DevicePattern.objects.filter(user=session_user)
        trade_spaces = TradeSpace.objects.filter()
        ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city)
        project_ships = ProjectShip.objects.filter(user=session_user)
        users = MyUser.objects.filter()
        trade_elements = TradeElement.objects.filter(trade_space=1)
        user_trade_elements = TradeElement.objects.filter(trade_space=trade_space_id, user=session_user)
        trade_building = BuildingInstalled.objects.filter(user=session_user, user_city=session_user_city,
                                                           production_class=13).first()
        delivery_queues = DeliveryQueue.objects.filter(user=session_user, user_city=session_user_city)
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouses': warehouses, 'basic_resources': basic_resources,
                  'user_city': user_city, 'user_citys': user_citys, 'warehouse_factorys': warehouse_factorys,
                  'factory_patterns': factory_patterns, 'warehouse_elements': warehouse_elements,
                  'hull_patterns': hull_patterns, 'armor_patterns': armor_patterns,
                  'shield_patterns': shield_patterns, 'engine_patterns': engine_patterns,
                  'generator_patterns': generator_patterns, 'weapon_patterns': weapon_patterns,
                  'shell_patterns': shell_patterns, 'module_patterns': module_patterns,
                  'device_patterns': device_patterns,
                  'trade_spaces': trade_spaces, 'trade_space_id': trade_space_id, 'project_ships': project_ships,
                  'ships': ships, 'trade_elements': trade_elements, 'user_trade_elements': user_trade_elements,
                  'users': users, 'message': message, 'trade_building': trade_building,
                  'delivery_queues': delivery_queues}
        return render(request, "trade.html", output)