# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity, Warehouse
from my_game.models import HullPattern
from my_game import function
from my_game.models import ProjectShip, TurnShipBuild


def designingships(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        function.check_all_queues(session_user)
        user_citys = UserCity.objects.filter(user=session_user).all()
        hulls = HullPattern.objects.filter(user=session_user).all()
        project_ships = ProjectShip.objects.filter(user=session_user).order_by('id')
        turn_ship_builds = TurnShipBuild.objects.filter(user=session_user, user_city=session_user_city)
        request.session['user'] = session_user.id
        request.session['user_city'] = session_user_city.id
        request.session['live'] = True
        output = {'user': session_user, 'warehouses': session_user_city.warehouse, 'user_city': session_user_city,
                  'user_citys': user_citys, 'hulls': hulls, 'project_ships': project_ships,
                  'turn_ship_builds': turn_ship_builds}
        return render(request, "designingships.html", output)
