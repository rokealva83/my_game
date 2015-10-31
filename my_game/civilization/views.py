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
        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('resource_id')
        user_citys = UserCity.objects.filter(user=session_user)
        race = Race.objects.filter(id=session_user.race_id).first()
        planets = {}
        for user_city in user_citys:
            planet = user_city.planet
            planets.update(planet)
        len_planet = len(planets)
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': session_user, 'race': race, 'warehouses': warehouses, 'user_city': session_user_city,
                  'user_citys': user_citys,
                  'planet': session_user_city.planet, 'len_planet': len_planet}
        return render(request, "civilization.html", output)
