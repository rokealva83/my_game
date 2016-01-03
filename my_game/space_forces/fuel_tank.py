# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity
from my_game.models import WarehouseElement, FuelPattern, BasicFuel, FuelTank
from my_game import function
from my_game.models import Ship, Fleet


def fuel_tank(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        function.check_all_queues(session_user)

        fleet_id = int(request.POST.get('hidden_fleet'))
        fuel_amount = int(request.POST.get('fuel_amount'))
        fuel_pattern_id = int(request.POST.get('fuel_pattern'))
        fleet = Fleet.objects.filter(id=fleet_id).first()
        ship_in_fleet = Ship.objects.filter(user=session_user, fleet_status=1, place_id=fleet.id).first()
        if fleet.planet_status == 1 and ship_in_fleet is not None:

            add_shipment = 0
            if int(fuel_amount) != 0 and add_shipment == 0 and fuel_pattern_id is not None:
                fuel = FuelPattern.objects.filter(id=fuel_pattern_id).first()
                size = fuel.fuel_size * int(fuel_amount)
                if size <= fleet.free_fuel_tank:
                    warehouse_element = WarehouseElement.objects.filter(user_city=session_user_city,
                                                                        element_class=14,
                                                                        element_id=fuel_pattern_id).first()
                    if warehouse_element.amount >= fuel_amount:
                        new_element_amount = warehouse_element.amount - fuel_amount
                        setattr(warehouse_element, 'amount', new_element_amount)
                        warehouse_element.save()
                        error = 0
                    else:
                        error = 1

                    if error == 0:
                        fuel_tank_obj = FuelTank.objects.filter(fleet=fleet, fuel_pattern=fuel).first()
                        if fuel_tank_obj:
                            new_fuel_amount = fuel_amount + fuel_tank_obj.amount_fuel
                            mass_fuel = fuel.fuel_mass * fuel_amount + fuel_tank_obj.mass_fuel
                            size_fuel = fuel.fuel_size * fuel_amount + fuel_tank_obj.size_fuel
                            setattr(fuel_tank_obj, 'amount_fuel', new_fuel_amount)
                            setattr(fuel_tank_obj, 'mass_fuel', mass_fuel)
                            setattr(fuel_tank_obj, 'size_fuel', size_fuel)
                            fuel_tank_obj.save()
                        else:
                            fuel_tank_obj = FuelTank(
                                fleet=fleet,
                                fuel_class=fuel.fuel_class,
                                amount_fuel=fuel_amount,
                                mass_fuel=fuel.fuel_mass * fuel_amount,
                                size_fuel=fuel.fuel_size * fuel_amount,
                                fuel_pattern=fuel,
                            )
                            fuel_tank_obj.save()

                        new_fleet_mass = fleet.ship_empty_mass + fuel.fuel_mass * fuel_amount
                        new_empty_fuel_tank = fleet.free_fuel_tank - fuel.fuel_size * fuel_amount

                        setattr(fleet, 'ship_empty_mass', new_fleet_mass)
                        setattr(fleet, 'free_fuel_tank', new_empty_fuel_tank)
                        fleet.save()
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
        fuel_patterns = FuelPattern.objects.filter(user=session_user).order_by('basic_pattern')
        fuel_tanks = FuelTank.objects.filter(fleet=fleet).order_by('fuel_pattern')
        basic_fuels = BasicFuel.objects.all()
        user_citys = UserCity.objects.filter(user=session_user).all()
        user_fleets = Fleet.objects.filter(user=session_user).all()
        ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1).all()
        ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city.id)
        request.session['userid'] = session_user.id
        request.session['user_city'] = session_user_city.id
        request.session['live'] = True
        output = {'user': session_user, 'warehouse': session_user_city.warehouse, 'user_city': session_user_city,
                  'user_citys': user_citys, 'user_fleets': user_fleets, 'fleet_id': fleet_id, 'message': message,
                  'ship_fleets': ship_fleets, 'ships': ships, 'command': command, 'fuel_patterns': fuel_patterns,
                  'fuel_tanks': fuel_tanks, 'basic_fuels': basic_fuels, 'warehouse_elements': warehouse_elements}
        return render(request, "fuel_tank.html", output)
