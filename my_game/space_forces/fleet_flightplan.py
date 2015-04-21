# -*- coding: utf-8 -*-

from datetime import datetime
from django.shortcuts import render
from my_game.models import MyUser, User_city
from my_game.models import Warehouse
from my_game import function
from my_game.models import Ship, Fleet, Fleet_parametr_scan, Fleet_engine, Fleet_parametr_resource_extraction
from my_game.models import Flightplan, Flightplan_flight, Flightplan_scan, Flightplan_production, Flightplan_hold, \
    Flightplan_refill, Flightplan_build_repair, Fleet_parametr_build_repair
from space_forces import flight
from my_game.models import Hull_pattern, Armor_pattern, Shell_pattern, Shield_pattern, Weapon_pattern, \
    Warehouse_factory, Warehouse_element, Factory_pattern, Engine_pattern, Generator_pattern, Module_pattern, \
    Basic_resource, Hold, Fuel_pattern


def fleet_flightplan(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        fleet_id = int(request.POST.get('hidden_fleet'))
        fleet_engine = Fleet_engine.objects.filter(fleet_id=fleet_id).first()
        fleet = Fleet.objects.filter(id=fleet_id).first()
        command = 0
        message = ''
        if request.POST.get('add_command'):
            command = 3
            answer = request

            city = request.POST.get('city')
            coordinate = request.POST.get('coordinate')
            if city or coordinate:
                flight.flight_system(session_user, session_user_city, answer)

            resource_extraction = request.POST.get('resource_extraction')
            if resource_extraction:
                time_extraction = request.POST.get('time_extraction')
                full_hold = request.POST.get('full_hold')

                fleet_parametr_resource_extraction = Fleet_parametr_resource_extraction.objects.filter(
                    fleet_id=fleet_id).first()
                if full_hold:
                    time_extraction = int(fleet.empty_hold / fleet_parametr_resource_extraction.extraction_per_minute)

                flightplan = Flightplan(
                    user=session_user,
                    id_fleet=fleet_id,
                    class_command=3,
                    id_command=1,
                    status=0
                )
                flightplan.save()

                flightplan_production = Flightplan_production(
                    user=session_user,
                    id_fleet=fleet_id,
                    id_fleetplan=flightplan.id,
                    id_command=1,
                    production_per_minute=fleet_parametr_resource_extraction.extraction_per_minute,
                    time_extraction=time_extraction
                )
                flightplan_production.save()

            scan = request.POST.get('scan')
            if scan:
                method_scanning = int(request.POST.get('scaning'))
                fleet_parametr_scan = Fleet_parametr_scan.objects.filter(fleet_id=fleet_id,
                                                                         method_scanning=method_scanning).first()
                flightplan = Flightplan(
                    user=session_user,
                    id_fleet=fleet_id,
                    class_command=6,
                    id_command=method_scanning,
                    status=0
                )
                flightplan.save()

                flightplan_scan = Flightplan_scan(
                    user=session_user,
                    id_fleet=fleet_id,
                    id_command=method_scanning,
                    range_scanning=fleet_parametr_scan.range_scanning,
                    start_time=datetime.now(),
                    time_scanning=fleet_parametr_scan.time_scanning,
                    id_fleetplan=flightplan.id
                )
                flightplan_scan.save()

            upload_hold = request.POST.get('upload_hold')
            if upload_hold:
                upload_amount = int(request.POST.get('upload_amount'))
                name_upload_element = request.POST.get('name_upload_element')
                name_upload_element = name_upload_element.split(';')
                id_element = int(name_upload_element[0])
                class_element = int(name_upload_element[1])
                name = find_name(class_element, id_element)

                flightplan = Flightplan(
                    user=session_user,
                    id_fleet=fleet_id,
                    class_command=2,
                    id_command=1,
                    status=0
                )
                flightplan.save()

                flightplan_hold = Flightplan_hold(
                    user=session_user,
                    id_fleet=fleet_id,
                    id_command=1,
                    amount=upload_amount,
                    start_time=datetime.now(),
                    id_fleetplan=flightplan.id,
                    time=300,
                    class_element=class_element,
                    id_element=id_element,
                    name=name
                )
                flightplan_hold.save()

            unload_hold = request.POST.get('unload_hold')
            if unload_hold:
                unload_all = request.POST.get('unload_all')
                unload_all_hold = request.POST.get('unload_all_hold')
                unload_amount = request.POST.get('unload_amount')
                id_hold_element = request.POST.get('id_hold_element')
                hold = Hold.objects.filter(id=id_hold_element).first()
                class_element = hold.class_shipment
                id_element = hold.id_shipment

                name = find_name(class_element, id_element)
                error = 0
                if unload_all_hold:
                    id_command = 4
                    unload_amount = 0
                    class_element = 0
                    id_element = 0
                    time = 600
                elif unload_all:
                    id_command = 3
                    unload_amount = hold.amount_shipment
                    class_element = 0
                    id_element = id_hold_element
                    time = 300
                else:
                    if unload_amount:
                        id_command = 2
                        class_element = hold.class_shipment
                        id_element = hold.id_shipment
                        time = 150
                    else:
                        message = ''
                        error = 1
                if error == 0:
                    flightplan = Flightplan(
                        user=session_user,
                        id_fleet=fleet_id,
                        class_command=2,
                        id_command=id_command,
                        status=0
                    )
                    flightplan.save()

                    flightplan_hold = Flightplan_hold(
                        user=session_user,
                        id_fleet=fleet_id,
                        id_command=id_command,
                        amount=unload_amount,
                        start_time=datetime.now(),
                        id_fleetplan=flightplan.id,
                        time=time,
                        class_element=class_element,
                        id_element=id_element,
                        name=name
                    )
                    flightplan_hold.save()

            refill_fleet = request.POST.get('refill_fleet')
            overload = request.POST.get('overload')
            yourself = request.POST.get('yourself')
            if refill_fleet is not None or overload is not None or yourself is not None:
                if yourself:
                    id_command = 1
                    id_fleet_refill = fleet_id
                    amount = request.POST.get('yourself_amount')
                    class_element = 14
                    id_fuel_yourself = request.POST.get('id_fuel_yourself')
                    id_fuel_yourself = id_fuel_yourself.split(';')
                    id_element = id_fuel_yourself[0]
                    class_refill = 1
                    time = 150
                    name = find_name(class_element, id_element)
                    yourself_full_tank = request.POST.get('yourself_full_tank')
                    if yourself_full_tank:
                        class_refill = 2
                        amount = 0
                        time = 300

                if refill_fleet:
                    id_command = 2
                    id_fleet_refill = request.POST.get('fleet_number')
                    id_element = request.POST.get('id_fuel')
                    amount = request.POST.get('amount')
                    hold = Hold.objects.filter(id=id_element).first()
                    name = find_name(hold.class_shipment, hold.id_shipment)
                    class_refill = 1
                    class_element = 0
                    time = 150
                    full_tank = request.POST.get('full_tank')
                    if full_tank:
                        class_refill = 2
                        amount = 0
                        time = 300

                elif overload:
                    id_command = 3
                    id_element = request.POST.get('id_hold_element')
                    amount = request.POST.get('overload_amount')
                    id_fleet_refill = request.POST.get('overload_fleet_number')
                    hold = Hold.objects.filter(id=id_element).first()
                    name = find_name(hold.class_shipment, hold.id_shipment)
                    class_refill = 1
                    class_element = 0
                    time = 300
                    all_goods = request.POST.get('all_goods')
                    if all_goods:
                        class_refill = 2
                        amount = 0
                        time = 450

                flightplan = Flightplan(
                    user=session_user,
                    id_fleet=fleet_id,
                    class_command=4,
                    id_command=id_command,
                    status=0
                )
                flightplan.save()

                flightplan_refill = Flightplan_refill(
                    user=session_user,
                    id_fleet=fleet_id,
                    id_command=id_command,
                    id_fleet_refill=id_fleet_refill,
                    class_refill=class_refill,
                    class_element=class_element,
                    id_element=id_element,
                    amount=amount,
                    start_time=datetime.now(),
                    time_refill=time,
                    id_fleetplan=flightplan.id,
                    name=name
                )
                flightplan_refill.save()

            repair = request.POST.get('repair')
            build = request.POST.get('build')
            if build is not None or repair is not None:
                if build:
                    id_hold_factory = request.POST.get('id_factory')
                    id_command = 5
                    fleet_repair = 0

                    hold = Hold.objects.filter(id=id_hold_factory).first()
                    factory = Factory_pattern.objects.filter(id=hold.id_shipment).first().time_deployment
                    fleet_parametr_build = Fleet_parametr_build_repair.objects.filter(fleet_id=fleet_id,
                                                                                      class_process=1).first().process_per_minute
                    time = factory * fleet_parametr_build

                if repair:
                    fleet_repair = request.POST.get('fleet_number')
                    repair_yourself = request.POST.get('repair_yourself')
                    id_command = 7
                    if repair_yourself:
                        fleet_repair = fleet_id
                    time = 0

                flightplan = Flightplan(
                    user=session_user,
                    id_fleet=fleet_id,
                    class_command=id_command,
                    id_command=id_command,
                    status=0
                )
                flightplan.save()

                flightplan_build_repair = Flightplan_build_repair(
                    id_fleet=fleet_id,
                    id_fleetplan=flightplan.id,
                    id_command=id_command,
                    fleet_repair=fleet_repair,
                    start_time=datetime.now(),
                    time=time,
                )
                flightplan_build_repair.save()

        if request.POST.get('delete_command'):
            command = 3
            fleet_id = int(request.POST.get('hidden_fleet'))
            hidden_flightplan_id = int(request.POST.get('hidden_flightplan_id'))
            flightplan = Flightplan.objects.filter(id=hidden_flightplan_id).first()
            if flightplan.class_command == 1:
                flightplan_flight = Flightplan_flight.objects.filter(id_fleetplan=flightplan.id).delete()
            if flightplan.class_command == 2:
                flightplan_hold = Flightplan_hold.objects.filter(id_fleetplan=flightplan.id).delete()
            if flightplan.class_command == 3:
                flightplan_scan = Flightplan_scan.objects.filter(id_fleetplan=flightplan.id).delete()
            if flightplan.class_command == 4:
                flightplan_scan = Flightplan_refill.objects.filter(id_fleetplan=flightplan.id).delete()
            if flightplan.class_command == 6:
                flightplan_production = Flightplan_production.objects.filter(id_fleetplan=flightplan.id).delete()
            flightplan = Flightplan.objects.filter(id=hidden_flightplan_id).delete()

        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('id_resource')
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = User_city.objects.filter(user=int(session_user))
        user_fleets = Fleet.objects.filter(user=session_user)
        ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1)
        flightplans = Flightplan.objects.filter(id_fleet=fleet_id).order_by('id')
        flightplan_flights = Flightplan_flight.objects.filter(id_fleet=fleet_id).order_by('id')
        flightplan_scans = Flightplan_scan.objects.filter(id_fleet=fleet_id).order_by('id')
        flightplan_productions = Flightplan_production.objects.filter(id_fleet=fleet_id).order_by('id')
        flightplan_holds = Flightplan_hold.objects.filter(id_fleet=fleet_id).order_by('id')
        flightplan_refills = Flightplan_refill.objects.filter(id_fleet=fleet_id).order_by('id')
        flightplan_build_repairs = Flightplan_build_repair.objects.filter(id_fleet=fleet_id).order_by('id')
        fleet_engine = Fleet_engine.objects.filter(fleet_id=fleet_id).first()
        fleet_parametr_scans = Fleet_parametr_scan.objects.filter(fleet_id=fleet_id)
        fleet_parametr_resource_extraction = Fleet_parametr_resource_extraction.objects.filter(
            fleet_id=fleet_id).first()
        fleet_parametr_build = Fleet_parametr_build_repair.objects.filter(fleet_id=fleet_id,
                                                                          class_process=1).first()
        fleet_parametr_repair = Fleet_parametr_build_repair.objects.filter(fleet_id=fleet_id,
                                                                           class_process=2).first()
        warehouse_factorys = Warehouse_factory.objects.filter(user=session_user,
                                                              user_city=session_user_city).order_by(
            'production_class', 'production_id')
        warehouse_elements = Warehouse_element.objects.filter(user=session_user,
                                                              user_city=session_user_city).order_by(
            'element_class', 'element_id')
        factory_patterns = Factory_pattern.objects.filter(user=session_user)
        hull_patterns = Hull_pattern.objects.filter(user=session_user)
        armor_patterns = Armor_pattern.objects.filter(user=session_user)
        shield_patterns = Shield_pattern.objects.filter(user=session_user)
        engine_patterns = Engine_pattern.objects.filter(user=session_user)
        generator_patterns = Generator_pattern.objects.filter(user=session_user)
        weapon_patterns = Weapon_pattern.objects.filter(user=session_user)
        shell_patterns = Shell_pattern.objects.filter(user=session_user)
        module_patterns = Module_pattern.objects.filter(user=session_user)
        basic_resources = Basic_resource.objects.all()
        fuel_patterns = Fuel_pattern.objects.filter(user=session_user)
        # device_patterns = Device_pattern.objects.filter(user = session_user)
        ship_holds = Hold.objects.filter(fleet_id=fleet_id).order_by('class_shipment')
        add_ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city)
        ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city)

        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True

        output = {'user': user, 'warehouses': warehouses, 'user_city': user_city, 'user_citys': user_citys,
                  'user_fleets': user_fleets, 'add_ships': add_ships, 'fleet_id': fleet_id,
                  'ship_fleets': ship_fleets, 'ships': ships, 'fleet': fleet,
                  'command': command, 'flightplans': flightplans, 'flightplan_flights': flightplan_flights,
                  'warehouse_factorys': warehouse_factorys, 'factory_patterns': factory_patterns,
                  'warehouse_elements': warehouse_elements, 'hull_patterns': hull_patterns,
                  'armor_patterns': armor_patterns, 'shield_patterns': shield_patterns,
                  'engine_patterns': engine_patterns, 'generator_patterns': generator_patterns,
                  'weapon_patterns': weapon_patterns, 'shell_patterns': shell_patterns, 'fuel_patterns': fuel_patterns,
                  'flightplan_scans': flightplan_scans, 'flightplan_productions': flightplan_productions,
                  'fleet_engine': fleet_engine, 'basic_resources': basic_resources,
                  'module_patterns': module_patterns, 'fleet_parametr_scans': fleet_parametr_scans,
                  'fleet_parametr_resource_extraction': fleet_parametr_resource_extraction,
                  'ship_holds': ship_holds, 'message': message, 'flightplan_holds': flightplan_holds,
                  'flightplan_refills': flightplan_refills, 'fleet_parametr_build': fleet_parametr_build,
                  'fleet_parametr_repair': fleet_parametr_repair, 'flightplan_build_repairs':flightplan_build_repairs}

        return render(request, "flightplan.html", output)


