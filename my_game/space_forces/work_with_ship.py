# -*- coding: utf-8 -*-


from django.shortcuts import render
from my_game.models import MyUser, User_city, Warehouse, User_variables
from my_game.models import Hull_pattern, Shield_pattern, Generator_pattern, Engine_pattern, \
    Armor_pattern, Module_pattern, Weapon_pattern
from my_game import function
from my_game.models import Project_ship, Element_ship, Turn_ship_build
from my_game.designing_ships import verification_project
import math


def modificate_ship(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])

    ship_amount = request.POST.get('amount_ship')

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
    ship_patterns = Project_ship.objects.filter(hull_id=modificate_ship_hull_id)
    warehouse = Warehouse.objects.filter(user=session_user).first()
    user_city = User_city.objects.filter(user=session_user).first()
    user = MyUser.objects.filter(user_id=session_user).first()
    user_citys = User_city.objects.filter(user=int(session_user))
    output = {'user': user, 'warehouse': warehouse, 'user_city': user_city, 'user_citys': user_citys, 'armors': armors,
              'shields': shields, 'engines': engines, 'generators': generators, 'weapons': weapons,
              'main_weapons': main_weapons, 'modules': modules, 'turn_ship_builds': turn_ship_builds,
              'modificate_ship_hull': modificate_ship_hull, 'modificate_ship_elements': modificate_ship_elements,
              'modificate_ship_id': modificate_ship_id, 'ship_patterns': ship_patterns, 'ship_amount': ship_amount}
    return render(request, "modificate_ship.html", output)


def choise_project(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])

    ship_amount = request.POST.get('ship_amount')

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
              'ship_amount': ship_amount}
    return render(request, "modificate_ship.html", output)


def action_modificate_ship(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])

    ship_amount = request.POST.get('ship_amount')
    modificate_ship_id = request.POST.get('modificate_ship_id')
    new_ship_id = request.POST.get('new_ship_id')

    modificate_ship_armor_elements = Element_ship.objects.filter(id_project_ship=modificate_ship_id,
                                                                 class_element=2).order_by('position',
                                                                                           'id_element_pattern')
    new_ship_armor_elements = Element_ship.objects.filter(id_project_ship=new_ship_id, class_element=2).order_by(
        'position',
        'id_element_pattern')
    len_modificate_armor_elements = len(modificate_ship_armor_elements)
    len_new_armor_elements = len(new_ship_armor_elements)
    user_variables = User_variables.objects.filter(id=1).first()
    time_build = user_variables.basic_time_build_ship

    if len_modificate_armor_elements == len_new_armor_elements:
        for i in range(len_modificate_armor_elements):
            new_ship_armor_element = new_ship_armor_elements[i]
            modificate_ship_armor_element = modificate_ship_armor_elements[i]
            if modificate_ship_armor_element.position != new_ship_armor_element.position or modificate_ship_armor_element.id_element_pattern != new_ship_armor_element.id_element_pattern:
                time_build = time_build * 1.15

    elif len_modificate_armor_elements < len_new_armor_elements:
        for i in range(len_modificate_armor_elements):
            new_ship_armor_element = new_ship_armor_elements[i]
            modificate_ship_armor_element = modificate_ship_armor_elements[i]
            if modificate_ship_armor_element.position != new_ship_armor_element.position or modificate_ship_armor_element.id_element_pattern != new_ship_armor_element.id_element_pattern:
                time_build = time_build * 1.15
            difference = len_new_armor_elements - len_modificate_armor_elements
            time_build = time_build * math.pow(1.1, difference)

    else:
        for i in range(len_new_armor_elements):
            new_ship_armor_element = new_ship_armor_elements[i]
            modificate_ship_armor_element = modificate_ship_armor_elements[i]
            if modificate_ship_armor_element.position != new_ship_armor_element.position or modificate_ship_armor_element.id_element_pattern != new_ship_armor_element.id_element_pattern:
                time_build = time_build * 1.15

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
              'ship_amount': ship_amount}
    return render(request, "modificate_ship.html", output)
