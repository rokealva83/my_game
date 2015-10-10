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
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)

        amount = int(request.POST.get('amount_fuel'))
        fleet_id = int(request.POST.get('hidden_fleet'))
        fuel_tank_id = int(request.POST.get('hidden_fuel'))
        command = 4
        if amount != 0:
            fleet = Fleet.objects.filter(id=fleet_id).first()
            if fleet.planet_status == 1:
                fuel_tank = FuelTank.objects.filter(id=fuel_tank_id).first()
                fuel = FuelPattern.objects.filter(id=fuel_tank.fuel_class).first()
                if int(fuel_tank.amount_fuel) <= int(amount):
                    amount = fuel_tank.amount_fuel
                    delete_fuel_tank = FuelTank.objects.filter(id=fuel_tank_id).delete()
                else:
                    new_amount = int(fuel_tank.amount_fuel) - int(amount)
                    new_fuel_mass = int(fuel_tank.mass_fuel) - int(fuel.mass * amount)
                    new_fuel_size = int(fuel_tank.size_fuel) - int(fuel.size * amount)
                    fuel_tank_up = FuelTank.objects.filter(id=fuel_tank_id).update(amount_fuel=new_amount,
                                                                                    mass_fuel=new_fuel_mass,
                                                                                    size_fuel=new_fuel_size)

                warehouse_element = WarehouseElement.objects.filter(user=session_user, user_city=session_user_city,
                                                                     element_class=14,
                                                                     element_id=fuel_tank.fuel_class).first()

                if warehouse_element:
                    new_amount = int(warehouse_element.amount) + amount
                    warehouse_element = WarehouseElement.objects.filter(user=session_user, user_city=session_user_city,
                                                                         element_class=14,
                                                                         element_id=fuel_tank.fuel_class).update(
                        amount=new_amount)
                else:
                    warehouse_element = WarehouseElement(
                        user=session_user,
                        user_city=session_user_city,
                        element_class=14,
                        element_id=fuel_tank.fuel_class,
                        amount=amount
                    )
                new_fleet_mass = int(fleet.ship_empty_mass) - int(fuel.mass * amount)
                new_free_fuel_tank = int(fleet.free_fuel_tank) + int(fuel.size * amount)
                fleet = Fleet.objects.filter(id=fleet_id).update(ship_empty_mass=new_fleet_mass,
                                                                 free_fuel_tank=new_free_fuel_tank)
                message = 'Топливо выгружено'
            else:
                message = 'Флот не над планетой'
        else:
            message = 'Топливо не выбрано'

        warehouse_elements = WarehouseElement.objects.filter(user=session_user, user_city=session_user_city,
                                                              element_class=14).order_by('element_id')
        fuel_patterns = FuelPattern.objects.filter(user=session_user)
        fuel_tanks = FuelTank.objects.filter(fleet_id=fleet_id)
        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by(
            'resource_id')
        basic_fuels = BasicFuel.objects.filter()
        user_city = UserCity.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = UserCity.objects.filter(user=int(session_user))
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