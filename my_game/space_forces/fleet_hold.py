# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity
from my_game.models import WarehouseElement, WarehouseFactory
from my_game import function
from my_game.models import Ship, Fleet, Hold
from my_game.models import FactoryPattern, HullPattern, ArmorPattern, ShellPattern, ShieldPattern, \
    GeneratorPattern, WeaponPattern, EnginePattern, ModulePattern, FuelPattern, DevicePattern


def fleet_hold(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        function.check_all_queues(session_user)

        add_ships = flightplans = flightplan_flights = ship_holds = {}
        message = 'LAG'
        shipment_id = class_shipment = amount_shipment = mass_shipment = size = error = 0

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
        ship_in_fleet = Ship.objects.filter(user=session_user, fleet_status=1, place_id=fleet.id).first()
        if fleet.planet_status == 1 and ship_in_fleet is not None:
            ship_holds = Hold.objects.filter(fleet=fleet).order_by('class_shipment')
            add_shipment = 0

            resource_amount = my_dictionary.get('resource_amount')
            shipment_id_res = my_dictionary.get('warehouse_resource')
            if int(resource_amount[0]) != 0 and shipment_id_res:
                amount = int(resource_amount[0])
                shipment_id = int(shipment_id_res[0])
                size = int(amount)
                if size <= fleet.empty_hold:
                    resource_hold = fleet.resource_hold
                    warehouse = session_user_city.warehouse
                    if shipment_id == 1:
                        if session_user_city.warehouse.res_nickel < amount:
                            amount = session_user_city.warehouse.res_nickel
                        res_nickel = resource_hold.res_nickel + amount
                        setattr(resource_hold, 'res_nickel', res_nickel)
                        setattr(warehouse, 'res_nickel', (warehouse.res_nickel - amount))
                    elif shipment_id == 2:
                        if session_user_city.warehouse.res_iron < amount:
                            amount = session_user_city.warehouse.res_iron
                        res_iron = resource_hold.res_iron + amount
                        setattr(resource_hold, 'res_iron', res_iron)
                        setattr(warehouse, 'res_iron', (warehouse.res_iron - amount))
                    elif shipment_id == 3:
                        if session_user_city.warehouse.res_cooper < amount:
                            amount = session_user_city.warehouse.res_cooper
                        res_cooper = resource_hold.res_cooper + amount
                        setattr(resource_hold, 'res_cooper', res_cooper)
                        setattr(warehouse, 'res_cooper', (warehouse.res_cooper - amount))
                    elif shipment_id == 4:
                        if session_user_city.warehouse.res_aluminum < amount:
                            amount = session_user_city.warehouse.res_aluminum
                        res_aluminum = resource_hold.res_aluminum + amount
                        setattr(resource_hold, 'res_aluminum', res_aluminum)
                        setattr(warehouse, 'res_aluminum', (warehouse.res_aluminum - amount))
                    elif shipment_id == 5:
                        if session_user_city.warehouse.res_veriarit < amount:
                            amount = session_user_city.warehouse.res_veriarit
                        res_veriarit = resource_hold.res_veriarit + amount
                        setattr(resource_hold, 'res_veriarit', res_veriarit)
                        setattr(warehouse, 'res_veriarit', (warehouse.res_veriarit - amount))
                    elif shipment_id == 6:
                        if session_user_city.warehouse.res_inneilit < amount:
                            amount = session_user_city.warehouse.res_inneilit
                        res_inneilit = resource_hold.res_inneilit + amount
                        setattr(resource_hold, 'res_inneilit', res_inneilit)
                        setattr(warehouse, 'res_inneilit', (warehouse.res_inneilit - amount))
                    elif shipment_id == 7:
                        if session_user_city.warehouse.res_renniit < amount:
                            amount = session_user_city.warehouse.res_renniit
                        res_renniit = resource_hold.res_renniit + amount
                        setattr(resource_hold, 'res_renniit', res_renniit)
                        setattr(warehouse, 'res_renniit', (warehouse.res_renniit - amount))
                    elif shipment_id == 8:
                        if session_user_city.warehouse.res_cobalt < amount:
                            amount = session_user_city.warehouse.res_cobalt
                        res_cobalt = resource_hold.res_cobalt + amount
                        setattr(resource_hold, 'res_cobalt', res_cobalt)
                        setattr(warehouse, 'res_cobalt', (warehouse.res_cobalt - amount))
                    elif shipment_id == 9:
                        if session_user_city.warehouse.mat_construction_material < amount:
                            amount = session_user_city.warehouse.mat_construction_material
                        mat_construction_material = resource_hold.mat_construction_material + amount
                        setattr(resource_hold, 'mat_construction_material', mat_construction_material)
                        setattr(warehouse, 'mat_construction_material', (warehouse.mat_construction_material - amount))
                    elif shipment_id == 10:
                        if session_user_city.warehouse.mat_chemical < amount:
                            amount = session_user_city.warehouse.mat_chemical
                        mat_chemical = resource_hold.mat_chemical + amount
                        setattr(resource_hold, 'mat_chemical', mat_chemical)
                        setattr(warehouse, 'mat_chemical', (warehouse.mat_chemical - amount))
                    elif shipment_id == 11:
                        if session_user_city.warehouse.mat_high_strength_allov < amount:
                            amount = session_user_city.warehouse.mat_high_strength_allov
                        mat_high_strength_allov = resource_hold.mat_high_strength_allov + amount
                        setattr(resource_hold, 'mat_high_strength_allov', mat_high_strength_allov)
                        setattr(warehouse, 'mat_high_strength_allov', (warehouse.mat_high_strength_allov - amount))
                    elif shipment_id == 12:
                        if session_user_city.warehouse.mat_nanoelement < amount:
                            amount = session_user_city.warehouse.mat_nanoelement
                        mat_nanoelement = resource_hold.mat_nanoelement + amount
                        setattr(resource_hold, 'mat_nanoelement', mat_nanoelement)
                        setattr(warehouse, 'mat_nanoelement', (warehouse.mat_nanoelement - amount))
                    elif shipment_id == 13:
                        if session_user_city.warehouse.mat_microprocessor_element < amount:
                            amount = session_user_city.warehouse.mat_microprocessor_element
                        mat_microprocessor_element = resource_hold.mat_microprocessor_element + amount
                        setattr(resource_hold, 'mat_microprocessor_element', mat_microprocessor_element)
                        setattr(warehouse, 'mat_microprocessor_element',
                                (warehouse.mat_microprocessor_element - amount))
                    elif shipment_id == 14:
                        if session_user_city.warehouse.mat_fober_optic_element < amount:
                            amount = session_user_city.warehouse.mat_fober_optic_element
                        mat_fober_optic_element = resource_hold.mat_fober_optic_element + amount
                        setattr(resource_hold, 'mat_fober_optic_element', mat_fober_optic_element)
                        setattr(warehouse, 'mat_fober_optic_element', (warehouse.mat_fober_optic_element - amount))
                    resource_hold.save()
                    warehouse.save()
                    mass_shipment = amount
                    add_shipment = 0
                    new_fleet_mass = fleet.ship_empty_mass + mass_shipment
                    new_empty_hold = fleet.empty_hold - size
                    new_hold = fleet.fleet_hold + size
                    Fleet.objects.filter(id=fleet.id).update(ship_empty_mass=new_fleet_mass, empty_hold=new_empty_hold,
                                                             fleet_hold=new_hold)
                    message = 'Ресурсы загружено'

            factory_amount = my_dictionary.get('factory_amount')
            shipment_id_fac = my_dictionary.get('warehouse_factory')
            if factory_amount[0] != 0 and add_shipment == 0 and shipment_id_fac is not None:
                shipment_id = int(shipment_id_fac[0])
                class_shipment = 10
                factory = FactoryPattern.objects.filter(id=shipment_id).first()
                size = factory.factory_size * int(factory_amount[0])
                if size <= fleet.empty_hold:
                    amount_shipment = int(factory_amount[0])
                    mass_shipment = int(factory.factory_mass) * int(factory_amount[0])
                    add_shipment = 1

            hull_amount = my_dictionary.get('hull_amount')
            shipment_id_hull = my_dictionary.get('warehouse_hull')
            if hull_amount[0] != 0 and add_shipment == 0 and shipment_id_hull is not None:
                shipment_id = int(shipment_id_hull[0])
                class_shipment = 1
                hull = HullPattern.objects.filter(id=shipment_id).first()
                size = hull.hull_size * int(hull_amount[0])
                if size <= fleet.empty_hold:
                    amount_shipment = int(hull_amount[0])
                    mass_shipment = hull.hull_mass * int(hull_amount[0])
                    add_shipment = 1

            armor_amount = my_dictionary.get('armor_amount')
            shipment_id_arm = my_dictionary.get('warehouse_armor')
            if int(armor_amount[0]) != 0 and add_shipment == 0 and shipment_id_arm is not None:
                shipment_id = int(shipment_id_arm[0])
                class_shipment = 2
                armor = ArmorPattern.objects.filter(id=shipment_id).first()
                size = 15 * int(armor_amount[0])
                if size <= fleet.empty_hold:
                    amount_shipment = int(armor_amount[0])
                    mass_shipment = armor.armor_mass * int(armor_amount[0])
                    add_shipment = 1

            shield_amount = my_dictionary.get('shield_amount')
            shipment_id_shield = my_dictionary.get('warehouse_shield')
            if int(shield_amount[0]) != 0 and add_shipment == 0 and shipment_id_shield is not None:
                shipment_id = int(shipment_id_shield[0])
                class_shipment = 3
                shield = ShieldPattern.objects.filter(id=shipment_id).first()
                size = shield.shield_size * int(shield_amount[0])
                if size <= fleet.empty_hold:
                    amount_shipment = int(shield_amount[0])
                    mass_shipment = shield.shield_mass * int(shield_amount[0])
                    add_shipment = 1

            engine_amount = my_dictionary.get('engine_amount')
            shipment_id_eng = my_dictionary.get('warehouse_engine')
            if int(engine_amount[0]) != 0 and add_shipment == 0 and shipment_id_eng is not None:
                shipment_id = int(shipment_id_eng[0])
                class_shipment = 4
                engine = EnginePattern.objects.filter(id=shipment_id).first()
                size = engine.engine_size * int(engine_amount[0])
                if size <= fleet.empty_hold:
                    amount_shipment = int(engine_amount[0])
                    mass_shipment = engine.engine_mass * int(engine_amount[0])
                    add_shipment = 1

            generator_amount = my_dictionary.get('generator_amount')
            shipment_id_gen = my_dictionary.get('warehouse_generator')
            if int(generator_amount[0]) != 0 and add_shipment == 0 and shipment_id_gen is not None:
                shipment_id = int(shipment_id_gen[0])
                class_shipment = 5
                generator = GeneratorPattern.objects.filter(id=shipment_id).first()
                size = generator.generator_size * int(generator_amount[0])
                if size <= fleet.empty_hold:
                    amount_shipment = int(generator_amount[0])
                    mass_shipment = generator.generator_mass * int(generator_amount[0])
                    add_shipment = 1

            weapon_amount = my_dictionary.get('weapon_amount')
            shipment_id_weap = my_dictionary.get('warehouse_weapon')
            if int(weapon_amount[0]) != 0 and add_shipment == 0 and shipment_id_weap is not None:
                shipment_id = int(shipment_id_weap[0])
                class_shipment = 6
                weapon = WeaponPattern.objects.filter(id=shipment_id).first()
                size = weapon.weapon_size * int(weapon_amount[0])
                if size <= fleet.empty_hold:
                    amount_shipment = int(weapon_amount[0])
                    mass_shipment = weapon.weapon_mass * int(weapon_amount[0])
                    add_shipment = 1

            shell_amount = my_dictionary.get('shell_amount')
            shipment_id_shell = my_dictionary.get('warehouse_shell')
            if int(shell_amount[0]) != 0 and add_shipment == 0 and shipment_id_shell is not None:
                shipment_id = int(shipment_id_shell[0])
                class_shipment = 7
                shell = ShellPattern.objects.filter(id=shipment_id).first()
                size = shell.shell_size * int(shell_amount[0])
                if size <= fleet.empty_hold:
                    amount_shipment = int(shell_amount[0])
                    mass_shipment = shell.shell_mass * int(shell_amount[0])
                    add_shipment = 1

            module_amount = my_dictionary.get('module_amount')
            shipment_id_mod = my_dictionary.get('warehouse_module')
            if int(module_amount[0]) != 0 and add_shipment == 0 and shipment_id_mod is not None:
                shipment_id = int(shipment_id_mod[0])
                class_shipment = 8
                module = ModulePattern.objects.filter(id=shipment_id).first()
                size = module.module_size * int(module_amount[0])
                if size <= fleet.empty_hold:
                    amount_shipment = int(module_amount[0])
                    mass_shipment = module.module_mass * int(module_amount[0])
                    add_shipment = 1

            device_amount = my_dictionary.get('device_amount')
            shipment_id_device = my_dictionary.get('warehouse_device')
            if int(device_amount[0]) != 0 and add_shipment == 0 and shipment_id_device is not None:
                shipment_id = int(shipment_id_device[0])
                class_shipment = 9
                device = DevicePattern.objects.filter(id=shipment_id).first()
                size = device.device_size * int(device_amount[0])
                if size <= fleet.empty_hold:
                    amount_shipment = int(device_amount[0])
                    mass_shipment = device.device_mass * int(device_amount[0])
                    add_shipment = 1

            fuel_amount = my_dictionary.get('fuel_amount')
            shipment_id_mod = my_dictionary.get('warehouse_fuel')
            if int(fuel_amount[0]) != 0 and add_shipment == 0 and shipment_id_mod is not None:
                shipment_id = int(shipment_id_mod[0])
                class_shipment = 14
                fuel = FuelPattern.objects.filter(id=shipment_id).first()
                size = fuel.fuel_size * int(fuel_amount[0])
                if size <= fleet.empty_hold:
                    amount_shipment = int(fuel_amount[0])
                    mass_shipment = fuel.fuel_mass * int(fuel_amount[0])
                    add_shipment = 1

            if add_shipment != 0:
                if class_shipment == 10:
                    warehouse_factory = WarehouseFactory.objects.filter(user_city=session_user_city,
                                                                        factory_id=shipment_id).first()
                    if warehouse_factory.amount >= amount_shipment:
                        new_factory_amount = warehouse_factory.amount - amount_shipment
                        WarehouseFactory.objects.filter(user_city=session_user_city, factory_id=shipment_id).update(
                            amount=new_factory_amount)
                    else:
                        error = 1

                elif 0 < class_shipment < 10 or class_shipment == 14:
                    warehouse_element = WarehouseElement.objects.filter(user_city=session_user_city,
                                                                        element_class=class_shipment,
                                                                        element_id=shipment_id).first()
                    if warehouse_element.amount >= amount_shipment:
                        new_element_amount = warehouse_element.amount - amount_shipment
                        WarehouseElement.objects.filter(user_city=session_user_city, element_class=class_shipment,
                                                        element_id=shipment_id).update(amount=new_element_amount)

                if error == 0:
                    hold = Hold.objects.filter(fleet=fleet, class_shipment=class_shipment,
                                               shipment_id=shipment_id, ).first()
                    if hold:
                        amount_shipment = amount_shipment + hold.amount_shipment
                        mass_shipment = mass_shipment + hold.mass_shipment
                        size = size + hold.size_shipment
                        Hold.objects.filter(fleet=fleet, class_shipment=class_shipment,
                                            shipment_id=shipment_id, ).update(amount_shipment=amount_shipment,
                                                                              mass_shipment=mass_shipment,
                                                                              size_shipment=size)
                    else:
                        hold = Hold(
                            fleet=fleet,
                            class_shipment=class_shipment,
                            shipment_id=shipment_id,
                            amount_shipment=amount_shipment,
                            mass_shipment=mass_shipment,
                            size_shipment=size
                        )
                        hold.save()

                    new_fleet_mass = fleet.ship_empty_mass + mass_shipment
                    new_empty_hold = fleet.empty_hold - size
                    new_hold = fleet.fleet_hold + size
                    Fleet.objects.filter(id=fleet.id).update(ship_empty_mass=new_fleet_mass, empty_hold=new_empty_hold,
                                                             fleet_hold=new_hold)
                    message = 'Комплектующие загружено'
                else:
                    message = 'LAG'
        else:
            message = 'Флот не над планетой'

        user_citys = UserCity.objects.filter(user=session_user).all()
        user_fleets = Fleet.objects.filter(user=session_user).all()
        ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city.id).all()
        ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1).all()
        warehouse_factorys = WarehouseFactory.objects.filter(user=session_user,
                                                             user_city=session_user_city).all()
        warehouse_elements = WarehouseElement.objects.filter(user=session_user,
                                                             user_city=session_user_city).order_by('element_class',
                                                                                                   'element_id')
        command = 2
        request.session['user'] = session_user.id
        request.session['user_city'] = session_user_city.id
        request.session['live'] = True
        output = {'user': session_user, 'warehouse': session_user_city.warehouse, 'user_city': session_user_city,
                  'user_citys': user_citys, 'user_fleets': user_fleets, 'add_ships': add_ships, 'fleet_id': fleet_id,
                  'ship_fleets': ship_fleets, 'fuel_patterns': fuel_patterns, 'shell_patterns': shell_patterns,
                  'ships': ships, 'command': command, 'flightplans': flightplans,
                  'flightplan_flights': flightplan_flights, 'warehouse_factorys': warehouse_factorys,
                  'factory_patterns': factory_patterns, 'warehouse_elements': warehouse_elements,
                  'hull_patterns': hull_patterns, 'armor_patterns': armor_patterns, 'shield_patterns': shield_patterns,
                  'weapon_patterns': weapon_patterns, 'device_patterns': device_patterns,
                  'engine_patterns': engine_patterns, 'generator_patterns': generator_patterns,
                  'module_patterns': module_patterns, 'message': message, 'ship_holds': ship_holds, 'fleet': fleet}
        return render(request, "fleet_hold.html", output)
