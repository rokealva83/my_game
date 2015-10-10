# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity
from my_game.models import Warehouse
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
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
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
            flightplan = Flightplan.objects.filter(id_fleet=fleet_id).first()
            if flightplan.status == 0:
                flightplan = Flightplan.objects.filter(id_fleet=fleet_id).delete()
                flightplan_flight = FlightplanFlight.objects.filter(id_fleet=fleet_id).delete()
                flightplan_scan = FlightplanScan.objects.filter(id_fleet=fleet_id).delete()
                flightplan_production = FlightplanProduction.objects.filter(id_fleet=fleet_id).delete()
                flightplan_hold = FlightplanHold.objects.filter(id_fleet=fleet_id).delete()
                flightplan_refill = FlightplanRefill.objects.filter(id_fleet=fleet_id).delete()
                flightplan_colonization = FlightplanColonization.objects.filter(id_fleet=fleet_id).delete()
                message = ''
                command = 3

        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('resource_id')
        user_city = UserCity.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = UserCity.objects.filter(user=int(session_user))
        user_fleets = Fleet.objects.filter(user=session_user)
        ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1)
        fleet = Fleet.objects.filter(user=session_user)
        flightplans = Flightplan.objects.filter(id_fleet=fleet_id)
        flightplan_flights = FlightplanFlight.objects.filter(id_fleet=fleet_id)
        flightplan_scans = FlightplanScan.objects.filter(id_fleet=fleet_id)
        flightplan_productions = FlightplanProduction.objects.filter(id_fleet=fleet_id)
        flightplan_refills = FlightplanRefill.objects.filter(id_fleet=fleet_id).order_by('id')
        flightplan_build_repairs = FlightplanBuildRepair.objects.filter(id_fleet=fleet_id).order_by('id')
        flightplan_colonization = FlightplanColonization.objects.filter(id_fleet=fleet_id).order_by('id')
        fleet_engine = FleetEngine.objects.filter(fleet_id=fleet_id).first()
        fleet_parametr_scans = FleetParametrScan.objects.filter(fleet_id=fleet_id)
        fleet_parametr_resource_extraction = FleetParametrResourceExtraction.objects.filter(
            fleet_id=fleet_id).first()
        fleet_parametr_build = FleetParametrBuildRepair.objects.filter(fleet_id=fleet_id,
                                                                          class_process=1).first()
        fleet_parametr_repair = FleetParametrBuildRepair.objects.filter(fleet_id=fleet_id,
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
        fuel_patterns = FuelPattern.objects.filter(user=session_user)
        basic_resources = BasicResource.objects.all()
        # device_patterns = Device_pattern.objects.filter(user = session_user)
        ship_holds = Hold.objects.filter(fleet_id=fleet_id).order_by('class_shipment')
        add_ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city)
        ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city)
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True

        output = {'user': user, 'warehouses': warehouses, 'user_city': user_city, 'user_citys': user_citys,
                  'user_fleets': user_fleets, 'add_ships': add_ships, 'fleet_id': fleet_id, 'ship_fleets': ship_fleets,
                  'ships': ships, 'fleet': fleet, 'command': command, 'flightplans': flightplans,
                  'flightplan_flights': flightplan_flights, 'warehouse_factorys': warehouse_factorys,
                  'factory_patterns': factory_patterns, 'warehouse_elements': warehouse_elements,
                  'hull_patterns': hull_patterns, 'armor_patterns': armor_patterns, 'shield_patterns': shield_patterns,
                  'engine_patterns': engine_patterns, 'generator_patterns': generator_patterns,
                  'weapon_patterns': weapon_patterns, 'shell_patterns': shell_patterns, 'fuel_patterns': fuel_patterns,
                  'flightplan_scans': flightplan_scans, 'flightplan_productions': flightplan_productions,
                  'fleet_engine': fleet_engine, 'basic_resources': basic_resources, 'module_patterns': module_patterns,
                  'fleet_parametr_scans': fleet_parametr_scans, 'ship_holds': ship_holds, 'message': message,
                  'fleet_parametr_resource_extraction': fleet_parametr_resource_extraction,
                  'flightplan_refills': flightplan_refills, 'flightplan_build_repairs': flightplan_build_repairs,
                  'fleet_parametr_build': fleet_parametr_build, 'fleet_parametr_repair': fleet_parametr_repair,
                  'flightplan_colonization': flightplan_colonization}

        return render(request, "space_forces.html", output)
