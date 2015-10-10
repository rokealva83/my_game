# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import Planet, MyUser, UserCity, Warehouse, Race
from my_game import function


def civilization(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('id_resource')
        user = MyUser.objects.filter(user_id=session_user).first()
        user_city = UserCity.objects.filter(user=int(session_user)).first()
        user_citys = UserCity.objects.filter(user=int(session_user))
        planet = Planet.objects.filter(id=user_city.planet_id).first()
        race = Race.objects.filter(id=user.race_id).first()
        planets = Planet.objects.filter(id=user_city.planet_id)
        len_planet = len(planets)
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'race': race, 'warehouses': warehouses, 'user_city': user_city,
                  'user_citys': user_citys,
                  'planet': planet, 'len_planet': len_planet}
        return render(request, "civilization.html", output)