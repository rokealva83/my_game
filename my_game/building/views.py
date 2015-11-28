# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity, TurnBuilding, TurnAssemblyPieces
from my_game.models import ManufacturingComplex
from my_game import function

def building(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        function.check_all_queues(session_user)
        turn_assembly_piecess = TurnAssemblyPieces.objects.filter(user=session_user, user_city=session_user_city)
        turn_buildings = TurnBuilding.objects.filter(user=session_user, user_city=session_user_city)
        manufacturing_complexs = ManufacturingComplex.objects.filter(user=session_user, user_city=session_user_city)
        user_citys = UserCity.objects.filter(user=session_user)
        request.session['user'] = session_user.id
        request.session['user_city'] = session_user_city.id
        request.session['live'] = True
        output = {'user': session_user, 'warehouse': session_user_city.warehouse, 'user_city': session_user_city,
                  'turn_assembly_piecess': turn_assembly_piecess, 'turn_buildings': turn_buildings,
                  'user_citys': user_citys, 'manufacturing_complexs': manufacturing_complexs}
        return render(request, "building.html", output)
