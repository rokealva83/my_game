# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity
from my_game.models import Ship, Fleet
from my_game import function
from my_game.space_forces.ship_output import ship_output
from my_game.space_forces.fleet_parametr import fleet_parametr


def add_ship(request):
    if 'live' not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        function.check_all_queues(session_user)
        flightplans = flightplan_flights = warehouse_factorys = {}
        command = 1
        ship_id = 0
        fleet_id = 0
        message = ''
        full_request = request.POST
        my_dictionary = dict(full_request.iterlists())
        amount_ship_dict = my_dictionary.get('amount_ship')
        fleet_id_dict = my_dictionary.get('hidden_fleet')
        ship_id_dict = my_dictionary.get('hidden_ship')
        len_amount_ship_dict = int(len(amount_ship_dict))
        for i in range(len_amount_ship_dict):
            amount_ship = int(amount_ship_dict[i])
            if amount_ship:
                fleet_id = int(fleet_id_dict[i])
                ship_id = int(ship_id_dict[i])
            if amount_ship and fleet_id and ship_id:
                fleet = Fleet.objects.filter(id=fleet_id).first()
                ship = Ship.objects.filter(id=ship_id, user=session_user, fleet_status=0,
                                           place_id=session_user_city.id).first()
                city_planet = int(session_user_city.planet.id)
                fleet_planet = int(fleet.planet_id)
                if fleet.status == 0 and city_planet == fleet_planet:
                    added_ship_fleet = Ship.objects.filter(project_ship=ship.project_ship, user=session_user,
                                                           fleet_status=1, place_id=fleet.id).first()

                    if amount_ship > ship.amount_ship:
                        amount_ship = ship.amount_ship
                    if amount_ship == ship.amount_ship:
                        if added_ship_fleet:
                            new_amount = ship.amount_ship + amount_ship
                            setattr(added_ship_fleet, 'amount_ship', new_amount)
                            added_ship_fleet.save()
                            Ship.objects.filter(id=ship.id).delete()
                        else:
                            setattr(ship, 'fleet_status', 1)
                            setattr(ship, 'place_id', fleet_id)
                            ship.save()
                    else:
                        new_planet_amount = ship.amount_ship - amount_ship
                        setattr(ship, 'amount_ship', new_planet_amount)
                        ship.save()
                        if added_ship_fleet:
                            new_fleet_amount = added_ship_fleet.amount_ship + amount_ship
                            setattr(added_ship_fleet, 'amount_ship', new_fleet_amount)
                            added_ship_fleet.save()
                        else:
                            new_fleet_ship = Ship(
                                user=session_user,
                                project_ship=ship.project_ship,
                                ship_name=ship.ship_name,
                                amount_ship=amount_ship,
                                fleet_status=1,
                                place_id=fleet_id)
                            new_fleet_ship.save()

                    fleet_parametr(fleet_id, ship, amount_ship, 1)
                    message = 'Корабли добавлено во флот'
                else:
                    message = 'Флот не над планетой'
            else:
                fleet_id = int(fleet_id_dict[0])
                message = 'Неверное количество кораблей'

        request.session['user'] = session_user.id
        request.session['user_city'] = session_user_city.id
        request.session['live'] = True
        fleet = Fleet.objects.filter(id=fleet_id).first()
        output = ship_output(session_user, session_user_city, fleet, flightplans, flightplan_flights,
                             warehouse_factorys,
                             command, message)
        return render(request, "space_forces.html", output)
