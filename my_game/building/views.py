# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity, TurnBuildingBuilding, TurnAssemblyPiecesBuilding, \
    TurnAssemblyPiecesFactory, TurnBuildingFactory
from my_game.models import ManufacturingComplex
from my_game import function


def building(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        function.check_all_queues(session_user)
        factory_turn_assembly_piecess = TurnAssemblyPiecesFactory.objects.filter(user=session_user,
                                                                                 user_city=session_user_city).all()
        building_turn_assembly_piecess = TurnAssemblyPiecesBuilding.objects.filter(user=session_user,
                                                                                   user_city=session_user_city).all()
        turn_building_buildings = TurnBuildingBuilding.objects.filter(user=session_user,
                                                                      user_city=session_user_city).all()
        turn_building_factorys = TurnBuildingFactory.objects.filter(user=session_user,
                                                                    user_city=session_user_city).all()
        manufacturing_complexs = ManufacturingComplex.objects.filter(user=session_user,
                                                                     user_city=session_user_city).all()
        user_citys = UserCity.objects.filter(user=session_user)
        request.session['user'] = session_user.id
        request.session['user_city'] = session_user_city.id
        request.session['live'] = True
        output = {'user': session_user, 'warehouse': session_user_city.warehouse, 'user_city': session_user_city,
                  'factory_turn_assembly_piecess': factory_turn_assembly_piecess,
                  'building_turn_assembly_piecess': building_turn_assembly_piecess,
                  'turn_building_buildings': turn_building_buildings, 'turn_building_factorys': turn_building_factorys,
                  'user_citys': user_citys, 'manufacturing_complexs': manufacturing_complexs}
        return render(request, "building.html", output)
