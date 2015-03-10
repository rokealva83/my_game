# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import Hull_pattern, Element_ship, Module_pattern
from my_game.models import MyUser, User_city
from my_game.models import Warehouse
from my_game.models import Project_ship, Ship, Fleet

from my_game import function


def delete_ship(request):
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
        command = 0
        hold = 0
        ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1)

        full_request = request.POST
        myDict = dict(full_request.iterlists())
        amount_ship_dict = myDict.get('amount_ship')
        fleet_id_dict = myDict.get('hidden_fleet')
        ship_id_dict = myDict.get('hidden_del_ship')
        len_amount_ship_dict = len(amount_ship_dict)
        for i in range(len_amount_ship_dict):
            if int(amount_ship_dict[i]) != 0:
                amount_ship = int(amount_ship_dict[i])
                fleet_id = int(fleet_id_dict[i])
                ship_id = int(ship_id_dict[i])

        fleet = Fleet.objects.filter(id=fleet_id).first()
        user_city = User_city.objects.filter(user=session_user, x=fleet.x, y=fleet.y, z=fleet.z).first()
        if user_city:
            if fleet.hold == fleet.empty_hold:
                ship = Ship.objects.filter(user=session_user, id_project_ship=ship_id, place_id=user_city.id,
                                           fleet_status=0).first()
                ship_pattern = Project_ship.objects.filter(id=ship.id_project_ship).first()
                hull_pattern = Hull_pattern.objects.filter(id=ship_pattern.hull_id).first()
                ship_elements = Element_ship.objects.filter(id_project_ship = ship.id_project_ship, class_element = 8)
                for ship_element in ship_elements:
                    element_pattern = Module_pattern.objects.filter(id=ship_element.id_element_pattern).first()
                    hold = hold + element_pattern.param1

                hold = hold + hull_pattern.hold_size

                if ship:
                    new_amount = int(ship.amount_ship) + int(amount_ship)
                    ship = Ship.objects.filter(user=session_user, id_project_ship=ship_id, place_id=user_city.id,
                                               fleet_status=0).update(amount_ship=new_amount)
                    ship = Ship.objects.filter(user=session_user, id_project_ship=ship_id, place_id=fleet_id,
                                               fleet_status=1).first()
                    new_amount = int(ship.amount_ship) - int(amount_ship)
                    if new_amount == 0:
                        ship = Ship.objects.filter(user=session_user, id_project_ship=ship_id, place_id=fleet_id,
                                                   fleet_status=1).delete()
                    else:
                        ship = Ship.objects.filter(user=session_user, id_project_ship=ship_id, place_id=fleet_id,
                                                   fleet_status=1).update(amount_ship=new_amount)

                    fleet = Fleet.objects.filter(user=session_user, id=fleet_id).first()
                    project_ship = Project_ship.objects.filter(id=ship_id).first()

                    system_power = int(fleet.system_power) - int(project_ship.system_power) * amount_ship
                    intersystem_power = int(fleet.intersystem_power) - int(project_ship.intersystem_power) * amount_ship
                    giper_power = int(fleet.giper_power) - int(project_ship.giper_power) * amount_ship
                    giper_accuracy = int(fleet.giper_accuracy) - int(project_ship.giper_accuracy) * amount_ship
                    null_power = int(fleet.null_power) - int(project_ship.null_power) * amount_ship
                    null_accuracy = int(fleet.null_accuracy) - int(project_ship.null_accuracy) * amount_ship
                    ship_empty_mass = int(fleet.ship_empty_mass) - int(project_ship.mass) * amount_ship
                    hold = int(fleet.hold) - hold * amount_ship
                    fleet = Fleet.objects.filter(user=session_user, id=fleet_id).update(
                        system_power=system_power,
                        intersystem_power=intersystem_power,
                        giper_power=giper_power,
                        giper_accuracy=giper_accuracy,
                        null_power=null_power,
                        null_accuracy=null_accuracy,
                        ship_empty_mass=ship_empty_mass,
                        hold = hold,
                        empty_hold = hold
                    )
                else:
                    project_ship = Project_ship.objects.filter(id=ship_id).first()

                    ship = Ship(
                        user=session_user,
                        id_project_ship=ship_id,
                        amount_ship=amount_ship,
                        fleet_status=0,
                        place_id=user_city.id,
                        name=project_ship.name
                    )
                    ship.save()
                    ship = Ship.objects.filter(user=session_user, id_project_ship=ship_id, place_id=fleet_id,
                                               fleet_status=1).first()
                    new_amount = int(ship.amount_ship) - int(amount_ship)
                    if new_amount == 0:
                        ship = Ship.objects.filter(user=session_user, id_project_ship=ship_id, place_id=fleet_id,
                                                   fleet_status=1).delete()
                    else:
                        ship = Ship.objects.filter(user=session_user, id_project_ship=ship_id, place_id=fleet_id,
                                                   fleet_status=1).update(amount_ship=new_amount)

                    fleet = Fleet.objects.filter(user=session_user, id=fleet_id).first()
                    project_ship = Project_ship.objects.filter(id=ship_id).first()

                    system_power = int(fleet.system_power) - int(project_ship.system_power) * amount_ship
                    intersystem_power = int(fleet.intersystem_power) - int(project_ship.intersystem_power) * amount_ship
                    giper_power = int(fleet.giper_power) - int(project_ship.giper_power) * amount_ship
                    giper_accuracy = int(fleet.giper_accuracy) - int(project_ship.giper_accuracy) * amount_ship
                    null_power = int(fleet.null_power) - int(project_ship.null_power) * amount_ship
                    null_accuracy = + int(fleet.null_accuracy) - int(project_ship.null_accuracy) * amount_ship
                    ship_empty_mass = int(fleet.ship_empty_mass) - int(project_ship.mass) * amount_ship
                    hold = int(fleet.hold) - hold * amount_ship
                    fleet = Fleet.objects.filter(user=session_user, id=fleet_id).update(
                        system_power=system_power,
                        intersystem_power=intersystem_power,
                        giper_power=giper_power,
                        giper_accuracy=giper_accuracy,
                        null_power=null_power,
                        null_accuracy=null_accuracy,
                        ship_empty_mass=ship_empty_mass,
                        hold = hold,
                        empty_hold = hold
                    )
            else:
                message = 'Трюмы не пусты'
        else:
            message = 'Флот не над планетой'

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