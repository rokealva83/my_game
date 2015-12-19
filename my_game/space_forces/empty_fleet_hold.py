# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity
from my_game.models import WarehouseElement, WarehouseFactory, BasicResource
from my_game import function
from my_game.models import Ship, Fleet, Hold
from my_game.models import FactoryPattern, HullPattern, ArmorPattern, ShellPattern, ShieldPattern, \
    GeneratorPattern, WeaponPattern, EnginePattern, ModulePattern, FuelPattern, DevicePattern
from my_game.space_forces.unloading import unloading


def empty_fleet_hold(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        function.check_all_queues(session_user)

        add_ships = {}
        flightplans = {}
        flightplan_flights = {}
        ship_holds = {}
        message = ''

        factory_patterns = FactoryPattern.objects.filter(user=session_user).all()
        hull_patterns = HullPattern.objects.filter(user=session_user).all()
        armor_patterns = ArmorPattern.objects.filter(user=session_user).all()
        shield_patterns = ShieldPattern.objects.filter(user=session_user).all()
        engine_patterns = EnginePattern.objects.filter(user=session_user).all()
        generator_patterns = GeneratorPattern.objects.filter(user=session_user).all()
        weapon_patterns = WeaponPattern.objects.filter(user=session_user).all()
        shell_patterns = ShellPattern.objects.filter(user=session_user).all()
        module_patterns = ModulePattern.objects.filter(user=session_user).all()
        fuel_patterns = FuelPattern.objects.filter(user=session_user).all()
        device_patterns = DevicePattern.objects.filter(user=session_user).all()

        full_request = request.POST
        my_dictionary = dict(full_request.iterlists())

        fleet_id_dict = my_dictionary.get('hidden_fleet')
        fleet_id = int(fleet_id_dict[0])
        fleet = Fleet.objects.filter(id=fleet_id).first()
        if fleet.planet_status == 1:
            ship_holds = Hold.objects.filter(fleet=fleet).order_by('class_shipment')

            resource_amount = my_dictionary.get('amount_resource1')
            if resource_amount is not None and resource_amount[0] != 0:
                shipment_id = 1
                class_shipment = 0
                size = int(resource_amount[0])
                amount_shipment = int(resource_amount[0])
                mass_shipment = int(resource_amount[0])
                unloading(session_user, session_user_city, fleet, class_shipment, shipment_id, amount_shipment,
                          mass_shipment, size)

            resource_amount = my_dictionary.get('amount_resource2')
            if resource_amount and resource_amount[0] != 0:
                shipment_id = 2
                class_shipment = 0
                size = int(resource_amount[0])
                amount_shipment = int(resource_amount[0])
                mass_shipment = int(resource_amount[0])
                unloading(session_user, session_user_city, fleet, class_shipment, shipment_id, amount_shipment,
                          mass_shipment, size)

            resource_amount = my_dictionary.get('amount_resource3')
            if resource_amount is not None and resource_amount[0] != 0:
                shipment_id = 3
                class_shipment = 0
                size = int(resource_amount[0])
                amount_shipment = int(resource_amount[0])
                mass_shipment = int(resource_amount[0])
                unloading(session_user, session_user_city, fleet, class_shipment, shipment_id, amount_shipment,
                          mass_shipment, size)

            resource_amount = my_dictionary.get('amount_resource4')
            if resource_amount is not None and resource_amount[0] != 0:
                shipment_id = 4
                class_shipment = 0
                size = int(resource_amount[0])
                amount_shipment = int(resource_amount[0])
                mass_shipment = int(resource_amount[0])
                unloading(session_user, session_user_city, fleet, class_shipment, shipment_id, amount_shipment,
                          mass_shipment, size)

            resource_amount = my_dictionary.get('amount_resource5')
            if resource_amount is not None and resource_amount[0] != 0:
                shipment_id = 5
                class_shipment = 0
                size = int(resource_amount[0])
                amount_shipment = int(resource_amount[0])
                mass_shipment = int(resource_amount[0])
                unloading(session_user, session_user_city, fleet, class_shipment, shipment_id, amount_shipment,
                          mass_shipment, size)

            resource_amount = my_dictionary.get('amount_resource6')
            if resource_amount is not None and resource_amount[0] != 0:
                shipment_id = 6
                class_shipment = 0
                size = int(resource_amount[0])
                amount_shipment = int(resource_amount[0])
                mass_shipment = int(resource_amount[0])
                unloading(session_user, session_user_city, fleet, class_shipment, shipment_id, amount_shipment,
                          mass_shipment, size)

            resource_amount = my_dictionary.get('amount_resource7')
            if resource_amount is not None and resource_amount[0] != 0:
                shipment_id = 7
                class_shipment = 0
                size = int(resource_amount[0])
                amount_shipment = int(resource_amount[0])
                mass_shipment = int(resource_amount[0])
                unloading(session_user, session_user_city, fleet, class_shipment, shipment_id, amount_shipment,
                          mass_shipment, size)

            resource_amount = my_dictionary.get('amount_resource8')
            if resource_amount is not None and resource_amount[0] != 0:
                shipment_id = 8
                class_shipment = 0
                size = int(resource_amount[0])

                amount_shipment = int(resource_amount[0])
                mass_shipment = int(resource_amount[0])
                unloading(session_user, session_user_city, fleet, class_shipment, shipment_id, amount_shipment,
                          mass_shipment, size)

            amount_factory = my_dictionary.get('amount_factory')
            if amount_factory is not None:
                shipment_id_fac = my_dictionary.get('hidden_factory')
                len_factory_amount = len(amount_factory)
                for i in range(len_factory_amount):
                    factory_amount = int(amount_factory[i])
                    if factory_amount != 0:
                        shipment_id = int(shipment_id_fac[i])
                        class_shipment = 10
                        factory = FactoryPattern.objects.filter(id=shipment_id).first()
                        size = int(factory.size) * factory_amount
                        amount_shipment = factory_amount
                        mass_shipment = int(factory.mass) * factory_amount
                        unloading(session_user, session_user_city, fleet, class_shipment, shipment_id, amount_shipment,
                                  mass_shipment, size)

            amount_hull = my_dictionary.get('amount_hull')
            if amount_hull is not None:
                shipment_id_hull = my_dictionary.get('hidden_hull')
                len_hull_amount = len(amount_hull)
                for i in range(len_hull_amount):
                    hull_amount = int(amount_hull[i])
                    if hull_amount != 0:
                        shipment_id = int(shipment_id_hull[i])
                        class_shipment = 1
                        hull = HullPattern.objects.filter(id=shipment_id).first()
                        size = int(hull.size) * hull_amount
                        amount_shipment = hull_amount
                        mass_shipment = int(hull.mass) * hull_amount
                        unloading(session_user, session_user_city, fleet, class_shipment, shipment_id, amount_shipment,
                                  mass_shipment, size)

            amount_armor = my_dictionary.get('amount_armor')
            if amount_armor is not None:
                shipment_id_arm = my_dictionary.get('hidden_armor')
                len_armor_amount = len(amount_armor)
                for i in range(len_armor_amount):
                    armor_amount = int(amount_armor[0])
                    if armor_amount != 0:
                        shipment_id = int(shipment_id_arm[i])
                        class_shipment = 2
                        armor = ArmorPattern.objects.filter(id=shipment_id).first()
                        size = 15 * armor_amount
                        amount_shipment = armor_amount
                        mass_shipment = int(armor.mass) * armor_amount
                        unloading(session_user, session_user_city, fleet, class_shipment, shipment_id, amount_shipment,
                                  mass_shipment, size)

            amount_shield = my_dictionary.get('amount_shield')
            if amount_shield is not None:
                shipment_id_shield = my_dictionary.get('hidden_shield')
                len_shield_amount = len(amount_shield)
                for i in range(len_shield_amount):
                    shield_amount = int(amount_shield[i])
                    if shield_amount != 0:
                        shipment_id = int(shipment_id_shield[i])
                        class_shipment = 3
                        shield = ShieldPattern.objects.filter(id=shipment_id).first()
                        size = int(shield.size) * shield_amount
                        amount_shipment = shield_amount
                        mass_shipment = int(shield.mass) * shield_amount
                        unloading(session_user, session_user_city, fleet, class_shipment, shipment_id, amount_shipment,
                                  mass_shipment, size)

            amount_engine = my_dictionary.get('amount_engine')
            if amount_engine is not None:
                shipment_id_eng = my_dictionary.get('hidden_engine')
                len_engine_amount = len(amount_engine)
                for i in range(len_engine_amount):
                    engine_amount = int(amount_engine[i])
                    if engine_amount != 0:
                        shipment_id = int(shipment_id_eng[i])
                        class_shipment = 4
                        engine = EnginePattern.objects.filter(id=shipment_id).first()
                        size = int(engine.size) * engine_amount
                        amount_shipment = engine_amount
                        mass_shipment = int(engine.mass) * engine_amount
                        unloading(session_user, session_user_city, fleet, class_shipment, shipment_id, amount_shipment,
                                  mass_shipment, size)

            amount_generator = my_dictionary.get('amount_generator')
            if amount_generator is not None:
                shipment_id_gen = my_dictionary.get('hidden_generator')
                len_generator_amount = len(amount_generator)
                for i in range(len_generator_amount):
                    generator_amount = int(amount_generator[i])
                    if generator_amount != 0:
                        shipment_id = int(shipment_id_gen[i])
                        class_shipment = 5
                        generator = GeneratorPattern.objects.filter(id=shipment_id).first()
                        size = int(generator.size) * generator_amount
                        amount_shipment = generator_amount
                        mass_shipment = int(generator.mass) * generator_amount
                        unloading(session_user, session_user_city, fleet, class_shipment, shipment_id, amount_shipment,
                                  mass_shipment, size)

            amount_weapon = my_dictionary.get('amount_weapon')
            if amount_weapon is not None:
                shipment_id_weap = my_dictionary.get('hidden_weapon')
                len_weapon_amount = len(amount_weapon)
                for i in range(len_weapon_amount):
                    weapon_amount = int(amount_weapon[i])
                    if weapon_amount != 0:
                        shipment_id = int(shipment_id_weap[i])
                        class_shipment = 6
                        weapon = WeaponPattern.objects.filter(id=shipment_id).first()
                        size = int(weapon.size) * weapon_amount
                        amount_shipment = weapon_amount
                        mass_shipment = int(weapon.mass) * weapon_amount
                        unloading(session_user, session_user_city, fleet, class_shipment, shipment_id, amount_shipment,
                                  mass_shipment, size)

            amount_shell = my_dictionary.get('amount_shell')
            if amount_shell is not None:
                shipment_id_shell = my_dictionary.get('hidden_shell')
                len_shell_amount = len(amount_shell)
                for i in range(len_shell_amount):
                    shell_amount = int(amount_shell[i])
                    if shell_amount != 0:
                        shipment_id = int(shipment_id_shell[i])
                        class_shipment = 7
                        shell = ShellPattern.objects.filter(id=shipment_id).first()
                        size = int(shell.size) * shell_amount
                        amount_shipment = shell_amount
                        mass_shipment = int(shell.mass) * shell_amount
                        unloading(session_user, session_user_city, fleet, class_shipment, shipment_id, amount_shipment,
                                  mass_shipment, size)

            amount_module = my_dictionary.get('amount_module')
            if amount_module is not None:
                shipment_id_mod = my_dictionary.get('hidden_module')
                len_module_amount = len(amount_module)
                for i in range(len_module_amount):
                    module_amount = int(amount_module[i])
                    if module_amount != 0:
                        shipment_id = int(shipment_id_mod[i])
                        class_shipment = 8
                        module = ModulePattern.objects.filter(id=shipment_id).first()
                        size = int(module.size) * module_amount
                        amount_shipment = module_amount
                        mass_shipment = int(module.mass) * module_amount
                        unloading(session_user, session_user_city, fleet, class_shipment, shipment_id, amount_shipment,
                                  mass_shipment, size)

            amount_device = my_dictionary.get('amount_device')
            if amount_device is not None:
                shipment_id_device = my_dictionary.get('hidden_device')
                len_device_amount = len(amount_device)
                for i in range(len_device_amount):
                    device_amount = int(amount_device[i])
                    if device_amount != 0:
                        shipment_id = int(shipment_id_device[i])
                        class_shipment = 9
                        device = DevicePattern.objects.filter(id=shipment_id).first()
                        size = int(device.size) * device_amount
                        amount_shipment = device_amount
                        mass_shipment = int(device.mass) * device_amount
                        unloading(session_user, session_user_city, fleet, class_shipment, shipment_id, amount_shipment,
                                  mass_shipment, size)

        else:
            message = 'Флот не над планетой'

        warehouse = session_user_city.warehouse
        basic_resources = BasicResource.objects.all()
        user_citys = UserCity.objects.filter(user=session_user).all()
        user_fleets = Fleet.objects.filter(user=session_user).all()
        ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city.id).all()
        ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1).all()
        warehouse_factorys = WarehouseFactory.objects.filter(user=session_user,
                                                             user_city=session_user_city).order_by(
            'production_class', 'production_id')
        warehouse_elements = WarehouseElement.objects.filter(user=session_user,
                                                             user_city=session_user_city).order_by(
            'element_class', 'element_id')

        command = 2
        request.session['user'] = session_user.id
        request.session['user_city'] = session_user_city.id
        request.session['live'] = True
        output = {'user': session_user, 'warehouse': warehouse, 'user_city': session_user, 'user_citys': user_citys,
                  'user_fleets': user_fleets, 'add_ships': add_ships, 'fleet_id': fleet_id, 'ship_fleets': ship_fleets,
                  'ships': ships, 'command': command, 'flightplans': flightplans,
                  'flightplan_flights': flightplan_flights, 'warehouse_factorys': warehouse_factorys,
                  'factory_patterns': factory_patterns, 'warehouse_elements': warehouse_elements,
                  'hull_patterns': hull_patterns, 'armor_patterns': armor_patterns, 'shell_patterns': shell_patterns,
                  'shield_patterns': shield_patterns, 'weapon_patterns': weapon_patterns,
                  'fuel_patterns': fuel_patterns, 'engine_patterns': engine_patterns,
                  'device_patterns': device_patterns, 'generator_patterns': generator_patterns,
                  'module_patterns': module_patterns, 'message': message, 'ship_holds': ship_holds,
                  'basic_resources': basic_resources}
        return render(request, "fleet_hold.html", output)
