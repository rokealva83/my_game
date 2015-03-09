from django.shortcuts import render
from my_game.models import MyUser, User_city
from my_game.models import Warehouse, Warehouse_element, Warehouse_factory, Warehouse_ship
from my_game import function
from my_game.models import Project_ship, Ship, Fleet, Hold
from my_game.models import Flightplan, Flightplan_flight
from my_game.models import Factory_pattern, Hull_pattern, Armor_pattern, Shell_pattern, Shield_pattern, \
    Generator_pattern, Weapon_pattern, Engine_pattern, Module_pattern


def fleet_hold(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)

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
            factory = Factory_pattern.objects.filter(id=id_shipment).first()
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
            hull = Hull_pattern.objects.filter(id=id_shipment).first()
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
            armor = Armor_pattern.objects.filter(id=id_shipment).first()
            size = armor.size * int(armor_amount[0])
            if size <= fleet.empty_hold:
                amount_shipment = int(armor_amount[0])
                mass_shipment = armor.mass * int(armor_amount[0])
                add_shipment = 1

        shield_amount = myDict.get('shield_amount')
        id_shipment_shield = myDict.get('warehouse_shield')
        if int(shield_amount[0]) != 0 and add_shipment == 0 and id_shipment_shield is not None:
            id_shipment = int(id_shipment_shield[0])
            class_shipment = 3
            shield = Shield_pattern.objects.filter(id=id_shipment).first()
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
            engine = Engine_pattern.objects.filter(id=id_shipment).first()
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
            generator = Generator_pattern.objects.filter(id=id_shipment).first()
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
            weapon = Weapon_pattern.objects.filter(id=id_shipment).first()
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
            shell = Shell_pattern.objects.filter(id=id_shipment).first()
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
            module = Module_pattern.objects.filter(id=id_shipment).first()
            size = module.size * int(module_amount[0])
            if size <= fleet.empty_hold:
                amount_shipment = int(module_amount[0])
                mass_shipment = module.mass * int(module_amount[0])
                add_shipment = 1

        if add_shipment != 0:

            warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).first()
            if class_shipment == 0:

                if id_shipment == 1:
                    if warehouse.resource1 >= amount_shipment:
                        new_resource1 = warehouse.resource1 - amount_shipment
                        warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).update(
                            resource1=new_resource1)
                    else:
                        error = 1

                elif id_shipment == 2:
                    if warehouse.resource2 >= amount_shipment:
                        new_resource2 = warehouse.resource2 - amount_shipment
                        warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).update(
                            resource2=new_resource2)
                    else:
                        error = 1

                elif id_shipment == 3:
                    if warehouse.resource3 >= amount_shipment:
                        new_resource3 = warehouse.resource3 - amount_shipment
                        warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).update(
                            resource3=new_resource3)
                    else:
                        error = 1

                elif id_shipment == 4:
                    if warehouse.resource4 >= amount_shipment:
                        new_resource4 = warehouse.resource4 - amount_shipment
                        warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).update(
                            resource4=new_resource4)
                    else:
                        error = 1

                elif id_shipment == 5:
                    if warehouse.mineral1 >= amount_shipment:
                        new_mineral1 = warehouse.mineral1 - amount_shipment
                        warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).update(
                            mineral1=new_mineral1)
                    else:
                        error = 1

                elif id_shipment == 6:
                    if warehouse.mineral2 >= amount_shipment:
                        new_mineral2 = warehouse.mineral2 - amount_shipment
                        warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).update(
                            mineral2=new_mineral2)
                    else:
                        error = 1
                elif id_shipment == 7:
                    if warehouse.mineral3 >= amount_shipment:
                        new_mineral3 = warehouse.mineral3 - amount_shipment
                        warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).update(
                            mineral3=new_mineral3)
                    else:
                        error = 1
                elif id_shipment == 8:
                    if warehouse.mineral4 >= amount_shipment:
                        new_mineral4 = warehouse.mineral4 - amount_shipment
                        warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).update(
                            mineral4=new_mineral4)
                    else:
                        error = 1

            elif class_shipment == 10:
                warehouse_factory = Warehouse_factory.objects.filter(user_city=session_user_city,
                                                                     factory_id=id_shipment).first()
                if warehouse_factory.amount >= amount_shipment:
                    new_factory_amount = warehouse_factory.amount - amount_shipment
                    warehouse_factory = Warehouse_factory.objects.filter(user_city=session_user_city,
                                                                         factory_id=id_shipment).update(
                        amount=new_factory_amount)
                else:
                    error = 1

            elif 0 < class_shipment < 10:
                warehouse_element = Warehouse_element.objects.filter(user_city=session_user_city,
                                                                     element_class=class_shipment,
                                                                     element_id=id_shipment).first()
                if warehouse_element.amount >= amount_shipment:
                    new_element_amount = warehouse_element.amount - amount_shipment
                    warehouse_element = Warehouse_element.objects.filter(user_city=session_user_city,
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

            warehouse = Warehouse.objects.filter(user=session_user, user_city=session_user_city).first()
            user_city = User_city.objects.filter(user=session_user).first()
            user = MyUser.objects.filter(user_id=session_user).first()
            user_citys = User_city.objects.filter(user=int(session_user))
            user_fleets = Fleet.objects.filter(user=session_user)
            ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city)
            ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1)
            command = 0
            request.session['userid'] = session_user
            request.session['user_city'] = session_user_city
            request.session['live'] = True
            output = {'user': user, 'warehouse': warehouse, 'user_city': user_city, 'user_citys': user_citys,
                      'user_fleets': user_fleets, 'ships': ships, 'ship_fleets': ship_fleets, 'command': command}
            return render(request, "fleet_hold.html", output)