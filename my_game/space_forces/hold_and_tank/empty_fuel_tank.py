# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity
from my_game.models import WarehouseElement
from my_game import function
from my_game.models import Ship, Fleet, FuelTank, FuelPattern, BasicFuel
from my_game.space_forces.hold_and_tank.unload_fuel import unload_fuel
from my_game.space_forces.hold_and_tank.unload_fuel_all import unload_fuel_all


def empty_fuel_tank(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        function.check_all_queues(session_user)
        command = 4
        message = ''
        fleet_id = int(request.POST.get('hidden_fleet'))
        fleet = Fleet.objects.filter(id=fleet_id).first()
        if request.POST.get('unload'):
            amount = int(request.POST.get('amount_fuel'))
            fuel_tank_id = int(request.POST.get('hidden_fuel'))
            message = unload_fuel(session_user, session_user_city, fleet, amount, fuel_tank_id)
        if request.POST.get('unload_fuel_all'):
            message = unload_fuel_all(session_user, session_user_city, fleet)

        warehouse_elements = WarehouseElement.objects.filter(user=session_user, user_city=session_user_city,
                                                             element_class=14).order_by('element_class', 'element_id')
        fuel_patterns = FuelPattern.objects.filter(user=session_user).order_by('basic_pattern')
        fuel_tanks = FuelTank.objects.filter(fleet=fleet).order_by('fuel_pattern')
        basic_fuels = BasicFuel.objects.all()
        user_citys = UserCity.objects.filter(user=session_user).all()
        user_fleets = Fleet.objects.filter(user=session_user).all()
        ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1).all()
        ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city.id).all()
        request.session['user'] = session_user.id
        request.session['user_city'] = session_user_city.id
        request.session['live'] = True
        output = {'user': session_user, 'warehouse': session_user_city.warehouse, 'user_city': session_user_city,
                  'user_citys': user_citys, 'user_fleets': user_fleets, 'fleet_id': fleet_id,
                  'ship_fleets': ship_fleets, 'ships': ships, 'command': command, 'fuel_patterns': fuel_patterns,
                  'fuel_tanks': fuel_tanks, 'message': message, 'basic_fuels': basic_fuels,
                  'warehouse_elements': warehouse_elements}
        return render(request, "fuel_tank.html", output)
