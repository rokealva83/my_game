# -*- coding: utf-8 -*-


from django.shortcuts import render
from my_game.models import MyUser, UserCity, Warehouse, UserVariables
from my_game.models import WarehouseElement
from my_game.models import Ship
from my_game.models import HullPattern, ShieldPattern, GeneratorPattern, EnginePattern, \
    ArmorPattern, ModulePattern, WeaponPattern
from my_game.models import ProjectShip, ElementShip, TurnShipBuild
import math
from datetime import datetime, timedelta


def modificate_ship(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()

    ship_amount = request.POST.get('amount_ship')
    hidden_amount_ship = int(request.POST.get('hidden_amount_ship'))
    modificate_ship_id = request.POST.get('hidden_ship_id')
    modificate_ship_project = ProjectShip.objects.filter(id=modificate_ship_id).first()
    modificate_ship_elements = ElementShip.objects.filter(project_ship=modificate_ship_id)
    modificate_ship_hull_id = modificate_ship_project.hull_id
    modificate_ship_hull = HullPattern.objects.filter(user=session_user, id=modificate_ship_hull_id).first()

    armors = ArmorPattern.objects.filter(user=session_user).all()
    shields = ShieldPattern.objects.filter(user=session_user).all()
    engines = EnginePattern.objects.filter(user=session_user).all()
    generators = GeneratorPattern.objects.filter(user=session_user).all()
    weapons = WeaponPattern.objects.filter(user=session_user).all()
    main_weapons = WeaponPattern.objects.filter(user=session_user).all()
    modules = ModulePattern.objects.filter(user=session_user).all()
    turn_ship_builds = TurnShipBuild.objects.filter(user=session_user, user_city=session_user_city).all()
    ship_patterns = ProjectShip.objects.filter(user=session_user).all()
    warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('resource_id')
    user_citys = UserCity.objects.filter(user=int(session_user))
    output = {'user': user, 'warehouses': warehouses, 'user_city': user_city, 'user_citys': user_citys,
              'armors': armors,
              'shields': shields, 'engines': engines, 'generators': generators, 'weapons': weapons,
              'main_weapons': main_weapons, 'modules': modules, 'turn_ship_builds': turn_ship_builds,
              'modificate_ship_hull': modificate_ship_hull, 'modificate_ship_elements': modificate_ship_elements,
              'modificate_ship_id': modificate_ship_id, 'ship_patterns': ship_patterns, 'ship_amount': ship_amount,
              'hidden_amount_ship': hidden_amount_ship}
    return render(request, "modificate_ship.html", output)
