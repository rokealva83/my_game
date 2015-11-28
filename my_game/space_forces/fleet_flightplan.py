# -*- coding: utf-8 -*-

from datetime import datetime
from django.shortcuts import render
from my_game.models import UserCity, MyUser
from my_game import function
from my_game.models import Ship, Fleet, FleetParametrScan, FleetEngine, FleetParametrResourceExtraction
from my_game.models import Flightplan, FlightplanFlight, FlightplanScan, FlightplanProduction, FlightplanHold, \
    FlightplanRefill, FlightplanBuildRepair, FleetParametrBuildRepair, FlightplanColonization, DevicePattern
from my_game.flightplan.create import flight, scan, upload_hold, unload_hold, refill, repair_build
from my_game.flightplan.create import resource_extraction
from my_game.models import HullPattern, ArmorPattern, ShellPattern, ShieldPattern, WeaponPattern, \
    WarehouseFactory, WarehouseElement, FactoryPattern, EnginePattern, GeneratorPattern, ModulePattern, \
    BasicResource, Hold, FuelPattern
from my_game.models import ResourceHold


def fleet_flightplan(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        function.check_all_queues(session_user)
        fleet = Fleet.objects.filter(id=int(request.POST.get('hidden_fleet'))).first()
        command = 0
        message = ''
        if request.POST.get('add_command'):
            command = 3
            answer = request

            city = request.POST.get('city')
            coordinate = request.POST.get('coordinate')
            if city or coordinate:
                message = flight.flight_system(session_user, session_user_city, fleet, answer)

            extraction = request.POST.get('resource_extraction')
            if extraction:
                time_extraction = request.POST.get('time_extraction')
                full_hold = request.POST.get('full_hold')
                resource_extraction.resource_extraction(session_user, fleet, time_extraction, full_hold)

            scaning = request.POST.get('scan')
            if scaning:
                method_scanning = int(request.POST.get('scaning'))
                scan.scan(session_user, fleet, method_scanning)

            upload = request.POST.get('upload_hold')
            if upload:
                upload_amount = int(request.POST.get('upload_amount'))
                name_upload_element = request.POST.get('name_upload_element')
                upload_hold.upload_hold(session_user, fleet, upload_amount, name_upload_element)

            unload = request.POST.get('unload_hold')
            if unload:
                unload_all = request.POST.get('unload_all')
                unload_all_hold = request.POST.get('unload_all_hold')
                unload_amount = request.POST.get('unload_amount')
                id_hold_element = request.POST.get('id_hold_element')
                unload_hold.unload_hold(session_user, fleet, unload_all, unload_all_hold, unload_amount,
                                        id_hold_element)

            refill_fleet = request.POST.get('refill_fleet')
            overload = request.POST.get('overload')
            yourself = request.POST.get('yourself')
            if refill_fleet is not None or overload is not None or yourself is not None:
                refill.refill(session_user, fleet, request)

            repair = request.POST.get('repair')
            build = request.POST.get('build')
            if build is not None or repair is not None:
                repair_build.repair_build(session_user, fleet, request)

            colonization = request.POST.get('colonization')
            if colonization:
                command_id = 1
                hold = Hold.objects.filter(fleet=fleet, class_shipment=9).first()
                if hold:
                    colonization_module = DevicePattern.objects.filter(id=hold.id_shipment).first()
                    flightplan = Flightplan(
                        user=session_user,
                        fleet=fleet,
                        class_command=8,
                        command_id=command_id,
                        status=0
                    )
                    flightplan.save()

                    flightplan_colonization = FlightplanColonization(
                        fleet=fleet,
                        command_id=command_id,
                        fleetplan=flightplan,
                        start_time=datetime.now(),
                        time=colonization_module.param1,
                    )
                    flightplan_colonization.save()

        if request.POST.get('delete_command'):
            command = 3
            fleet = int(request.POST.get('hidden_fleet'))
            hidden_flightplan_id = int(request.POST.get('hidden_flightplan_id'))
            flightplan = Flightplan.objects.filter(id=hidden_flightplan_id).first()
            if flightplan.class_command == 1:
                FlightplanFlight.objects.filter(fleetplan=flightplan).delete()
            if flightplan.class_command == 2:
                FlightplanHold.objects.filter(fleetplan=flightplan).delete()
            if flightplan.class_command == 6:
                FlightplanScan.objects.filter(fleetplan=flightplan).delete()
            if flightplan.class_command == 4:
                FlightplanRefill.objects.filter(fleetplan=flightplan).delete()
            if flightplan.class_command == 3:
                FlightplanProduction.objects.filter(fleetplan=flightplan).delete()
            flightplan.delete()

        user_city = UserCity.objects.filter(user=session_user).first()
        user_citys = UserCity.objects.filter(user=int(session_user))
        user_fleets = Fleet.objects.filter(user=session_user)
        ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1)
        flightplans = Flightplan.objects.filter(fleet=fleet).order_by('id')
        flightplan_flights = FlightplanFlight.objects.filter(fleet=fleet).order_by('id')
        flightplan_scans = FlightplanScan.objects.filter(fleet=fleet).order_by('id')
        flightplan_productions = FlightplanProduction.objects.filter(fleet=fleet).order_by('id')
        flightplan_holds = FlightplanHold.objects.filter(fleet=fleet).order_by('id')
        flightplan_refills = FlightplanRefill.objects.filter(fleet=fleet).order_by('id')
        flightplan_build_repairs = FlightplanBuildRepair.objects.filter(fleet=fleet).order_by('id')
        flightplan_colonization = FlightplanColonization.objects.filter(fleet=fleet).order_by('id')
        fleet_engine = FleetEngine.objects.filter(fleet=fleet).first()
        fleet_parametr_scans = FleetParametrScan.objects.filter(fleet=fleet)
        fleet_parametr_resource_extraction = FleetParametrResourceExtraction.objects.filter(
            fleet=fleet).first()
        fleet_parametr_builds = FleetParametrBuildRepair.objects.filter(fleet=fleet,
                                                                        class_process=1).first()
        fleet_parametr_repair = FleetParametrBuildRepair.objects.filter(fleet=fleet,
                                                                        class_process=2).first()
        warehouse_factorys = WarehouseFactory.objects.filter(user=session_user,
                                                             user_city=session_user_city).order_by(
            'production_class', 'production_id')
        warehouse_elements = WarehouseElement.objects.filter(user=session_user,
                                                             user_city=session_user_city).order_by(
            'element_class', 'element_id')
        factory_patterns = FactoryPattern.objects.filter(user=session_user)
        hull_patterns = HullPattern.objects.filter(user=session_user)
        armor_patterns = ArmorPattern.objects.filter(user=session_user)
        shield_patterns = ShieldPattern.objects.filter(user=session_user)
        engine_patterns = EnginePattern.objects.filter(user=session_user)
        generator_patterns = GeneratorPattern.objects.filter(user=session_user)
        weapon_patterns = WeaponPattern.objects.filter(user=session_user)
        shell_patterns = ShellPattern.objects.filter(user=session_user)
        module_patterns = ModulePattern.objects.filter(user=session_user)
        basic_resources = BasicResource.objects.all()
        fuel_patterns = FuelPattern.objects.filter(user=session_user)
        device_patterns = DevicePattern.objects.filter(user=session_user)
        ship_holds = Hold.objects.filter(fleet=fleet).order_by('class_shipment')
        ship_resource_hold = ResourceHold.objects.filter(fleet - fleet).first()
        add_ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city)
        ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city)

        request.session['user'] = session_user.id
        request.session['user_city'] = session_user_city.id
        request.session['live'] = True

        output = {'user': session_user, 'warehouse': session_user.warehouse, 'user_city': user_city,
                  'user_citys': user_citys, 'user_fleets': user_fleets, 'add_ships': add_ships, 'fleet': fleet,
                  'ship_fleets': ship_fleets, 'ships': ships, 'command': command, 'flightplans': flightplans,
                  'flightplan_flights': flightplan_flights, 'warehouse_factorys': warehouse_factorys,
                  'factory_patterns': factory_patterns, 'warehouse_elements': warehouse_elements,
                  'hull_patterns': hull_patterns, 'armor_patterns': armor_patterns, 'shield_patterns': shield_patterns,
                  'device_patterns': device_patterns, 'engine_patterns': engine_patterns,
                  'generator_patterns': generator_patterns, 'weapon_patterns': weapon_patterns,
                  'shell_patterns': shell_patterns, 'fuel_patterns': fuel_patterns,
                  'flightplan_scans': flightplan_scans, 'flightplan_productions': flightplan_productions,
                  'fleet_engine': fleet_engine, 'basic_resources': basic_resources, 'module_patterns': module_patterns,
                  'fleet_parametr_scans': fleet_parametr_scans, 'ship_resource_hold': ship_resource_hold,
                  'fleet_parametr_resource_extraction': fleet_parametr_resource_extraction, 'ship_holds': ship_holds,
                  'message': message, 'flightplan_holds': flightplan_holds, 'flightplan_refills': flightplan_refills,
                  'fleet_parametr_builds': fleet_parametr_builds, 'fleet_parametr_repair': fleet_parametr_repair,
                  'flightplan_build_repairs': flightplan_build_repairs,
                  'flightplan_colonization': flightplan_colonization}

        return render(request, "flightplan.html", output)
