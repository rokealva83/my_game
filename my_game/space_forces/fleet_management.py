# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, User_city
from my_game.models import Warehouse, Warehouse_element, Warehouse_factory
from my_game.models import Project_ship, Ship, Fleet
from my_game.models import Flightplan, Flightplan_flight
from my_game.models import Hull_pattern, Shell_pattern, Shield_pattern, Generator_pattern, Engine_pattern, \
    Armor_pattern, Module_pattern, Factory_pattern, Weapon_pattern
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

        if request.POST.get('navy_ships'):
            add_ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city)
            fleet_id = int(request.POST.get('hidden_fleet'))
            command = 1

        if request.POST.get('flight_plan'):
            fleet_id = int(request.POST.get('hidden_fleet'))
            flightplans = Flightplan.objects.filter(user=session_user, id_fleet=fleet_id)
            flightplan_flights = Flightplan_flight.objects.filter(user=session_user, id_fleet=fleet_id)
            command = 3

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
            # device_patterns = Device_pattern.objects.filter(user = session_user)
            command = 2

        warehouse = Warehouse.objects.filter(user=session_user).first()
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = User_city.objects.filter(user=int(session_user))
        user_fleets = Fleet.objects.filter(user=session_user)
        ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1)
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouse': warehouse, 'user_city': user_city, 'user_citys': user_citys,
                  'user_fleets': user_fleets, 'add_ships': add_ships, 'fleet_id': fleet_id, 'ship_fleets': ship_fleets,
                  'command': command, 'flightplans': flightplans, 'flightplan_flights': flightplan_flights,
                  'warehouse_factorys': warehouse_factorys, 'factory_patterns': factory_patterns,
                  'warehouse_elements': warehouse_elements, 'hull_patterns': hull_patterns,
                  'armor_patterns': armor_patterns, 'shield_patterns': shield_patterns,
                  'engine_patterns': engine_patterns, 'generator_patterns': generator_patterns,
                  'weapon_patterns': weapon_patterns, 'shell_patterns': shell_patterns,
                  'module_patterns': module_patterns}
        return render(request, "space_forces.html", output)