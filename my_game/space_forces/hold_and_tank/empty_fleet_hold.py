# -*- coding: utf-8 -*-

from django.shortcuts import render

from my_game.models import MyUser, UserCity
from my_game.models import WarehouseElement, WarehouseFactory, BasicResource
from my_game import function
from my_game.models import Ship, Fleet, Hold
from my_game.models import FactoryPattern, HullPattern, ArmorPattern, ShellPattern, ShieldPattern, \
    GeneratorPattern, WeaponPattern, EnginePattern, ModulePattern, FuelPattern, DevicePattern
from space_forces.hold_and_tank.unload_hold import unload_hold


def empty_fleet_hold(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        function.check_all_queues(session_user)
        add_ships = {}
        flightplans = {}
        flightplan_flights = {}
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

        full_request = request.POST
        my_dictionary = dict(full_request.iterlists())

        fleet_id_dict = my_dictionary.get('hidden_fleet')
        fleet_id = int(fleet_id_dict[0])
        fleet = Fleet.objects.filter(id=fleet_id).first()
        if fleet.planet_status == 1:
            message = unload_hold(session_user, session_user_city, fleet, my_dictionary)
        else:
            message = 'Флот не над планетой'
        ship_holds = Hold.objects.filter(fleet=fleet).order_by('class_shipment')
        warehouse = session_user_city.warehouse
        basic_resources = BasicResource.objects.all()
        user_citys = UserCity.objects.filter(user=session_user).all()
        user_fleets = Fleet.objects.filter(user=session_user).all()
        ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city.id).all()
        ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1).all()
        warehouse_factorys = WarehouseFactory.objects.filter(user=session_user, user_city=session_user_city).all()
        warehouse_elements = WarehouseElement.objects.filter(user=session_user, user_city=session_user_city).order_by(
            'element_class', 'element_id')
        command = 2
        request.session['user'] = session_user.id
        request.session['user_city'] = session_user_city.id
        request.session['live'] = True
        output = {'user': session_user, 'warehouse': warehouse, 'user_city': session_user_city,
                  'user_citys': user_citys, 'user_fleets': user_fleets, 'add_ships': add_ships, 'fleet_id': fleet_id,
                  'ship_fleets': ship_fleets, 'ships': ships, 'command': command, 'flightplans': flightplans,
                  'flightplan_flights': flightplan_flights, 'warehouse_factorys': warehouse_factorys,
                  'factory_patterns': factory_patterns, 'warehouse_elements': warehouse_elements,
                  'hull_patterns': hull_patterns, 'armor_patterns': armor_patterns, 'shell_patterns': shell_patterns,
                  'shield_patterns': shield_patterns, 'weapon_patterns': weapon_patterns,
                  'fuel_patterns': fuel_patterns, 'engine_patterns': engine_patterns,
                  'device_patterns': device_patterns, 'generator_patterns': generator_patterns,
                  'module_patterns': module_patterns, 'message': message, 'ship_holds': ship_holds,
                  'basic_resources': basic_resources, 'fleet': fleet}
        return render(request, "fleet_hold.html", output)
