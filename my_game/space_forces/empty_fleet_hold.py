# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, User_city
from my_game.models import Warehouse, Warehouse_element, Warehouse_factory, Warehouse_ship
from my_game import function
from my_game.models import Project_ship, Ship, Fleet, Hold
from my_game.models import Flightplan, Flightplan_flight
from my_game.models import Factory_pattern, Hull_pattern, Armor_pattern, Shell_pattern, Shield_pattern, \
    Generator_pattern, Weapon_pattern, Engine_pattern, Module_pattern


def empty_fleet_hold(request):
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
        ship_holds = {}
        message = ''

        factory_patterns = Factory_pattern.objects.filter(user=session_user)
        hull_patterns = Hull_pattern.objects.filter(user=session_user)
        armor_patterns = Armor_pattern.objects.filter(user=session_user)
        shield_patterns = Shield_pattern.objects.filter(user=session_user)
        engine_patterns = Engine_pattern.objects.filter(user=session_user)
        generator_patterns = Generator_pattern.objects.filter(user=session_user)
        weapon_patterns = Weapon_pattern.objects.filter(user=session_user)
        shell_patterns = Shell_pattern.objects.filter(user=session_user)
        module_patterns = Module_pattern.objects.filter(user=session_user)
        # device_patterns = Device_pattern.objects.filter(user = session_user)
        error = 0

        full_request = request.POST
        myDict = dict(full_request.iterlists())

        fleet_id_dict = myDict.get('hidden_fleet')
        fleet_id = int(fleet_id_dict[0])
        fleet = Fleet.objects.filter(id=fleet_id).first()
        if fleet.planet_status == 1:
            command = 2
            ship_holds = Hold.objects.filter(fleet_id=fleet_id).order_by('class_shipment')
            add_shipment = 0

            resource_amount = myDict.get('amount_resource1')
            if resource_amount is not None and resource_amount[0] != 0:
                id_shipment = 1
                class_shipment = 0
                size = int(resource_amount[0])
                amount_shipment = int(resource_amount[0])
                mass_shipment = int(resource_amount[0])
                unloading(session_user, session_user_city, fleet_id, class_shipment, id_shipment, amount_shipment,
                          mass_shipment, size)

            resource_amount = myDict.get('amount_resource2')
            if resource_amount is not None and resource_amount[0] != 0:
                id_shipment = 2
                class_shipment = 0
                size = int(resource_amount[0])
                amount_shipment = int(resource_amount[0])
                mass_shipment = int(resource_amount[0])
                unloading(session_user, session_user_city, fleet_id, class_shipment, id_shipment, amount_shipment,
                          mass_shipment, size)

            resource_amount = myDict.get('amount_resource3')
            if resource_amount is not None and resource_amount[0] != 0:
                id_shipment = 3
                class_shipment = 0
                size = int(resource_amount[0])
                amount_shipment = int(resource_amount[0])
                mass_shipment = int(resource_amount[0])
                unloading(session_user, session_user_city, fleet_id, class_shipment, id_shipment, amount_shipment,
                          mass_shipment, size)

            resource_amount = myDict.get('amount_resource4')
            if resource_amount is not None and resource_amount[0] != 0:
                id_shipment = 4
                class_shipment = 0
                size = int(resource_amount[0])
                amount_shipment = int(resource_amount[0])
                mass_shipment = int(resource_amount[0])
                unloading(session_user, session_user_city, fleet_id, class_shipment, id_shipment, amount_shipment,
                          mass_shipment, size)

            resource_amount = myDict.get('amount_mineral1')
            if resource_amount is not None and resource_amount[0] != 0:
                id_shipment = 5
                class_shipment = 0
                size = int(resource_amount[0])
                amount_shipment = int(resource_amount[0])
                mass_shipment = int(resource_amount[0])
                unloading(session_user, session_user_city, fleet_id, class_shipment, id_shipment, amount_shipment,
                          mass_shipment, size)

            resource_amount = myDict.get('amount_mineral2')
            if resource_amount is not None and resource_amount[0] != 0:
                id_shipment = 6
                class_shipment = 0
                size = int(resource_amount[0])
                amount_shipment = int(resource_amount[0])
                mass_shipment = int(resource_amount[0])
                unloading(session_user, session_user_city, fleet_id, class_shipment, id_shipment, amount_shipment,
                          mass_shipment, size)

            resource_amount = myDict.get('amount_mineral3')
            if resource_amount is not None and resource_amount[0] != 0:
                id_shipment = 7
                class_shipment = 0
                size = int(resource_amount[0])
                amount_shipment = int(resource_amount[0])
                mass_shipment = int(resource_amount[0])
                unloading(session_user, session_user_city, fleet_id, class_shipment, id_shipment, amount_shipment,
                          mass_shipment, size)

            resource_amount = myDict.get('amount_mineral4')
            if resource_amount is not None and resource_amount[0] != 0:
                id_shipment = 8
                class_shipment = 0
                size = int(resource_amount[0])

                amount_shipment = int(resource_amount[0])
                mass_shipment = int(resource_amount[0])
                unloading(session_user, session_user_city, fleet_id, class_shipment, id_shipment, amount_shipment,
                          mass_shipment, size)

            amount_factory = myDict.get('amount_factory')
            if amount_factory is not None:
                id_shipment_fac = myDict.get('hidden_factory')
                len_factory_amount = len(amount_factory)
                for i in range(len_factory_amount):
                    factory_amount = int(amount_factory[i])
                    if factory_amount != 0:
                        id_shipment = int(id_shipment_fac[i])
                        class_shipment = 10
                        factory = Factory_pattern.objects.filter(id=id_shipment).first()
                        size = int(factory.size) * factory_amount
                        amount_shipment = factory_amount
                        mass_shipment = int(factory.mass) * factory_amount
                        unloading(session_user, session_user_city, fleet_id, class_shipment, id_shipment, amount_shipment,
                                  mass_shipment, size)

            amount_hull = myDict.get('amount_hull')
            if amount_hull is not None:
                id_shipment_hull = myDict.get('hidden_hull')
                len_hull_amount = len(amount_hull)
                for i in range(len_hull_amount):
                    hull_amount = int(amount_hull[i])
                    if hull_amount != 0:
                        id_shipment = int(id_shipment_hull[i])
                        class_shipment = 1
                        hull = Hull_pattern.objects.filter(id=id_shipment).first()
                        size = int(hull.size) * hull_amount
                        amount_shipment = hull_amount
                        mass_shipment = int(hull.mass) * hull_amount
                        unloading(session_user, session_user_city, fleet_id, class_shipment, id_shipment, amount_shipment,
                                  mass_shipment, size)

            amount_armor = myDict.get('amount_armor')
            if amount_armor is not None:
                id_shipment_arm = myDict.get('hidden_armor')
                len_armor_amount = len(amount_armor)
                for i in range(len_armor_amount):
                    armor_amount = int(amount_armor[0])
                    if armor_amount != 0:
                        id_shipment = int(id_shipment_arm[i])
                        class_shipment = 2
                        armor = Armor_pattern.objects.filter(id=id_shipment).first()
                        size = 15 * armor_amount
                        amount_shipment = armor_amount
                        mass_shipment = int(armor.mass) * armor_amount
                        unloading(session_user, session_user_city, fleet_id, class_shipment, id_shipment, amount_shipment,
                                  mass_shipment, size)

            amount_shield = myDict.get('amount_shield')
            if amount_shield is not None:
                id_shipment_shield = myDict.get('hidden_shield')
                len_shield_amount = len(amount_shield)
                for i in range(len_shield_amount):
                    shield_amount = int(amount_shield[i])
                    if shield_amount != 0:
                        id_shipment = int(id_shipment_shield[i])
                        class_shipment = 3
                        shield = Shield_pattern.objects.filter(id=id_shipment).first()
                        size = int(shield.size) * shield_amount
                        amount_shipment = shield_amount
                        mass_shipment = int(shield.mass) * shield_amount
                        unloading(session_user, session_user_city, fleet_id, class_shipment, id_shipment, amount_shipment,
                                  mass_shipment, size)

            amount_engine = myDict.get('amount_engine')
            if amount_engine is not None:
                id_shipment_eng = myDict.get('hidden_engine')
                len_engine_amount = len(amount_engine)
                for i in range(len_engine_amount):
                    engine_amount = int(amount_engine[i])
                    if engine_amount != 0:
                        id_shipment = int(id_shipment_eng[i])
                        class_shipment = 4
                        engine = Engine_pattern.objects.filter(id=id_shipment).first()
                        size = int(engine.size) * engine_amount
                        amount_shipment = engine_amount
                        mass_shipment = int(engine.mass) * engine_amount
                        unloading(session_user, session_user_city, fleet_id, class_shipment, id_shipment, amount_shipment,
                                  mass_shipment, size)

            amount_generator = myDict.get('amount_generator')
            if amount_generator is not None:
                id_shipment_gen = myDict.get('hidden_generator')
                len_generator_amount = len(amount_generator)
                for i in range(len_generator_amount):
                    generator_amount = int(amount_generator[i])
                    if generator_amount != 0:
                        id_shipment = int(id_shipment_gen[i])
                        class_shipment = 5
                        generator = Generator_pattern.objects.filter(id=id_shipment).first()
                        size = int(generator.size) * generator_amount
                        amount_shipment = generator_amount
                        mass_shipment = int(generator.mass) * generator_amount
                        unloading(session_user, session_user_city, fleet_id, class_shipment, id_shipment, amount_shipment,
                                  mass_shipment, size)

            amount_weapon = myDict.get('amount_weapon')
            if amount_weapon is not None:
                id_shipment_weap = myDict.get('hidden_weapon')
                len_weapon_amount = len(amount_weapon)
                for i in range(len_weapon_amount):
                    weapon_amount = int(amount_weapon[i])
                    if weapon_amount != 0:
                        id_shipment = int(id_shipment_weap[i])
                        class_shipment = 6
                        weapon = Weapon_pattern.objects.filter(id=id_shipment).first()
                        size = int(weapon.size) * weapon_amount
                        amount_shipment = weapon_amount
                        mass_shipment = int(weapon.mass) * weapon_amount
                        unloading(session_user, session_user_city, fleet_id, class_shipment, id_shipment, amount_shipment,
                                  mass_shipment, size)

            amount_shell = myDict.get('amount_shell')
            if amount_shell is not None:
                id_shipment_shell = myDict.get('hidden_shell')
                len_shell_amount = len(amount_shell)
                for i in range(len_shell_amount):
                    shell_amount = int(amount_shell[i])
                    if shell_amount != 0:
                        id_shipment = int(id_shipment_shell[i])
                        class_shipment = 7
                        shell = Shell_pattern.objects.filter(id=id_shipment).first()
                        size = int(shell.size) * shell_amount
                        amount_shipment = shell_amount
                        mass_shipment = int(shell.mass) * shell_amount
                        unloading(session_user, session_user_city, fleet_id, class_shipment, id_shipment, amount_shipment,
                                  mass_shipment, size)

            amount_module = myDict.get('amount_module')
            if amount_module is not None:
                id_shipment_mod = myDict.get('hidden_module')
                len_module_amount = len(amount_module)
                for i in range(len_module_amount):
                    module_amount = int(amount_module[i])
                    if module_amount != 0:
                        id_shipment = int(id_shipment_mod[i])
                        class_shipment = 8
                        module = Module_pattern.objects.filter(id=id_shipment).first()
                        size = int(module.size) * module_amount
                        amount_shipment = module_amount
                        mass_shipment = int(module.mass) * module_amount
                        unloading(session_user, session_user_city, fleet_id, class_shipment, id_shipment, amount_shipment,
                                  mass_shipment, size)
        else:
            message = 'Флот не над планетой'

        warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).first()
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = User_city.objects.filter(user=int(session_user))
        user_fleets = Fleet.objects.filter(user=session_user)
        ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city)
        ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1)
        warehouse_factorys = Warehouse_factory.objects.filter(user=session_user,
                                                              user_city=session_user_city).order_by(
            'production_class', 'production_id')
        warehouse_elements = Warehouse_element.objects.filter(user=session_user,
                                                              user_city=session_user_city).order_by(
            'element_class', 'element_id')

        command = 2
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouse': warehouse, 'user_city': user_city, 'user_citys': user_citys,
                  'user_fleets': user_fleets, 'add_ships': add_ships, 'fleet_id': fleet_id,
                  'ship_fleets': ship_fleets,
                  'ships': ships, 'command': command, 'flightplans': flightplans,
                  'flightplan_flights': flightplan_flights, 'warehouse_factorys': warehouse_factorys,
                  'factory_patterns': factory_patterns, 'warehouse_elements': warehouse_elements,
                  'hull_patterns': hull_patterns, 'armor_patterns': armor_patterns,
                  'shield_patterns': shield_patterns,
                  'engine_patterns': engine_patterns, 'generator_patterns': generator_patterns,
                  'module_patterns': module_patterns, 'message': message, 'ship_holds': ship_holds}
        return render(request, "fleet_hold.html", output)


