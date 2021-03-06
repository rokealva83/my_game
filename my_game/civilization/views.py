# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import Planet, MyUser, UserCity
from my_game import function


def civilization(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        function.check_all_queues(session_user)
        user_citys = UserCity.objects.filter(user=session_user)
        planets = Planet.objects.filter(id=session_user_city.planet_id)
        len_planet = len(planets)
        request.session['user'] = session_user.id
        request.session['user_city'] = session_user_city.id
        request.session['live'] = True
        output = {'user': session_user, 'race': session_user.race, 'warehouse': session_user_city.warehouse,
                  'user_city': session_user_city, 'user_citys': user_citys, 'planet': session_user_city.planet,
                  'len_planet': len_planet}
        return render(request, "civilization.html", output)
