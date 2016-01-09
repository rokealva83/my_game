# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity
from my_game.models import WarehouseElement, WarehouseFactory, BasicResource, BasicFuel
from my_game.models import Ship, Fleet, Hold, FleetParametrScan, FleetEnergyPower, FleetEngine, \
    FlightplanProduction, FlightplanScan, FlightplanHold, FlightplanRefill, FlightplanBuildRepair, \
    FlightplanColonization, ResourceHold, FleetFuelRefill, FleetOverload
from my_game.models import Flightplan, FlightplanFlight, FleetParametrResourceExtraction, \
    FleetParametrBuildRepair
from my_game.models import HullPattern, ShellPattern, ShieldPattern, GeneratorPattern, EnginePattern, \
    ArmorPattern, ModulePattern, FactoryPattern, WeaponPattern, FuelPattern, FuelTank, DevicePattern
from my_game import function


def fleet_manage(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        function.check_all_queues(session_user)
        add_ships = {}
        fleet_id = 1
        fleet = None
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
        fuel_patterns = {}
        ship_holds = {}
        message = ''

        command = 0
        if request.POST.get('create_fleet'):
            name = request.POST.get('fleet_name')
            fleet_energy = FleetEnergyPower()
            fleet_energy.save()
            fleet_engine = FleetEngine()
            fleet_engine.save()
            resource_hold = ResourceHold()
            resource_hold.save()

            new_fleet = Fleet(
                user=session_user,
                fleet_name=name,
                x=session_user_city.x,
                y=session_user_city.y,
                z=session_user_city.z,
                system_id=session_user_city.system.id,
                planet_id=session_user_city.planet.id,
                resource_hold=resource_hold,
                fleet_engine=fleet_engine,
                fleet_energy_power=fleet_energy
            )
            new_fleet.save()

        if request.POST.get('hidden_fleet'):
            fleet_id = int(request.POST.get('hidden_fleet'))
            fleet = Fleet.objects.filter(id=fleet_id).first()

        if request.POST.get('navy_ships'):
            add_ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city.id).all()
            command = 1

        if request.POST.get('flight_plan'):
            flightplans = Flightplan.objects.filter(user=session_user, fleet=fleet).all()
            flightplan_flights = FlightplanFlight.objects.filter(user=session_user, fleet=fleet).all()
            command = 3
            user_citys = UserCity.objects.filter(user=session_user).all()
            user_fleets = Fleet.objects.filter(user=session_user).all()
            ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city.id).all()
            ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1).all()
            fleet_engine = FleetEngine.objects.filter(fleet=fleet).first()
            fleet_parametr_scans = FleetParametrScan.objects.filter(fleet=fleet).all()
            fleet_parametr_resource_extraction = FleetParametrResourceExtraction.objects.filter(fleet=fleet).first()
            fleet_parametr_build = FleetParametrBuildRepair.objects.filter(fleet=fleet, class_process=1).first()
            fleet_parametr_repair = FleetParametrBuildRepair.objects.filter(fleet=fleet, class_process=2).first()
            flightplan_scans = FlightplanScan.objects.filter(fleet=fleet).all()
            flightplan_productions = FlightplanProduction.objects.filter(fleet=fleet).all()
            flightplan_holds = FlightplanHold.objects.filter(fleet=fleet).order_by('id')
            flightplan_refills = FlightplanRefill.objects.filter(fleet=fleet).order_by('id')
            flightplan_build_repairs = FlightplanBuildRepair.objects.filter(fleet=fleet).order_by('id')
            fleet_refill = FleetFuelRefill.objects.filter(fleet=fleet).first()
            fleet_overload = FleetOverload.objects.filter(fleet=fleet).first()
            flightplan_colonizations = FlightplanColonization.objects.filter(fleet=fleet).order_by('id')
            warehouse_factorys = WarehouseFactory.objects.filter(user=session_user,
                                                                 user_city=session_user_city).all()
            warehouse_elements = WarehouseElement.objects.filter(user=session_user,
                                                                 user_city=session_user_city).order_by('element_class',
                                                                                                       'element_id')
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

            output = {'user': session_user, 'warehouse': session_user_city.warehouse, 'user_city': session_user_city,
                      'user_citys': user_citys, 'user_fleets': user_fleets, 'add_ships': add_ships,
                      'fleet_id': fleet_id, 'ship_fleets': ship_fleets, 'ships': ships, 'fleet': fleet,
                      'command': command, 'flightplans': flightplans, 'flightplan_flights': flightplan_flights,
                      'warehouse_factorys': warehouse_factorys, 'factory_patterns': factory_patterns,
                      'warehouse_elements': warehouse_elements, 'hull_patterns': hull_patterns,
                      'armor_patterns': armor_patterns, 'shield_patterns': shield_patterns,
                      'engine_patterns': engine_patterns, 'generator_patterns': generator_patterns,
                      'weapon_patterns': weapon_patterns, 'shell_patterns': shell_patterns,
                      'fuel_patterns': fuel_patterns, 'flightplan_scans': flightplan_scans,
                      'flightplan_productions': flightplan_productions,
                      'basic_resources': basic_resources, 'module_patterns': module_patterns,
                      'fleet_parametr_scans': fleet_parametr_scans, 'flightplan_refills': flightplan_refills,
                      'fleet_parametr_resource_extraction': fleet_parametr_resource_extraction,
                      'ship_holds': ship_holds, 'flightplan_holds': flightplan_holds,
                      'fleet_parametr_build': fleet_parametr_build, 'fleet_parametr_repair': fleet_parametr_repair,
                      'flightplan_build_repairs': flightplan_build_repairs, 'device_patterns': device_patterns,
                      'fleet_overload': fleet_overload, 'fleet_refill': fleet_refill, 'fleet_engine': fleet_engine,
                      'flightplan_colonizations': flightplan_colonizations}
            return render(request, "flightplan.html", output)

        if request.POST.get('hold_fleet'):
            warehouse_factorys = WarehouseFactory.objects.filter(user=session_user,
                                                                 user_city=session_user_city).all()
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
            device_patterns = DevicePattern.objects.filter(user=session_user).all()
            command = 2
            ship_holds = Hold.objects.filter(fleet=fleet).order_by('class_shipment')

        if request.POST.get('fuel_tank'):
            warehouse_elements = WarehouseElement.objects.filter(user=session_user, user_city=session_user_city,
                                                                 element_class=14).order_by('element_id')
            fuel_patterns = FuelPattern.objects.filter(user=session_user).order_by('basic_pattern')
            fuel_tanks = FuelTank.objects.filter(fleet=fleet).order_by('fuel_pattern')
            command = 4
            basic_fuels = BasicFuel.objects.filter()
            user_citys = UserCity.objects.filter(user=session_user).all()
            user_fleets = Fleet.objects.filter(user=session_user)
            ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1)
            ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city.id)
            request.session['user'] = session_user.id
            request.session['user_city'] = session_user_city.id
            request.session['live'] = True
            output = {'user': session_user, 'warehouse': session_user_city.warehouse, 'user_city': session_user_city,
                      'user_citys': user_citys, 'user_fleets': user_fleets, 'fleet_id': fleet_id,
                      'ship_fleets': ship_fleets, 'ships': ships, 'command': command, 'fuel_patterns': fuel_patterns,
                      'fuel_tanks': fuel_tanks, 'basic_fuels': basic_fuels, 'warehouse_elements': warehouse_elements}
            return render(request, "fuel_tank.html", output)

        if request.POST.get('delete_fleet'):
            command = 0
            ship = Ship.objects.filter(fleet_status=1, place_id=fleet_id).first()
            if ship:
                message = 'Во флоте есть корабли'
            else:
                fleet = Fleet.objects.filter(id=fleet_id).delete()
                FleetParametrScan.objects.filter(fleet=fleet).delete()
                message = 'Флот удален'

        basic_resources = BasicResource.objects.filter()
        user_citys = UserCity.objects.filter(user=session_user).all()
        user_fleets = Fleet.objects.filter(user=session_user).all()
        ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1).all()
        ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city.id).all()
        request.session['user'] = session_user.id
        request.session['user_city'] = session_user_city.id
        request.session['live'] = True
        output = {'user': session_user, 'warehouse': session_user_city.warehouse, 'basic_resources': basic_resources,
                  'user_city': session_user_city, 'user_citys': user_citys, 'user_fleets': user_fleets,
                  'add_ships': add_ships, 'fleet_id': fleet_id, 'ship_fleets': ship_fleets, 'ships': ships,
                  'command': command, 'flightplans': flightplans, 'flightplan_flights': flightplan_flights,
                  'warehouse_factorys': warehouse_factorys, 'factory_patterns': factory_patterns,
                  'warehouse_elements': warehouse_elements, 'hull_patterns': hull_patterns,
                  'armor_patterns': armor_patterns, 'shield_patterns': shield_patterns,
                  'engine_patterns': engine_patterns, 'generator_patterns': generator_patterns,
                  'weapon_patterns': weapon_patterns, 'shell_patterns': shell_patterns, 'fuel_patterns': fuel_patterns,
                  'module_patterns': module_patterns, 'message': message, 'ship_holds': ship_holds,
                  'device_patterns': device_patterns, 'fleet': fleet}
        return render(request, "fleet_hold.html", output)
