# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity
from my_game.models import Ship, Fleet
from my_game.space_forces.fleet_parametr import fleet_parametr

from my_game import function


def delete_ship(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        function.check_all_queues(session_user)
        flightplans = flightplan_flights = warehouse_factorys = {}
        fleet_id = ship_id = command = amount_ship = 0

        full_request = request.POST
        my_dictionary = dict(full_request.iterlists())
        amount_ship_dict = my_dictionary.get('amount_ship')
        fleet_id_dict = my_dictionary.get('hidden_fleet')
        ship_id_dict = my_dictionary.get('hidden_del_ship')
        len_amount_ship_dict = len(amount_ship_dict)
        for i in range(len_amount_ship_dict):
            if int(amount_ship_dict[i]) != 0:
                amount_ship = int(amount_ship_dict[i])
                fleet_id = int(fleet_id_dict[i])
                ship_id = int(ship_id_dict[i])

        fleet = Fleet.objects.filter(id=fleet_id).first()
        user_city = UserCity.objects.filter(user=session_user, x=fleet.x, y=fleet.y, z=fleet.z).first()
        if user_city:
            if not fleet.fleet_hold:
                removed_ship = Ship.objects.filter(id=ship_id).first()
                removed_ship_planet = Ship.objects.filter(project_ship=removed_ship.project_ship, fleet_status=0,
                                                          place_id=user_city.id).first()

                if amount_ship > removed_ship.amount_ship:
                        amount_ship = removed_ship.amount_ship

                if removed_ship.amount_ship == amount_ship:
                    if removed_ship_planet:
                        new_amount = removed_ship_planet.amount_ship + amount_ship
                        setattr(removed_ship_planet, 'amount_ship', new_amount)
                        removed_ship_planet.save()
                        Ship.objects.filter(id=ship_id).delete()
                    else:
                        setattr(removed_ship, 'fleet_status', 0)
                        setattr(removed_ship, 'place_id', user_city.id)
                        removed_ship.save()
                else:
                    new_fleet_amount = removed_ship.amount_ship - amount_ship
                    setattr(removed_ship, 'amount_ship', new_fleet_amount)
                    removed_ship.save()
                    if removed_ship_planet:
                        new_amount = removed_ship_planet.amount_ship + amount_ship
                        setattr(removed_ship_planet, 'amount_ship', new_amount)
                        removed_ship_planet.save()
                    else:
                        new_planet_ship = Ship(
                            user=session_user,
                            project_ship=removed_ship.project_ship,
                            ship_name=removed_ship.ship_name,
                            amount_ship=amount_ship,
                            fleet_status=0,
                            place_id=user_city.id
                        )
                        new_planet_ship.save()
                fleet_parametr(fleet_id, removed_ship, amount_ship, -1)
                message = 'Корабли переведены в ангар'
            else:
                message = 'Трюмы не пусты'
        else:
            message = 'Флот не над планетой'

        user_citys = UserCity.objects.filter(user=session_user).all()
        user_fleets = Fleet.objects.filter(user=session_user).all()
        ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1).all()
        ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city.id).all()
        add_ships = Ship.objects.filter(user=session_user, fleet_status=0, place_id=session_user_city.id).all()
        request.session['userid'] = session_user.id
        request.session['user_city'] = session_user_city.id
        request.session['live'] = True
        output = {'user': session_user, 'warehouses': session_user_city.warehouse, 'user_city': session_user_city,
                  'user_citys': user_citys, 'user_fleets': user_fleets, 'add_ships': add_ships, 'fleet_id': fleet_id,
                  'ship_fleets': ship_fleets, 'ships': ships, 'fleet': fleet, 'command': command,
                  'flightplans': flightplans, 'flightplan_flights': flightplan_flights,
                  'warehouse_factorys': warehouse_factorys, 'message': message}
        return render(request, "space_forces.html", output)
