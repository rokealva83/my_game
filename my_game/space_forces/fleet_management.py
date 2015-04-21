# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, User_city
from my_game.models import Warehouse, Warehouse_element, Warehouse_factory, Basic_resource, Basic_fuel
from my_game.models import Ship, Fleet, Hold, Element_ship, Fleet_parametr_scan, Fleet_energy_power, Fleet_engine, \
    Flightplan_production, Flightplan_scan, Flightplan_hold, Flightplan_refill, Flightplan_repair
from my_game.models import Flightplan, Flightplan_flight, Fleet_parametr_resource_extraction
from my_game.models import Hull_pattern, Shell_pattern, Shield_pattern, Generator_pattern, Engine_pattern, \
    Armor_pattern, Module_pattern, Factory_pattern, Weapon_pattern, Fuel_pattern, Fuel_tank
from my_game import function


def fleet_manage(request):
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
        fuel_patterns = {}
        ship_holds = {}
        message = ''

        fleet_id = 0
        command = 0
        ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1)
        if request.POST.get('create_fleet'):
            name = request.POST.get('fleet_name')
            user_city = User_city.objects.filter(id=session_user_city).first()
            new_fleet = Fleet(
                user=session_user,
                name=name,
                x=user_city.x,
                y=user_city.y,
                z=user_city.z,
                system=user_city.system_id,
                planet=user_city.planet_id
            )
            new_fleet.save()
            fleet_id = new_fleet.pk

            fleet_energy = Fleet_energy_power(
                fleet_id=fleet_id
            )
            fleet_energy.save()

            fleet_engine = Fleet_engine(
                fleet_id=fleet_id
            )
            fleet_engine.save()

        if request.POST.get('navy_ships'):
            add_ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city)
            fleet_id = int(request.POST.get('hidden_fleet'))
            command = 1

        if request.POST.get('flight_plan'):
            fleet_id = int(request.POST.get('hidden_fleet'))
            flightplans = Flightplan.objects.filter(user=session_user, id_fleet=fleet_id)
            flightplan_flights = Flightplan_flight.objects.filter(user=session_user, id_fleet=fleet_id)
            command = 3
            warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).first()
            warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by(
                'id_resource')
            user_city = User_city.objects.filter(user=session_user).first()
            user = MyUser.objects.filter(user_id=session_user).first()
            user_citys = User_city.objects.filter(user=int(session_user))
            user_fleets = Fleet.objects.filter(user=session_user)
            ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city)
            ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1)
            fleet = Fleet.objects.filter(id=fleet_id).first()
            fleet_parametr_scans = Fleet_parametr_scan.objects.filter(fleet_id=fleet_id)
            fleet_parametr_resource_extraction = Fleet_parametr_resource_extraction.objects.filter(
                fleet_id=fleet_id).first()
            flightplan_scans = Flightplan_scan.objects.filter(id_fleet=fleet_id)
            flightplan_productions = Flightplan_production.objects.filter(id_fleet=fleet_id)
            flightplan_holds = Flightplan_hold.objects.filter(id_fleet=fleet_id).order_by('id')
            flightplan_refills = Flightplan_refill.objects.filter(id_fleet=fleet_id).order_by('id')
            fleet_engine = Fleet_engine.objects.filter(fleet_id=fleet_id).first()
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
            fuel_patterns = Fuel_pattern.objects.filter(user=session_user)
            basic_resources = Basic_resource.objects.all()
            # device_patterns = Device_pattern.objects.filter(user = session_user)
            ship_holds = Hold.objects.filter(fleet_id=fleet_id).order_by('class_shipment')

            output = {'user': user, 'warehouses': warehouses, 'user_city': user_city, 'user_citys': user_citys,
                      'user_fleets': user_fleets, 'add_ships': add_ships, 'fleet_id': fleet_id,
                      'ship_fleets': ship_fleets, 'ships': ships, 'fleet': fleet,
                      'command': command, 'flightplans': flightplans, 'flightplan_flights': flightplan_flights,
                      'warehouse_factorys': warehouse_factorys, 'factory_patterns': factory_patterns,
                      'warehouse_elements': warehouse_elements, 'hull_patterns': hull_patterns,
                      'armor_patterns': armor_patterns, 'shield_patterns': shield_patterns,
                      'engine_patterns': engine_patterns, 'generator_patterns': generator_patterns,
                      'weapon_patterns': weapon_patterns, 'shell_patterns': shell_patterns,
                      'fuel_patterns': fuel_patterns, 'flightplan_scans': flightplan_scans,
                      'flightplan_productions': flightplan_productions, 'fleet_engine': fleet_engine,
                      'basic_resources': basic_resources, 'module_patterns': module_patterns,
                      'fleet_parametr_scans': fleet_parametr_scans, 'flightplan_refills': flightplan_refills,
                      'fleet_parametr_resource_extraction': fleet_parametr_resource_extraction,
                      'ship_holds': ship_holds, 'flightplan_holds': flightplan_holds}
            return render(request, "flightplan.html", output)

        if request.POST.get('hold_fleet'):
            fleet_id = int(request.POST.get('hidden_fleet'))
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
            fuel_patterns = Fuel_pattern.objects.filter(user=session_user)
            # device_patterns = Device_pattern.objects.filter(user = session_user)

            command = 2
            ship_holds = Hold.objects.filter(fleet_id=fleet_id).order_by('class_shipment')

        if request.POST.get('fuel_tank'):
            fleet_id = int(request.POST.get('hidden_fleet'))

            warehouse_elements = Warehouse_element.objects.filter(user=session_user, user_city=session_user_city,
                                                                  element_class=14).order_by('element_id')
            fuel_patterns = Fuel_pattern.objects.filter(user=session_user)

            command = 4
            fuel_tanks = Fuel_tank.objects.filter(fleet_id=fleet_id)
            warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by(
                'id_resource')
            basic_fuels = Basic_fuel.objects.filter()
            user_city = User_city.objects.filter(user=session_user).first()
            user = MyUser.objects.filter(user_id=session_user).first()
            user_citys = User_city.objects.filter(user=int(session_user))
            user_fleets = Fleet.objects.filter(user=session_user)
            ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1)
            ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city)
            request.session['userid'] = session_user
            request.session['user_city'] = session_user_city
            request.session['live'] = True
            output = {'user': user, 'warehouses': warehouses, 'user_city': user_city, 'user_citys': user_citys,
                      'user_fleets': user_fleets, 'fleet_id': fleet_id, 'ship_fleets': ship_fleets, 'ships': ships,
                      'command': command, 'fuel_patterns': fuel_patterns, 'fuel_tanks': fuel_tanks,
                      'basic_fuels': basic_fuels, 'warehouse_elements': warehouse_elements}
            return render(request, "fuel_tank.html", output)

        if request.POST.get('delete_fleet'):
            fleet_id = int(request.POST.get('hidden_fleet'))
            command = 0
            ship = Ship.objects.filter(fleet_status=1, place_id=fleet_id).first()
            if ship:
                message = 'Во флоте есть корабли'
            else:
                fleet = Fleet.objects.filter(id=fleet_id).delete()
                fleet_parametr_scan = Fleet_parametr_scan.objects.filter(fleet_id=fleet_id).delete()
                fleet_energy = Fleet_energy_power.objects.filter(fleet_id=fleet_id).delete()
                fleet_engine = Fleet_engine.objects.filter(fleet_id=fleet_id).delete()
                message = 'Флот удален'

        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('id_resource')
        basic_resources = Basic_resource.objects.filter()
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = User_city.objects.filter(user=int(session_user))
        user_fleets = Fleet.objects.filter(user=session_user)
        ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1)
        ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city)
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouses': warehouses, 'basic_resources': basic_resources, 'user_city': user_city,
                  'user_citys': user_citys,
                  'user_fleets': user_fleets, 'add_ships': add_ships, 'fleet_id': fleet_id, 'ship_fleets': ship_fleets,
                  'ships': ships, 'command': command, 'flightplans': flightplans,
                  'flightplan_flights': flightplan_flights, 'warehouse_factorys': warehouse_factorys,
                  'factory_patterns': factory_patterns, 'warehouse_elements': warehouse_elements,
                  'hull_patterns': hull_patterns, 'armor_patterns': armor_patterns, 'shield_patterns': shield_patterns,
                  'engine_patterns': engine_patterns, 'generator_patterns': generator_patterns,
                  'weapon_patterns': weapon_patterns, 'shell_patterns': shell_patterns, 'fuel_patterns': fuel_patterns,
                  'module_patterns': module_patterns, 'message': message, 'ship_holds': ship_holds}
        return render(request, "fleet_hold.html", output)