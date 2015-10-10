# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity
from my_game.models import Warehouse, WarehouseElement, WarehouseFactory, BasicResource
from my_game import function
from my_game.models import Ship, Fleet, Hold
from my_game.models import FactoryPattern, HullPattern, ArmorPattern, ShellPattern, ShieldPattern, \
    GeneratorPattern, WeaponPattern, EnginePattern, ModulePattern, FuelPattern, DevicePattern


def fleet_hold(request):
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
        factory_patterns = {}
        hull_patterns = {}
        armor_patterns = {}
        shield_patterns = {}
        engine_patterns = {}
        generator_patterns = {}
        weapon_patterns = {}
        shell_patterns = {}
        module_patterns = {}
        device_patterns = {}
        ship_holds = {}
        message = ''
        add_shipment = 0
        id_shipment = 0
        class_shipment = 0
        amount_shipment = 0
        mass_shipment = 0
        size = 0

        factory_patterns = FactoryPattern.objects.filter(user=session_user)
        hull_patterns = HullPattern.objects.filter(user=session_user)
        armor_patterns = ArmorPattern.objects.filter(user=session_user)
        shield_patterns = ShieldPattern.objects.filter(user=session_user)
        engine_patterns = EnginePattern.objects.filter(user=session_user)
        generator_patterns = GeneratorPattern.objects.filter(user=session_user)
        weapon_patterns = WeaponPattern.objects.filter(user=session_user)
        shell_patterns = ShellPattern.objects.filter(user=session_user)
        module_patterns = ModulePattern.objects.filter(user=session_user)
        fuel_patterns = FuelPattern.objects.filter(user=session_user)
        device_patterns = DevicePattern.objects.filter(user=session_user)
        error = 0

        full_request = request.POST
        myDict = dict(full_request.iterlists())

        fleet_id_dict = myDict.get('hidden_fleet')
        fleet_id = int(fleet_id_dict[0])
        fleet = Fleet.objects.filter(id=fleet_id).first()
        ship_in_fleet = Ship.objects.filter(user=session_user, fleet_status=1, place_id=fleet_id).first()
        if fleet.planet_status == 1 and ship_in_fleet is not None:
            command = 2
            ship_holds = Hold.objects.filter(fleet_id=fleet_id).order_by('class_shipment')
            add_shipment = 0

            resource_amount = myDict.get('resource_amount')
            id_shipment_res = myDict.get('warehouse_resource')
            if resource_amount[0] != 0 and id_shipment_res is not None:
                id_shipment = int(id_shipment_res[0])
                class_shipment = 0
                size = int(resource_amount[0])
                if size <= fleet.empty_hold:
                    amount_shipment = int(resource_amount[0])
                    mass_shipment = int(resource_amount[0])
                    add_shipment = 1

            factory_amount = myDict.get('factory_amount')
            id_shipment_fac = myDict.get('warehouse_factory')
            if factory_amount[0] != 0 and add_shipment == 0 and id_shipment_fac is not None:
                id_shipment = int(id_shipment_fac[0])
                class_shipment = 10
                factory = FactoryPattern.objects.filter(id=id_shipment).first()
                size = factory.size * int(factory_amount[0])
                if size <= fleet.empty_hold:
                    amount_shipment = int(factory_amount[0])
                    mass_shipment = int(factory.mass) * int(factory_amount[0])
                    add_shipment = 1

            hull_amount = myDict.get('hull_amount')
            id_shipment_hull = myDict.get('warehouse_hull')
            if hull_amount[0] != 0 and add_shipment == 0 and id_shipment_hull is not None:
                id_shipment = int(id_shipment_hull[0])
                class_shipment = 1
                hull = HullPattern.objects.filter(id=id_shipment).first()
                size = hull.size * int(hull_amount[0])
                if size <= fleet.empty_hold:
                    amount_shipment = int(hull_amount[0])
                    mass_shipment = hull.mass * int(hull_amount[0])
                    add_shipment = 1

            armor_amount = myDict.get('armor_amount')
            id_shipment_arm = myDict.get('warehouse_armor')
            if int(armor_amount[0]) != 0 and add_shipment == 0 and id_shipment_arm is not None:
                id_shipment = int(id_shipment_arm[0])
                class_shipment = 2
                armor = ArmorPattern.objects.filter(id=id_shipment).first()
                size = 15 * int(armor_amount[0])
                if size <= fleet.empty_hold:
                    amount_shipment = int(armor_amount[0])
                    mass_shipment = armor.mass * int(armor_amount[0])
                    add_shipment = 1

            shield_amount = myDict.get('shield_amount')
            id_shipment_shield = myDict.get('warehouse_shield')
            if int(shield_amount[0]) != 0 and add_shipment == 0 and id_shipment_shield is not None:
                id_shipment = int(id_shipment_shield[0])
                class_shipment = 3
                shield = ShieldPattern.objects.filter(id=id_shipment).first()
                size = shield.size * int(shield_amount[0])
                if size <= fleet.empty_hold:
                    amount_shipment = int(shield_amount[0])
                    mass_shipment = shield.mass * int(shield_amount[0])
                    add_shipment = 1

            engine_amount = myDict.get('engine_amount')
            id_shipment_eng = myDict.get('warehouse_engine')
            if int(engine_amount[0]) != 0 and add_shipment == 0 and id_shipment_eng is not None:
                id_shipment = int(id_shipment_eng[0])
                class_shipment = 4
                engine = EnginePattern.objects.filter(id=id_shipment).first()
                size = engine.size * int(engine_amount[0])
                if size <= fleet.empty_hold:
                    amount_shipment = int(engine_amount[0])
                    mass_shipment = engine.mass * int(engine_amount[0])
                    add_shipment = 1

            generator_amount = myDict.get('generator_amount')
            id_shipment_gen = myDict.get('warehouse_generator')
            if int(generator_amount[0]) != 0 and add_shipment == 0 and id_shipment_gen is not None:
                id_shipment = int(id_shipment_gen[0])
                class_shipment = 5
                generator = GeneratorPattern.objects.filter(id=id_shipment).first()
                size = generator.size * int(generator_amount[0])
                if size <= fleet.empty_hold:
                    amount_shipment = int(generator_amount[0])
                    mass_shipment = generator.mass * int(generator_amount[0])
                    add_shipment = 1

            weapon_amount = myDict.get('weapon_amount')
            id_shipment_weap = myDict.get('warehouse_weapon')
            if int(weapon_amount[0]) != 0 and add_shipment == 0 and id_shipment_weap is not None:
                id_shipment = int(id_shipment_weap[0])
                class_shipment = 6
                weapon = WeaponPattern.objects.filter(id=id_shipment).first()
                size = weapon.size * int(weapon_amount[0])
                if size <= fleet.empty_hold:
                    amount_shipment = int(weapon_amount[0])
                    mass_shipment = weapon.mass * int(weapon_amount[0])
                    add_shipment = 1

            shell_amount = myDict.get('shell_amount')
            id_shipment_shell = myDict.get('warehouse_shell')
            if int(shell_amount[0]) != 0 and add_shipment == 0 and id_shipment_shell is not None:
                id_shipment = int(id_shipment_shell[0])
                class_shipment = 7
                shell = ShellPattern.objects.filter(id=id_shipment).first()
                size = shell.size * int(shell_amount[0])
                if size <= fleet.empty_hold:
                    amount_shipment = int(shell_amount[0])
                    mass_shipment = shell.mass * int(shell_amount[0])
                    add_shipment = 1

            module_amount = myDict.get('module_amount')
            id_shipment_mod = myDict.get('warehouse_module')
            if int(module_amount[0]) != 0 and add_shipment == 0 and id_shipment_mod is not None:
                id_shipment = int(id_shipment_mod[0])
                class_shipment = 8
                module = ModulePattern.objects.filter(id=id_shipment).first()
                size = module.size * int(module_amount[0])
                if size <= fleet.empty_hold:
                    amount_shipment = int(module_amount[0])
                    mass_shipment = module.mass * int(module_amount[0])
                    add_shipment = 1

            device_amount = myDict.get('device_amount')
            id_shipment_device = myDict.get('warehouse_device')
            if int(device_amount[0]) != 0 and add_shipment == 0 and id_shipment_device is not None:
                id_shipment = int(id_shipment_device[0])
                class_shipment = 9
                device = DevicePattern.objects.filter(id=id_shipment).first()
                size = device.size * int(device_amount[0])
                if size <= fleet.empty_hold:
                    amount_shipment = int(device_amount[0])
                    mass_shipment = device.mass * int(device_amount[0])
                    add_shipment = 1

            fuel_amount = myDict.get('fuel_amount')
            id_shipment_mod = myDict.get('warehouse_fuel')
            if int(fuel_amount[0]) != 0 and add_shipment == 0 and id_shipment_mod is not None:
                id_shipment = int(id_shipment_mod[0])
                class_shipment = 14
                fuel = FuelPattern.objects.filter(id=id_shipment).first()
                size = fuel.size * int(fuel_amount[0])
                if size <= fleet.empty_hold:
                    amount_shipment = int(fuel_amount[0])
                    mass_shipment = fuel.mass * int(fuel_amount[0])
                    add_shipment = 1

            if add_shipment != 0:
                if class_shipment == 0:
                    warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city,
                                                         id_resource=id_shipment).first()
                    if warehouse.amount >= amount_shipment:
                        new_amount = warehouse.amount - amount_shipment
                        warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city,
                                                             id_resource=id_shipment).update(amount=new_amount)
                    else:
                        error = 1

                elif class_shipment == 10:
                    warehouse_factory = WarehouseFactory.objects.filter(user_city=session_user_city,
                                                                         factory_id=id_shipment).first()
                    if warehouse_factory.amount >= amount_shipment:
                        new_factory_amount = warehouse_factory.amount - amount_shipment
                        warehouse_factory = WarehouseFactory.objects.filter(user_city=session_user_city,
                                                                             factory_id=id_shipment).update(
                            amount=new_factory_amount)
                    else:
                        error = 1

                elif 0 < class_shipment < 10 or class_shipment == 14:
                    warehouse_element = WarehouseElement.objects.filter(user_city=session_user_city,
                                                                         element_class=class_shipment,
                                                                         element_id=id_shipment).first()
                    if warehouse_element.amount >= amount_shipment:
                        new_element_amount = warehouse_element.amount - amount_shipment
                        warehouse_element = WarehouseElement.objects.filter(user_city=session_user_city,
                                                                             element_class=class_shipment,
                                                                             element_id=id_shipment).update(
                            amount=new_element_amount)

                if error == 0:
                    hold = Hold.objects.filter(fleet_id=fleet_id, class_shipment=class_shipment,
                                               id_shipment=id_shipment, ).first()
                    if hold:
                        amount_shipment = amount_shipment + hold.amount_shipment
                        mass_shipment = mass_shipment + hold.mass_shipment
                        size = size + hold.size_shipment
                        hold = Hold.objects.filter(fleet_id=fleet_id, class_shipment=class_shipment,
                                                   id_shipment=id_shipment, ).update(amount_shipment=amount_shipment,
                                                                                     mass_shipment=mass_shipment,
                                                                                     size_shipment=size)
                    else:
                        hold = Hold(
                            fleet_id=fleet_id,
                            class_shipment=class_shipment,
                            id_shipment=id_shipment,
                            amount_shipment=amount_shipment,
                            mass_shipment=mass_shipment,
                            size_shipment=size
                        )
                        hold.save()

                    new_fleet_mass = fleet.ship_empty_mass + mass_shipment
                    new_empty_hold = fleet.empty_hold - size
                    fleet = Fleet.objects.filter(id=fleet_id).update(ship_empty_mass=new_fleet_mass,
                                                                     empty_hold=new_empty_hold)
                else:
                    message = 'LAG'
            else:
                message = 'LAG'
        else:
            message = 'Флот не над планетой'

        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('id_resource')
        basic_resources = BasicResource.objects.filter()
        user_city = UserCity.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = UserCity.objects.filter(user=int(session_user))
        user_fleets = Fleet.objects.filter(user=session_user)
        ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city)
        ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1)
        warehouse_factorys = WarehouseFactory.objects.filter(user=session_user,
                                                              user_city=session_user_city).order_by(
            'production_class', 'production_id')
        warehouse_elements = WarehouseElement.objects.filter(user=session_user,
                                                              user_city=session_user_city).order_by(
            'element_class', 'element_id')

        command = 2
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouses': warehouses, 'basic_resources': basic_resources, 'user_city': user_city,
                  'user_citys': user_citys, 'user_fleets': user_fleets, 'add_ships': add_ships, 'fleet_id': fleet_id,
                  'ship_fleets': ship_fleets, 'fuel_patterns': fuel_patterns, 'shell_patterns': shell_patterns,
                  'ships': ships, 'command': command, 'flightplans': flightplans,
                  'flightplan_flights': flightplan_flights, 'warehouse_factorys': warehouse_factorys,
                  'factory_patterns': factory_patterns, 'warehouse_elements': warehouse_elements,
                  'hull_patterns': hull_patterns, 'armor_patterns': armor_patterns, 'shield_patterns': shield_patterns,
                  'weapon_patterns': weapon_patterns, 'device_patterns': device_patterns,
                  'engine_patterns': engine_patterns, 'generator_patterns': generator_patterns,
                  'module_patterns': module_patterns, 'message': message, 'ship_holds': ship_holds}
        return render(request, "fleet_hold.html", output)