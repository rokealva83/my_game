# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity
from my_game.models import Warehouse, WarehouseElement, FuelPattern, BasicFuel, FuelTank
from my_game import function
from my_game.models import Ship, Fleet


def fuel_tank(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)

        fleet_id = int(request.POST.get('hidden_fleet'))
        fuel_amount = int(request.POST.get('fuel_amount'))
        fuel_pattern_id = int(request.POST.get('fuel_pattern'))
        fleet = Fleet.objects.filter(id=fleet_id).first()
        ship_in_fleet = Ship.objects.filter(user=session_user, fleet_status=1, place_id=fleet_id).first()
        if fleet.planet_status == 1 and ship_in_fleet is not None:

            add_shipment = 0
            if int(fuel_amount) != 0 and add_shipment == 0 and fuel_pattern_id is not None:
                fuel = FuelPattern.objects.filter(id=fuel_pattern_id).first()
                size = fuel.size * int(fuel_amount)
                if size <= fleet.free_fuel_tank:
                    warehouse_element = WarehouseElement.objects.filter(user_city=session_user_city,
                                                                         element_class=14,
                                                                         element_id=fuel_pattern_id).first()
                    if warehouse_element.amount >= fuel_amount:
                        new_element_amount = warehouse_element.amount - fuel_amount
                        warehouse_element = WarehouseElement.objects.filter(user_city=session_user_city,
                                                                             element_class=14,
                                                                             element_id=fuel_pattern_id).update(
                            amount=new_element_amount)
                        error = 0
                    else:
                        error = 1

                    if error == 0:
                        fuel_tank = FuelTank.objects.filter(fleet_id=fleet_id, fuel_class=fuel_pattern_id).first()
                        if fuel_tank:
                            new_fuel_amount = fuel_amount + fuel_tank.amount_fuel
                            mass_fuel = fuel.mass * fuel_amount + fuel_tank.mass_fuel
                            size_fuel = fuel.size * fuel_amount + fuel_tank.size_fuel
                            fuel_tank = FuelTank.objects.filter(fleet_id=fleet_id, fuel_class=fuel_pattern_id).update(
                                amount_fuel=new_fuel_amount, mass_fuel=mass_fuel, size_fuel=size_fuel)

                        else:
                            fuel_tank = FuelTank(
                                fleet_id=fleet_id,
                                fuel_class=fuel_pattern_id,
                                amount_fuel=fuel_amount,
                                mass_fuel=fuel.mass * fuel_amount,
                                size_fuel=fuel.size * fuel_amount,
                                fuel_id=fuel.fuel_id
                            )
                            fuel_tank.save()

                        new_fleet_mass = fleet.ship_empty_mass + fuel.mass * fuel_amount
                        new_empty_fuel_tank = fleet.free_fuel_tank - fuel.size * fuel_amount

                        fleet = Fleet.objects.filter(id=fleet_id).update(ship_empty_mass=new_fleet_mass,
                                                                         free_fuel_tank=new_empty_fuel_tank)
                        message = 'Топливо загружено'
                    else:
                        message = 'Нехватка топлива на складе'
                else:
                    message = 'Нехватает места'
            else:
                message = 'Топливо не выбрано'
        else:
            message = 'Флот не над планетой'

        command = 4
        warehouse_elements = WarehouseElement.objects.filter(user=session_user, user_city=session_user_city,
                                                              element_class=14).order_by('element_id')
        fuel_patterns = FuelPattern.objects.filter(user=session_user)
        fuel_tanks = FuelTank.objects.filter(fleet_id=fleet_id)
        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by(
            'id_resource')
        basic_fuels = BasicFuel.objects.all()
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