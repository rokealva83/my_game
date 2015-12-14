# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity
from my_game.models import DevicePattern
from my_game import function
from my_game.models import Ship, Fleet
from my_game.models import Flightplan, FlightplanFlight, FlightplanScan, FlightplanHold, FlightplanProduction
from my_game.models import HullPattern, ArmorPattern, ShellPattern, ShieldPattern, WeaponPattern, \
    WarehouseFactory, WarehouseElement, FactoryPattern, EnginePattern, GeneratorPattern, ModulePattern, \
    BasicResource, Hold, FleetEngine, FleetParametrScan, FleetParametrResourceExtraction, FuelPattern, \
    FlightplanBuildRepair, FlightplanRefill, FleetParametrBuildRepair, FlightplanColonization
from my_game.flightplan.starting_flight import starting_flight


def start_flightplan(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        function.check_all_queues(session_user)
        message = ''
        command = 0
        fleet_id = 0

        if request.POST.get('start_flight'):
            fleet_id = int(request.POST.get('hidden_fleet'))
            message = starting_flight(fleet_id, session_user)
            command = 0

        if request.POST.get('delete_list'):
            fleet_id = int(request.POST.get('hidden_fleet'))
            fleet = Fleet.objects.filter(id=fleet_id).first()
            flightplan = Flightplan.objects.filter(fleet=fleet).first()
            if flightplan.status == 0:
                Flightplan.objects.filter(fleet=fleet).delete()
                FlightplanFlight.objects.filter(fleet=fleet).delete()
                FlightplanScan.objects.filter(fleet=fleet).delete()
                FlightplanProduction.objects.filter(fleet=fleet).delete()
                FlightplanHold.objects.filter(fleet=fleet).delete()
                FlightplanRefill.objects.filter(fleet=fleet).delete()
                FlightplanColonization.objects.filter(fleet=fleet).delete()
                message = ''
                command = 3

        user_citys = UserCity.objects.filter(user=session_user).all()
        user_fleets = Fleet.objects.filter(user=session_user).all()
        ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1).all()
        fleet = Fleet.objects.filter(id=fleet_id).first()
        flightplans = Flightplan.objects.filter(fleet=fleet).all()
        flightplan_flights = FlightplanFlight.objects.filter(fleet=fleet).all()
        flightplan_scans = FlightplanScan.objects.filter(fleet=fleet).all()
        flightplan_productions = FlightplanProduction.objects.filter(fleet=fleet).all()
        flightplan_refills = FlightplanRefill.objects.filter(fleet=fleet).order_by('id')
        flightplan_build_repairs = FlightplanBuildRepair.objects.filter(fleet=fleet).order_by('id')
        flightplan_colonization = FlightplanColonization.objects.filter(fleet=fleet).order_by('id')
        fleet_engine = FleetEngine.objects.filter(fleet=fleet).first()
        fleet_parametr_scans = FleetParametrScan.objects.filter(fleet=fleet).all()
        fleet_parametr_resource_extraction = FleetParametrResourceExtraction.objects.filter(
            fleet=fleet).first()
        fleet_parametr_build = FleetParametrBuildRepair.objects.filter(fleet=fleet,
                                                                       class_process=1).first()
        fleet_parametr_repair = FleetParametrBuildRepair.objects.filter(fleet=fleet,
                                                                        class_process=2).first()
        warehouse_factorys = WarehouseFactory.objects.filter(user=session_user,
                                                             user_city=session_user_city).order_by(
            'production_class', 'production_id')
        warehouse_elements = WarehouseElement.objects.filter(user=session_user,
                                                             user_city=session_user_city).order_by(
            'element_class', 'element_id')
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
        basic_resources = BasicResource.objects.all()
        device_patterns = DevicePattern.objects.filter(user=session_user).all()
        ship_holds = Hold.objects.filter(fleet=fleet).order_by('class_shipment')
        add_ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city.id).all()
        ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city.id).all()
        request.session['userid'] = session_user.id
        request.session['user_city'] = session_user_city.id
        request.session['live'] = True

        output = {'user': session_user, 'warehouse': session_user.warehouse, 'user_city': session_user_city,
                  'user_citys': user_citys, 'user_fleets': user_fleets, 'add_ships': add_ships, 'fleet_id': fleet_id,
                  'ship_fleets': ship_fleets, 'ships': ships, 'fleet': fleet, 'command': command,
                  'flightplans': flightplans, 'flightplan_flights': flightplan_flights,
                  'warehouse_factorys': warehouse_factorys, 'factory_patterns': factory_patterns,
                  'warehouse_elements': warehouse_elements, 'hull_patterns': hull_patterns,
                  'armor_patterns': armor_patterns, 'shield_patterns': shield_patterns,
                  'engine_patterns': engine_patterns, 'generator_patterns': generator_patterns,
                  'weapon_patterns': weapon_patterns, 'shell_patterns': shell_patterns, 'fuel_patterns': fuel_patterns,
                  'flightplan_scans': flightplan_scans, 'flightplan_productions': flightplan_productions,
                  'fleet_engine': fleet_engine, 'basic_resources': basic_resources, 'module_patterns': module_patterns,
                  'fleet_parametr_scans': fleet_parametr_scans, 'ship_holds': ship_holds, 'message': message,
                  'fleet_parametr_resource_extraction': fleet_parametr_resource_extraction,
                  'flightplan_refills': flightplan_refills, 'flightplan_build_repairs': flightplan_build_repairs,
                  'fleet_parametr_build': fleet_parametr_build, 'fleet_parametr_repair': fleet_parametr_repair,
                  'flightplan_colonization': flightplan_colonization, 'device_patterns': device_patterns}

        return render(request, "space_forces.html", output)
