# -*- coding: utf-8 -*-


from datetime import datetime, timedelta
from django.shortcuts import render
from my_game.models import MyUser, User_city
from my_game.models import Warehouse
from my_game import function
from my_game.models import Ship, Fleet
from my_game.models import Flightplan, Flightplan_flight, Flightplan_scan, Flightplan_hold, Flightplan_production
from my_game.models import Hull_pattern, Armor_pattern, Shell_pattern, Shield_pattern, Weapon_pattern, \
    Warehouse_factory, Warehouse_element, Factory_pattern, Engine_pattern, Generator_pattern, Module_pattern, \
    Basic_resource, Hold, Fleet_engine, Fleet_parametr_scan, Fleet_parametr_resource_extraction, Fuel_pattern


def start_flight(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        message = ''
        command = 0
        if request.POST.get('start_flight'):
            fleet_id = int(request.POST.get('hidden_fleet'))
            flightplan = Flightplan.objects.filter(id_fleet=fleet_id).first()
            id_flightplan = flightplan.pk
            if flightplan.class_command == 1:
                flightplan_flight = Flightplan_flight.objects.filter(id_fleet=fleet_id,
                                                                     id_command=flightplan.id_command).first()
                start_time = datetime.now()
                finish_time = start_time + timedelta(seconds=flightplan_flight.flight_time)
                flightplan_flight = Flightplan_flight.objects.filter(id_fleet=fleet_id,
                                                                     id_command=flightplan.id_command).update(
                    start_time=start_time, finish_time=finish_time)

                flightplan = Flightplan.objects.filter(id=id_flightplan, id_fleet=fleet_id).update(status=1)
                fleet = Fleet.objects.filter(id=fleet_id).update(status=True, planet_status=0)
            command = 0

        if request.POST.get('delete_list'):
            fleet_id = int(request.POST.get('hidden_fleet'))
            flightplan = Flightplan.objects.filter(id_fleet=fleet_id).delete()
            flightplan_flight = Flightplan_flight.objects.filter(id_fleet=fleet_id).delete()
            flightplan_scan = Flightplan_scan.objects.filter(id_fleet=fleet_id).delete()
            flightplan_production = Flightplan_production.objects.filter(id_fleet=fleet_id).delete()
            flightplan_hold = Flightplan_hold.objects.filter(id_fleet=fleet_id).delete()
            message = ''
            command = 3

        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('id_resource')
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = User_city.objects.filter(user=int(session_user))
        user_fleets = Fleet.objects.filter(user=session_user)
        ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1)
        fleet = Fleet.objects.filter(user=session_user)
        flightplans = Flightplan.objects.filter(id_fleet=fleet_id)
        flightplan_flights = Flightplan_flight.objects.filter(id_fleet=fleet_id)
        flightplan_scans = Flightplan_scan.objects.filter(id_fleet=fleet_id)
        flightplan_productions = Flightplan_production.objects.filter(id_fleet=fleet_id)
        fleet_engine = Fleet_engine.objects.filter(fleet_id=fleet_id).first()
        fleet_parametr_scans = Fleet_parametr_scan.objects.filter(fleet_id=fleet_id)
        fleet_parametr_resource_extraction = Fleet_parametr_resource_extraction.objects.filter(
            fleet_id=fleet_id).first()
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
                  'fleet_parametr_resource_extraction': fleet_parametr_resource_extraction}

        return render(request, "space_forces.html", output)
