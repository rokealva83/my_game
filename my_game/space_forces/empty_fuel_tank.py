# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity
from my_game.models import Warehouse, WarehouseElement
from my_game import function
from my_game.models import Ship, Fleet, FuelTank, FuelPattern, BasicFuel


def empty_fuel_tank(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        function.check_all_queues(session_user)

        amount = int(request.POST.get('amount_fuel'))
        fleet_id = int(request.POST.get('hidden_fleet'))
        fleet = Fleet.objects.filter(id=fleet_id).first()
        fuel_tank_id = int(request.POST.get('hidden_fuel'))
        command = 4
        if amount != 0:
            if fleet.planet_status == 1:
                fuel_tank = FuelTank.objects.filter(id=fuel_tank_id).first()
                fuel = FuelPattern.objects.filter(id=fuel_tank.fuel_class).first()
                if int(fuel_tank.amount_fuel) <= int(amount):
                    amount = fuel_tank.amount_fuel
                    FuelTank.objects.filter(id=fuel_tank_id).delete()
                else:
                    new_amount = int(fuel_tank.amount_fuel) - int(amount)
                    new_fuel_mass = int(fuel_tank.mass_fuel) - int(fuel.mass * amount)
                    new_fuel_size = int(fuel_tank.size_fuel) - int(fuel.size * amount)
                    FuelTank.objects.filter(id=fuel_tank_id).update(amount_fuel=new_amount,
                                                                    mass_fuel=new_fuel_mass,
                                                                    size_fuel=new_fuel_size)

                warehouse_element = WarehouseElement.objects.filter(user=session_user, user_city=session_user_city,
                                                                    element_class=14,
                                                                    element_id=fuel_tank.fuel_class).first()

                if warehouse_element:
                    new_amount = int(warehouse_element.amount) + amount
                    WarehouseElement.objects.filter(user=session_user, user_city=session_user_city, element_class=14,
                                                    element_id=fuel_tank.fuel_class).update(amount=new_amount)
                else:
                    WarehouseElement(
                        user=session_user,
                        user_city=session_user_city,
                        element_class=14,
                        element_id=fuel_tank.fuel_class,
                        amount=amount
                    )
                new_fleet_mass = int(fleet.ship_empty_mass) - int(fuel.mass * amount)
                new_free_fuel_tank = int(fleet.free_fuel_tank) + int(fuel.size * amount)
                Fleet.objects.filter(id=fleet_id).update(ship_empty_mass=new_fleet_mass,
                                                         free_fuel_tank=new_free_fuel_tank)
                message = 'Топливо выгружено'
            else:
                message = 'Флот не над планетой'
        else:
            message = 'Топливо не выбрано'

        warehouse_elements = WarehouseElement.objects.filter(user=session_user, user_city=session_user_city,
                                                             element_class=14).order_by('element_id')
        fuel_patterns = FuelPattern.objects.filter(user=session_user).all()
        fuel_tanks = FuelTank.objects.filter(fleet=fleet).all()
        basic_fuels = BasicFuel.objects.all()
        user_citys = UserCity.objects.filter(user=session_user).all()
        user_fleets = Fleet.objects.filter(user=session_user).all()
        ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1).all()
        ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city.id).all()
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': session_user, 'warehouse': session_user_city.warehouse, 'user_city': session_user_city,
                  'user_citys': user_citys, 'user_fleets': user_fleets, 'fleet_id': fleet_id,
                  'ship_fleets': ship_fleets, 'ships': ships, 'command': command, 'fuel_patterns': fuel_patterns,
                  'fuel_tanks': fuel_tanks, 'message': message, 'basic_fuels': basic_fuels,
                  'warehouse_elements': warehouse_elements}
        return render(request, "fuel_tank.html", output)
