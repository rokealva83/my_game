# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity
from my_game.models import ProjectShip, TurnShipBuild, Ship, ElementShip
from my_game.models import HullPattern, ShieldPattern, GeneratorPattern, EnginePattern, ArmorPattern, ModulePattern, \
    WeaponPattern


def view_ship_project(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        user_citys = UserCity.objects.filter(user=session_user)
        project_id = 1
        if request.POST.get('hidden_ship'):
            project_id = request.POST.get('hidden_ship')
            project_ship = ProjectShip.objects.filter(id=project_id).first()

        elif request.POST.get('hidden_ship_id'):
            project_ship = Ship.objects.filter(id=int(request.POST.get('hidden_ship_id'))).first().project_ship
            project_id = project_ship.id

        project_elements = ElementShip.objects.filter(project_ship=project_ship).order_by('class_element')
        hulls = HullPattern.objects.filter(user=session_user).order_by('basic_pattern')
        armors = ArmorPattern.objects.filter(user=session_user).order_by('basic_pattern')
        shields = ShieldPattern.objects.filter(user=session_user).order_by('basic_pattern')
        engines = EnginePattern.objects.filter(user=session_user).order_by('basic_pattern')
        generators = GeneratorPattern.objects.filter(user=session_user).order_by('basic_pattern')
        weapons = WeaponPattern.objects.filter(user=session_user, weapon_class__in=[1, 3]).order_by('basic_pattern')
        main_weapons = WeaponPattern.objects.filter(user=session_user, weapon_class__in=[2, 4]).order_by(
            'basic_pattern')
        modules = ModulePattern.objects.filter(user=session_user).order_by('basic_pattern')
        project_ships = ProjectShip.objects.filter(user=session_user).order_by('id')
        turn_ship_builds = TurnShipBuild.objects.filter(user=session_user, user_city=session_user_city)

        output = {'user': session_user, 'warehouse': session_user_city.warehouse, 'user_city': session_user_city,
                  'user_citys': user_citys, 'view_project': 1, 'hulls': hulls, 'project_ships': project_ships,
                  'turn_ship_builds': turn_ship_builds, 'project_id': int(project_id), 'armors': armors,
                  'shields': shields, 'engines': engines, 'generators': generators, 'weapons': weapons,
                  'main_weapons': main_weapons, 'modules': modules, 'project_elements': project_elements}
    return output