def unloading(*args):
    session_user = args[0]
    session_user_city = args[1]
    fleet_id = args[2]
    class_shipment = args[3]
    id_shipment = args[4]
    amount_shipment = args[5]
    mass_shipment = args[6]
    size = args[7]

    hold = Hold.objects.filter(fleet_id=fleet_id, class_shipment=class_shipment, id_shipment=id_shipment).first()
    hold_amount_shipment = hold.amount_shipment

    if class_shipment == 0:
        warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).first()
        if id_shipment == 1:
            amount_resource = warehouse.resource1
            new_amount = amount_resource + amount_shipment
            warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).update(
                resource1=new_amount)
        elif id_shipment == 2:
            amount_resource = warehouse.resource2
            new_amount = amount_resource + amount_shipment
            warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).update(
                resource2=new_amount)
        elif id_shipment == 3:
            amount_resource = warehouse.resource3
            new_amount = amount_resource + amount_shipment
            warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).update(
                resource3=new_amount)
        elif id_shipment == 4:
            amount_resource = warehouse.resource4
            new_amount = amount_resource + amount_shipment
            warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).update(
                resource4=new_amount)
        elif id_shipment == 5:
            amount_resource = warehouse.mineral1
            new_amount = amount_resource + amount_shipment
            warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).update(
                mineral1=new_amount)
        elif id_shipment == 6:
            amount_resource = warehouse.mineral2
            new_amount = amount_resource + amount_shipment
            warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).update(
                mineral2=new_amount)
        elif id_shipment == 7:
            amount_resource = warehouse.mineral3
            new_amount = amount_resource + amount_shipment
            warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).update(
                mineral3=new_amount)
        elif id_shipment == 8:
            amount_resource = warehouse.mineral1
            new_amount = amount_resource + amount_shipment
            warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).update(
                mineral4=new_amount)

        mass = amount_shipment
        size = amount_shipment

    elif class_shipment == 10:
        warehouse_factory = Warehouse_factory.objects.filter(user=session_user, user_city=session_user_city,
                                                             factory_id=id_shipment).first()
        amount_factory = warehouse_factory.amount
        new_amount = amount_factory + amount_shipment
        warehouse_factory = Warehouse_factory.objects.filter(user=session_user, user_city=session_user_city,
                                                             factory_id=id_shipment).update(amount=new_amount)
        mass = amount_shipment * warehouse_factory.mass
        size = amount_shipment * warehouse_factory.size

    else:
        element = Warehouse_element.objects.filter(user=session_user, user_city=session_user_city,
                                                   element_class=class_shipment, element_id=id_shipment).first()
        amount_element = element.amount
        new_amount = amount_shipment + amount_element
        element = Warehouse_element.objects.filter(user=session_user, user_city=session_user_city,
                                                   element_class=class_shipment, element_id=id_shipment).update(
            amount=new_amount)
        hold = Hold.objects.filter(fleet_id=fleet_id, class_shipment=class_shipment, id_shipment=id_shipment).first()
        mass = amount_shipment * (hold.mass_shipment / hold.amount_shipment)
        size = amount_shipment * (hold.size_shipment / hold.amount_shipment)

    if hold_amount_shipment == amount_shipment:
        hold = Hold.objects.filter(fleet_id=fleet_id, class_shipment=class_shipment, id_shipment=id_shipment).delete()
    else:
        new_amount = hold.amount_shipment - amount_shipment

        new_mass = hold.mass_shipment - amount_shipment * (hold.mass_shipment / hold.amount_shipment)
        new_size = hold.size_shipment - amount_shipment * (hold.size_shipment / hold.amount_shipment)

        hold = Hold.objects.filter(fleet_id=fleet_id, class_shipment=class_shipment, id_shipment=id_shipment).update(
            amount_shipment=new_amount, mass_shipment=new_mass, size_shipment=new_size)
    fleet = Fleet.objects.filter(id=fleet_id).first()
    empty_hold = fleet.empty_hold
    ship_empty_mass = fleet.ship_empty_mass
    new_empty_hold = empty_hold + size
    new_ship_empty_mass = ship_empty_mass - mass
    fleet = Fleet.objects.filter(id=fleet_id).update(empty_hold=new_empty_hold, ship_empty_mass=new_ship_empty_mass)
