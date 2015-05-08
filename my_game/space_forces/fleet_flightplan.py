# -*- coding: utf-8 -*-

from datetime import datetime
from django.shortcuts import render
from my_game.models import MyUser, User_city
from my_game.models import Warehouse
from my_game import function
from my_game.models import Ship, Fleet, Fleet_parametr_scan, Fleet_engine, Fleet_parametr_resource_extraction
from my_game.models import Flightplan, Flightplan_flight, Flightplan_scan, Flightplan_production, Flightplan_hold, \
    Flightplan_refill, Flightplan_build_repair, Fleet_parametr_build_repair, Flightplan_colonization, Device_pattern
from my_game.flightplan.create import flight, scan, upload_hold, unload_hold, refill, repair_build
from my_game.flightplan.create import resource_extraction
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

            extraction = request.POST.get('resource_extraction')
            if extraction:
                time_extraction = request.POST.get('time_extraction')
                full_hold = request.POST.get('full_hold')
                resource_extraction.resource_extraction(session_user, fleet_id, fleet, time_extraction, full_hold)

            scaning = request.POST.get('scan')
            if scaning:
                method_scanning = int(request.POST.get('scaning'))
                scan.scan(session_user, fleet_id, method_scanning)

            upload = request.POST.get('upload_hold')
            if upload:
                upload_amount = int(request.POST.get('upload_amount'))
                name_upload_element = request.POST.get('name_upload_element')
                upload_hold.upload_hold(session_user, fleet_id, upload_amount, name_upload_element)

            unload = request.POST.get('unload_hold')
            if unload:
                unload_all = request.POST.get('unload_all')
                unload_all_hold = request.POST.get('unload_all_hold')
                unload_amount = request.POST.get('unload_amount')
                id_hold_element = request.POST.get('id_hold_element')
                unload_hold.unload_hold(session_user, fleet_id, unload_all, unload_all_hold, unload_amount,
                                        id_hold_element)

            refill_fleet = request.POST.get('refill_fleet')
            overload = request.POST.get('overload')
            yourself = request.POST.get('yourself')
            if refill_fleet is not None or overload is not None or yourself is not None:
                refill.refill(session_user, fleet_id, request)

            repair = request.POST.get('repair')
            build = request.POST.get('build')
            if build is not None or repair is not None:
                repair_build.repair_build(session_user, fleet_id, request)

            colonization = request.POST.get('colonization')
            if colonization:
                ships = Ship.objects.filter()

                id_command = 1
                flightplan = Flightplan(
                    user=session_user,
                    id_fleet=fleet_id,
                    class_command=8,
                    id_command=id_command,
                    status=0
                )
                flightplan.save()

                hold = Hold.objects.filter(fleet_id=fleet_id, class_shipment=9).first()
                colonization_module = Device_pattern.objects.filter(id=hold.id_shipment).first()

                flightplan_colonization = Flightplan_colonization(
                    id_fleet=fleet_id,
                    id_command=id_command,
                    id_fleetplan=flightplan.id,
                    start_time=datetime.now(),
                    time=colonization_module.param1,
                )
                flightplan_colonization.save()

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
        flightplan_colonization = Flightplan_colonization.objects.filter(id_fleet=fleet_id).order_by('id')
        fleet_engine = Fleet_engine.objects.filter(fleet_id=fleet_id).first()
        fleet_parametr_scans = Fleet_parametr_scan.objects.filter(fleet_id=fleet_id)
        fleet_parametr_resource_extraction = Fleet_parametr_resource_extraction.objects.filter(
            fleet_id=fleet_id).first()
        fleet_parametr_builds = Fleet_parametr_build_repair.objects.filter(fleet_id=fleet_id,
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
        device_patterns = Device_pattern.objects.filter(user=session_user)
        ship_holds = Hold.objects.filter(fleet_id=fleet_id).order_by('class_shipment')
        add_ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city)
        ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city)

        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True

        output = {'user': user, 'warehouses': warehouses, 'user_city': user_city, 'user_citys': user_citys,
                  'user_fleets': user_fleets, 'add_ships': add_ships, 'fleet_id': fleet_id,
                  'ship_fleets': ship_fleets, 'ships': ships, 'fleet': fleet, 'command': command,
                  'flightplans': flightplans, 'flightplan_flights': flightplan_flights,
                  'warehouse_factorys': warehouse_factorys, 'factory_patterns': factory_patterns,
                  'warehouse_elements': warehouse_elements, 'hull_patterns': hull_patterns,
                  'armor_patterns': armor_patterns, 'shield_patterns': shield_patterns,
                  'device_patterns': device_patterns, 'engine_patterns': engine_patterns,
                  'generator_patterns': generator_patterns, 'weapon_patterns': weapon_patterns,
                  'shell_patterns': shell_patterns, 'fuel_patterns': fuel_patterns,
                  'flightplan_scans': flightplan_scans, 'flightplan_productions': flightplan_productions,
                  'fleet_engine': fleet_engine, 'basic_resources': basic_resources, 'module_patterns': module_patterns,
                  'fleet_parametr_scans': fleet_parametr_scans,
                  'fleet_parametr_resource_extraction': fleet_parametr_resource_extraction, 'ship_holds': ship_holds,
                  'message': message, 'flightplan_holds': flightplan_holds, 'flightplan_refills': flightplan_refills,
                  'fleet_parametr_builds': fleet_parametr_builds, 'fleet_parametr_repair': fleet_parametr_repair,
                  'flightplan_build_repairs': flightplan_build_repairs,
                  'flightplan_colonization': flightplan_colonization}

        return render(request, "flightplan.html", output)


