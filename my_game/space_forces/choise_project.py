# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import ElementShip, ModulePattern, GeneratorPattern, EnginePattern, \
    WeaponPattern, ShieldPattern, HullPattern, ArmorPattern
from my_game.models import MyUser, UserCity
from my_game.models import ProjectShip, TurnShipBuild


def choise_project(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()

    ship_amount = request.POST.get('ship_amount')
    hidden_amount_ship = int(request.POST.get('hidden_amount_ship'))

    modificate_ship_id = request.POST.get('modificate_ship_id')
    new_ship_id = request.POST.get('new_ship_id')
    new_ship = ProjectShip.objects.get(id=new_ship_id)

    modificate_ship_project = ProjectShip.objects.filter(id=modificate_ship_id).first()
    new_ship_project = ProjectShip.objects.filter(id=new_ship_id).first()

    modificate_ship_elements = ElementShip.objects.filter(project_ship=modificate_ship_project).all()
    new_ship_elements = ElementShip.objects.filter(project_ship=new_ship).all()

    ship_patterns = ProjectShip.objects.filter(hull_pattern=modificate_ship_project.hull_pattern).all()

    armors = ArmorPattern.objects.filter(user=session_user).all()
    shields = ShieldPattern.objects.filter(user=session_user).all()
    engines = EnginePattern.objects.filter(user=session_user).all()
    generators = GeneratorPattern.objects.filter(user=session_user).all()
    weapons = WeaponPattern.objects.filter(user=session_user).all()
    main_weapons = WeaponPattern.objects.filter(user=session_user).all()
    modules = ModulePattern.objects.filter(user=session_user).all()
    turn_ship_builds = TurnShipBuild.objects.filter(user=session_user, user_city=session_user_city).all()
    hulls = HullPattern.objects.filter(user=session_user).all()
    user_citys = UserCity.objects.filter(user=session_user).all()
    output = {'user': session_user, 'warehouses': session_user_city.warehouse, 'user_city': session_user_city,
              'user_citys': user_citys, 'armors': armors, 'shields': shields, 'engines': engines,
              'generators': generators, 'weapons': weapons, 'main_weapons': main_weapons, 'modules': modules,
              'hulls': hulls, 'turn_ship_builds': turn_ship_builds, 'ship_patterns': ship_patterns,
              'modificate_ship_hull': modificate_ship_project.hull_pattern, 'modificate_ship_elements': modificate_ship_elements,
              'modificate_ship_id': modificate_ship_id, 'new_ship_hull': new_ship_project.hull_pattern,
              'new_ship_elements': new_ship_elements, 'new_ship_id': new_ship_id, 'ship_amount': ship_amount,
              'hidden_amount_ship': hidden_amount_ship}
    return render(request, "modificate_ship.html", output)
