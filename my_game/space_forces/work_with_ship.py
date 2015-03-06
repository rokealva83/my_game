# -*- coding: utf-8 -*-


from django.shortcuts import render
from my_game.models import MyUser, User_city, Warehouse
from my_game.models import Hull_pattern, Shield_pattern, Generator_pattern, Engine_pattern, \
    Armor_pattern, Module_pattern, Weapon_pattern
from my_game import function
from my_game.models import Project_ship, Element_ship, Turn_ship_build
from my_game.designing_ships import verification_project


def modificate_ship(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])

    amount_ship = request.POST.get('amount_ship')

    modificate_ship_id = request.POST.get('hidden_ship_id')
    modificate_ship_project = Project_ship.objects.filter(id=modificate_ship_id).first()
    modificate_ship_elements = Element_ship.objects.filter(id_project_ship=modificate_ship_id)
    modificate_ship_hull_id = modificate_ship_project.hull_id
    modificate_ship_hull = Hull_pattern.objects.filter(user=session_user, id=modificate_ship_hull_id).first()

    armors = Armor_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')
    shields = Shield_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')
    engines = Engine_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')
    generators = Generator_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')
    weapons = Weapon_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')
    main_weapons = Weapon_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')
    modules = Module_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')
    turn_ship_builds = Turn_ship_build.objects.filter(user=session_user, user_city=session_user_city)
    hulls = Hull_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')
    ship_patterns = Project_ship.objects.filter(hull_id=modificate_ship_hull_id)
    warehouse = Warehouse.objects.filter(user=session_user).first()
    user_city = User_city.objects.filter(user=session_user).first()
    user = MyUser.objects.filter(user_id=session_user).first()
    user_citys = User_city.objects.filter(user=int(session_user))
    output = {'user': user, 'warehouse': warehouse, 'user_city': user_city, 'user_citys': user_citys, 'armors': armors,
              'shields': shields, 'engines': engines, 'generators': generators, 'weapons': weapons,
              'main_weapons': main_weapons, 'modules': modules, 'hulls': hulls, 'turn_ship_builds': turn_ship_builds,
              'modificate_ship_hull': modificate_ship_hull, 'modificate_ship_elements': modificate_ship_elements,
              'modificate_ship_id': modificate_ship_id, 'ship_patterns': ship_patterns, 'amount_ship': amount_ship}
    return render(request, "modificate_ship.html", output)


def choise_project(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])

    amount_ship = request.POST.get('amount_ship')

    modificate_ship_id = request.POST.get('modificate_ship_id')
    new_ship_id = request.POST.get('new_ship_id')
    modificate_ship_project = Project_ship.objects.filter(id=modificate_ship_id).first()
    new_ship_project = Project_ship.objects.filter(id=new_ship_id).first()
    modificate_ship_elements = Element_ship.objects.filter(id_project_ship=modificate_ship_id)
    new_ship_elements = Element_ship.objects.filter(id_project_ship=new_ship_id)
    modificate_ship_hull_id = modificate_ship_project.hull_id
    new_ship_hull_id = new_ship_project.hull_id
    modificate_ship_hull = Hull_pattern.objects.filter(user=session_user, id=modificate_ship_hull_id).first()
    new_ship_hull = Hull_pattern.objects.filter(user=session_user, id=new_ship_hull_id).first()
    ship_patterns = Project_ship.objects.filter(hull_id=modificate_ship_hull_id)

    armors = Armor_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')
    shields = Shield_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')
    engines = Engine_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')
    generators = Generator_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')
    weapons = Weapon_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')
    main_weapons = Weapon_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')
    modules = Module_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')
    turn_ship_builds = Turn_ship_build.objects.filter(user=session_user, user_city=session_user_city)
    hulls = Hull_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')
    warehouse = Warehouse.objects.filter(user=session_user).first()
    user_city = User_city.objects.filter(user=session_user).first()
    user = MyUser.objects.filter(user_id=session_user).first()
    user_citys = User_city.objects.filter(user=int(session_user))
    output = {'user': user, 'warehouse': warehouse, 'user_city': user_city, 'user_citys': user_citys, 'armors': armors,
              'shields': shields, 'engines': engines, 'generators': generators, 'weapons': weapons,
              'main_weapons': main_weapons, 'modules': modules, 'hulls': hulls, 'turn_ship_builds': turn_ship_builds,
              'ship_patterns': ship_patterns, 'modificate_ship_hull': modificate_ship_hull,
              'modificate_ship_elements': modificate_ship_elements, 'modificate_ship_id': modificate_ship_id,
              'new_ship_hull': new_ship_hull, 'new_ship_elements': new_ship_elements, 'new_ship_id': new_ship_id,
              'amount_ship': amount_ship}
    return render(request, "modificate_ship.html", output)


def modificate_ship_action(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])

    amount_ship = request.POST.get('amount_ship')
    modificate_ship_id = request.POST.get('hidden_ship_id')
    modificate_ship_project = Project_ship.objects.filter(id=modificate_ship_id).first()
    modificate_ship_elements = Element_ship.objects.filter(id_project_ship=modificate_ship_id)
    modificate_ship_hull_id = modificate_ship_project.hull_id
    modificate_ship_hull = Hull_pattern.objects.filter(user=session_user, id=modificate_ship_hull_id).first()

    armors = Armor_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')
    shields = Shield_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')
    engines = Engine_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')
    generators = Generator_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')
    weapons = Weapon_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')
    main_weapons = Weapon_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')
    modules = Module_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')
    turn_ship_builds = Turn_ship_build.objects.filter(user=session_user, user_city=session_user_city)
    hulls = Hull_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')
    ship_patterns = Project_ship.objects.filter(hull_id=modificate_ship_hull_id)
    warehouse = Warehouse.objects.filter(user=session_user).first()
    user_city = User_city.objects.filter(user=session_user).first()
    user = MyUser.objects.filter(user_id=session_user).first()
    user_citys = User_city.objects.filter(user=int(session_user))
    output = {'user': user, 'warehouse': warehouse, 'user_city': user_city, 'user_citys': user_citys,
              'modificate_ship_hull': modificate_ship_hull, 'armors': armors,
              'shields': shields, 'engines': engines, 'generators': generators, 'weapons': weapons,
              'main_weapons': main_weapons, 'modules': modules, 'hulls': hulls,
              'modificate_ship_elements': modificate_ship_elements,
              'turn_ship_builds': turn_ship_builds, 'modificate_ship_id': modificate_ship_id,
              'ship_patterns': ship_patterns}
    return render(request, "modificate_ship.html", output)