def find_name(*args):
    class_element = args[0]
    id_element = args[1]
    name = ''
    if class_element == 0:
        resource = Basic_resource.objects.filter(id=id_element).first()
        name = resource.name

    elif class_element == 1:
        hull = Hull_pattern.objects.filter(id=id_element).first()
        name = hull.name

    elif class_element == 2:
        armor = Armor_pattern.objects.filter(id=id_element).first()
        name = armor.name

    elif class_element == 3:
        shield = Shield_pattern.objects.filter(id=id_element).first()
        name = shield.name

    elif class_element == 4:
        engine = Engine_pattern.objects.filter(id=id_element).first()
        name = engine.name

    elif class_element == 5:
        generator = Generator_pattern.objects.filter(id=id_element).first()
        name = generator.name

    elif class_element == 6:
        weapon = Weapon_pattern.objects.filter(id=id_element).first()
        name = weapon.name

    elif class_element == 7:
        shell = Shell_pattern.objects.filter(id=id_element).first()
        name = shell.name

    elif class_element == 8:
        module = Module_pattern.objects.filter(id=id_element).first()
        name = module.name

    elif class_element == 10:
        factory = Factory_pattern.objects.filter(id=id_element).first()
        name = factory.name

    elif class_element == 14:
        factory = Fuel_pattern.objects.filter(id=id_element).first()
        name = factory.name
    return name