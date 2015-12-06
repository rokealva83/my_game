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
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])

    ship_amount = request.POST.get('amount_ship')
    hidden_amount_ship = int(request.POST.get('hidden_amount_ship'))
    modificate_ship_id = request.POST.get('hidden_ship_id')
    modificate_ship_project = ProjectShip.objects.filter(id=modificate_ship_id).first()
    modificate_ship_elements = ElementShip.objects.filter(id_project_ship=modificate_ship_id)
    modificate_ship_hull_id = modificate_ship_project.hull_id
    modificate_ship_hull = HullPattern.objects.filter(user=session_user, id=modificate_ship_hull_id).first()

    armors = ArmorPattern.objects.filter(user=session_user).all()
    shields = ShieldPattern.objects.filter(user=session_user).all()
    engines = EnginePattern.objects.filter(user=session_user).all()
    generators = GeneratorPattern.objects.filter(user=session_user).all()
    weapons = WeaponPattern.objects.filter(user=session_user).all()
    main_weapons = WeaponPattern.objects.filter(user=session_user).all()
    modules = ModulePattern.objects.filter(user=session_user).all()
    turn_ship_builds = TurnShipBuild.objects.filter(user=session_user, user_city=session_user_city)
    ship_patterns = ProjectShip.objects.filter(user=session_user)
    warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('resource_id')
    user_city = UserCity.objects.filter(user=session_user).first()
    user = MyUser.objects.filter(user_id=session_user).first()
    user_citys = UserCity.objects.filter(user=int(session_user))
    output = {'user': user, 'warehouses': warehouses, 'user_city': user_city, 'user_citys': user_citys,
              'armors': armors,
              'shields': shields, 'engines': engines, 'generators': generators, 'weapons': weapons,
              'main_weapons': main_weapons, 'modules': modules, 'turn_ship_builds': turn_ship_builds,
              'modificate_ship_hull': modificate_ship_hull, 'modificate_ship_elements': modificate_ship_elements,
              'modificate_ship_id': modificate_ship_id, 'ship_patterns': ship_patterns, 'ship_amount': ship_amount,
              'hidden_amount_ship': hidden_amount_ship}
    return render(request, "modificate_ship.html", output)


def choise_project(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])

    ship_amount = request.POST.get('ship_amount')
    hidden_amount_ship = int(request.POST.get('hidden_amount_ship'))

    modificate_ship_id = request.POST.get('modificate_ship_id')
    new_ship_id = request.POST.get('new_ship_id')
    modificate_ship_project = ProjectShip.objects.filter(id=modificate_ship_id).first()
    new_ship_project = ProjectShip.objects.filter(id=new_ship_id).first()
    modificate_ship_elements = ElementShip.objects.filter(id_project_ship=modificate_ship_id)
    new_ship_elements = ElementShip.objects.filter(id_project_ship=new_ship_id)
    modificate_ship_hull_id = modificate_ship_project.hull_id
    new_ship_hull_id = new_ship_project.hull_id
    modificate_ship_hull = HullPattern.objects.filter(user=session_user, id=modificate_ship_hull_id).first()
    new_ship_hull = HullPattern.objects.filter(user=session_user, id=new_ship_hull_id).first()
    ship_patterns = ProjectShip.objects.filter(hull_id=modificate_ship_hull_id)

    armors = ArmorPattern.objects.filter(user=session_user).all()
    shields = ShieldPattern.objects.filter(user=session_user).all()
    engines = EnginePattern.objects.filter(user=session_user).all()
    generators = GeneratorPattern.objects.filter(user=session_user).all()
    weapons = WeaponPattern.objects.filter(user=session_user).all()
    main_weapons = WeaponPattern.objects.filter(user=session_user).all()
    modules = ModulePattern.objects.filter(user=session_user).all()
    turn_ship_builds = TurnShipBuild.objects.filter(user=session_user, user_city=session_user_city)
    hulls = HullPattern.objects.filter(user=session_user).all()
    warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('resource_id')
    user_city = UserCity.objects.filter(user=session_user).first()
    user = MyUser.objects.filter(user_id=session_user).first()
    user_citys = UserCity.objects.filter(user=int(session_user))
    output = {'user': user, 'warehouses': warehouses, 'user_city': user_city, 'user_citys': user_citys,
              'armors': armors,
              'shields': shields, 'engines': engines, 'generators': generators, 'weapons': weapons,
              'main_weapons': main_weapons, 'modules': modules, 'hulls': hulls, 'turn_ship_builds': turn_ship_builds,
              'ship_patterns': ship_patterns, 'modificate_ship_hull': modificate_ship_hull,
              'modificate_ship_elements': modificate_ship_elements, 'modificate_ship_id': modificate_ship_id,
              'new_ship_hull': new_ship_hull, 'new_ship_elements': new_ship_elements, 'new_ship_id': new_ship_id,
              'ship_amount': ship_amount, 'hidden_amount_ship': hidden_amount_ship}
    return render(request, "modificate_ship.html", output)


def action_modificate_ship(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])

    ship_amount = int(request.POST.get('ship_amount'))
    hidden_amount_ship = int(request.POST.get('hidden_amount_ship'))
    modificate_ship_id = int(request.POST.get('modificate_ship_id'))
    new_ship_id = int(request.POST.get('new_ship_id'))

    armors = ArmorPattern.objects.filter(user=session_user).all()
    shields = ShieldPattern.objects.filter(user=session_user).all()
    engines = EnginePattern.objects.filter(user=session_user).all()
    generators = GeneratorPattern.objects.filter(user=session_user).all()
    weapons = WeaponPattern.objects.filter(user=session_user).all()
    main_weapons = WeaponPattern.objects.filter(user=session_user).all()
    modules = ModulePattern.objects.filter(user=session_user).all()
    hulls = HullPattern.objects.filter(user=session_user).all()
    warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('resource_id')
    user_city = UserCity.objects.filter(user=session_user).first()
    user = MyUser.objects.filter(user_id=session_user).first()
    user_citys = UserCity.objects.filter(user=int(session_user))
    user_variables = UserVariables.objects.filter(id=1).first()

    modificate_ship_project = ProjectShip.objects.filter(id=modificate_ship_id).first()
    modificate_ship_elements = ElementShip.objects.filter(id_project_ship=modificate_ship_id)
    new_ship_elements = ElementShip.objects.filter(id_project_ship=new_ship_id)
    modificate_ship_hull_id = modificate_ship_project.hull_id
    modificate_ship_hull = HullPattern.objects.filter(user=session_user, id=modificate_ship_hull_id).first()
    ship_patterns = ProjectShip.objects.filter(hull_id=modificate_ship_hull_id)
    turn_ship_builds = TurnShipBuild.objects.filter(user=session_user, user_city=session_user_city)

    if new_ship_id is None:
        message = 'Нехватает кораблей в ангаре'
        output = {'user': user, 'warehouses': warehouses, 'user_city': user_city, 'user_citys': user_citys,
                  'armors': armors,
                  'shields': shields, 'engines': engines, 'generators': generators, 'weapons': weapons,
                  'main_weapons': main_weapons, 'modules': modules, 'turn_ship_builds': turn_ship_builds,
                  'modificate_ship_hull': modificate_ship_hull, 'modificate_ship_elements': modificate_ship_elements,
                  'modificate_ship_id': modificate_ship_id, 'ship_patterns': ship_patterns, 'ship_amount': ship_amount}
        return render(request, "modificate_ship.html", output)

    new_ship_project = ProjectShip.objects.filter(id=new_ship_id).first()
    new_ship_hull_id = new_ship_project.hull_id
    new_ship_hull = HullPattern.objects.filter(user=session_user, id=new_ship_hull_id).first()

    if ship_amount > hidden_amount_ship:
        message = 'Нехватает кораблей в ангаре'
        output = {'user': user, 'warehouses': warehouses, 'user_city': user_city, 'user_citys': user_citys,
                  'armors': armors, 'shields': shields, 'engines': engines, 'generators': generators,
                  'weapons': weapons, 'main_weapons': main_weapons, 'modules': modules, 'hulls': hulls,
                  'ship_patterns': ship_patterns, 'modificate_ship_hull': modificate_ship_hull,
                  'modificate_ship_elements': modificate_ship_elements,
                  'modificate_ship_id': modificate_ship_id, 'new_ship_hull': new_ship_hull,
                  'new_ship_elements': new_ship_elements, 'new_ship_id': new_ship_id,
                  'ship_amount': ship_amount, 'message': message}
        return render(request, "modificate_ship.html", output)

    if modificate_ship_hull_id != new_ship_hull_id:
        warehouse_element = WarehouseElement.objects.filter(user_city=session_user_city, element_class=1,
                                                             element_id=new_ship_hull_id).first()
        if warehouse_element.amount <= ship_amount:
            message = 'Нехватает комплектующих на складе'
            output = {'user': user, 'warehouses': warehouses, 'user_city': user_city, 'user_citys': user_citys,
                      'armors': armors, 'shields': shields, 'engines': engines, 'generators': generators,
                      'weapons': weapons, 'main_weapons': main_weapons, 'modules': modules, 'hulls': hulls,
                      'ship_patterns': ship_patterns, 'modificate_ship_hull': modificate_ship_hull,
                      'modificate_ship_elements': modificate_ship_elements,
                      'modificate_ship_id': modificate_ship_id, 'new_ship_hull': new_ship_hull,
                      'new_ship_elements': new_ship_elements, 'new_ship_id': new_ship_id,
                      'ship_amount': ship_amount, 'message': message}
            return render(request, "modificate_ship.html", output)

    time_build = user_variables.basic_time_build_ship

    for j in range(2, 9, 1):
        if j == 7:
            j = 6
        modificate_ship_elements = ElementShip.objects.filter(id_project_ship=modificate_ship_id,
                                                               class_element=j).order_by('position',
                                                                                         'id_element_pattern')
        new_ship_elements = ElementShip.objects.filter(id_project_ship=new_ship_id, class_element=j).order_by(
            'position',
            'id_element_pattern')
        len_modificate_ship_elements = len(modificate_ship_elements)
        len_new_ship_elements = len(new_ship_elements)
        if len_modificate_ship_elements == len_new_ship_elements:
            for i in range(len_modificate_ship_elements):
                new_ship_element = new_ship_elements[i]
                modificate_ship_element = modificate_ship_elements[i]
                if modificate_ship_element.position != new_ship_element.position or modificate_ship_element.element_pattern_id != new_ship_element.element_pattern_id:
                    time_build = time_build * 1.15
                error = error_function(session_user_city, new_ship_element, new_ship_project, ship_amount)
                if error == True:
                    message = 'Нехватает комплектующих на складе'
                    output = {'user': user, 'warehouses': warehouses, 'user_city': user_city, 'user_citys': user_citys,
                              'armors': armors, 'shields': shields, 'engines': engines, 'generators': generators,
                              'weapons': weapons, 'main_weapons': main_weapons, 'modules': modules, 'hulls': hulls,
                              'ship_patterns': ship_patterns, 'modificate_ship_hull': modificate_ship_hull,
                              'modificate_ship_elements': modificate_ship_elements,
                              'modificate_ship_id': modificate_ship_id, 'new_ship_hull': new_ship_hull,
                              'new_ship_elements': new_ship_elements, 'new_ship_id': new_ship_id,
                              'ship_amount': ship_amount, 'message': message}
                    return render(request, "modificate_ship.html", output)


        elif len_modificate_ship_elements < len_new_ship_elements:
            for i in range(len_modificate_ship_elements):
                new_ship_element = new_ship_elements[i]
                modificate_ship_element = modificate_ship_elements[i]
                if modificate_ship_element.position != new_ship_element.position or modificate_ship_element.element_pattern_id != new_ship_element.element_pattern_id:
                    time_build = time_build * 1.15
                difference = len_new_ship_elements - len_modificate_ship_elements
                time_build = time_build * math.pow(1.1, difference)
                error = error_function(session_user_city, new_ship_element, new_ship_project, ship_amount)
                if error == True:
                    message = 'Нехватает комплектующих на складе'
                    output = {'user': user, 'warehouses': warehouses, 'user_city': user_city, 'user_citys': user_citys,
                              'armors': armors, 'shields': shields, 'engines': engines, 'generators': generators,
                              'weapons': weapons, 'main_weapons': main_weapons, 'modules': modules, 'hulls': hulls,
                              'ship_patterns': ship_patterns, 'modificate_ship_hull': modificate_ship_hull,
                              'modificate_ship_elements': modificate_ship_elements,
                              'modificate_ship_id': modificate_ship_id, 'new_ship_hull': new_ship_hull,
                              'new_ship_elements': new_ship_elements, 'new_ship_id': new_ship_id,
                              'ship_amount': ship_amount, 'message': message}
                    return render(request, "modificate_ship.html", output)
            for k in range(len_modificate_ship_elements, len_new_ship_elements):
                new_ship_element = new_ship_elements[k]
                error = error_function(session_user_city, new_ship_element, new_ship_project, ship_amount)
                if error == True:
                    message = 'Нехватает комплектующих на складе'
                    output = {'user': user, 'warehouses': warehouses, 'user_city': user_city, 'user_citys': user_citys,
                              'armors': armors, 'shields': shields, 'engines': engines, 'generators': generators,
                              'weapons': weapons, 'main_weapons': main_weapons, 'modules': modules, 'hulls': hulls,
                              'ship_patterns': ship_patterns, 'modificate_ship_hull': modificate_ship_hull,
                              'modificate_ship_elements': modificate_ship_elements,
                              'modificate_ship_id': modificate_ship_id, 'new_ship_hull': new_ship_hull,
                              'new_ship_elements': new_ship_elements, 'new_ship_id': new_ship_id,
                              'ship_amount': ship_amount, 'message': message}
                    return render(request, "modificate_ship.html", output)

        else:
            for i in range(len_new_ship_elements):
                new_ship_element = new_ship_elements[i]
                modificate_ship_element = modificate_ship_elements[i]
                if modificate_ship_element.position != new_ship_element.position or modificate_ship_element.element_pattern_id != new_ship_element.element_pattern_id:
                    time_build = time_build * 1.15
                difference = len_modificate_ship_elements - len_new_ship_elements
                time_build = time_build * math.pow(1.05, difference)
                error = error_function(session_user_city, new_ship_element, new_ship_project, ship_amount)
                if error == True:
                    message = 'Нехватает комплектующих на складе'
                    output = {'user': user, 'warehouses': warehouses, 'user_city': user_city, 'user_citys': user_citys,
                              'armors': armors, 'shields': shields, 'engines': engines, 'generators': generators,
                              'weapons': weapons, 'main_weapons': main_weapons, 'modules': modules, 'hulls': hulls,
                              'ship_patterns': ship_patterns, 'modificate_ship_hull': modificate_ship_hull,
                              'modificate_ship_elements': modificate_ship_elements,
                              'modificate_ship_id': modificate_ship_id, 'new_ship_hull': new_ship_hull,
                              'new_ship_elements': new_ship_elements, 'new_ship_id': new_ship_id,
                              'ship_amount': ship_amount, 'message': message}
                    return render(request, "modificate_ship.html", output)

    for new_ship_element in new_ship_elements:
        warehouse_element = WarehouseElement.objects.filter(user_city=session_user_city,
                                                             element_class=new_ship_element.class_element,
                                                             element_id=new_ship_element.element_pattern_id).first()
        new_amount = warehouse_element.amount - (1 * ship_amount)
        warehouse_element = WarehouseElement.objects.filter(user_city=session_user_city,
                                                             element_class=new_ship_element.class_element,
                                                             element_id=new_ship_element.element_pattern_id).update(
            amount=new_amount)
        ship = Ship.objects.filter(place_id=session_user_city, id_project_ship=modificate_ship_id).first()
        new_amount = ship.amount_ship - ship_amount
        ship = Ship.objects.filter(place_id=session_user_city, id_project_ship=modificate_ship_id).update(
            amount_ship=new_amount)
    last_ship_build = TurnShipBuild.objects.filter(user=session_user, user_city=session_user_city).last()
    if last_ship_build is not None:
        start_time = last_ship_build.finish_time_build
    else:
        start_time = datetime.now()
    finish_time = start_time + timedelta(seconds=time_build)

    turn_create_ship = TurnShipBuild(
        user=session_user,
        user_city=session_user_city,
        ship_pattern=new_ship_id,
        amount=ship_amount,
        start_time_build=start_time,
        finish_time_build=finish_time,
        process_id=3
    )
    turn_create_ship.save()

    project_ships = ProjectShip.objects.filter(user=session_user).order_by('id')
    turn_ship_builds = TurnShipBuild.objects.filter(user=session_user, user_city=session_user_city)
    message = 'Модификация началась'
    output = {'user': user, 'warehouses': warehouses, 'user_city': user_city, 'user_citys': user_citys,
              'hulls': hulls, 'project_ships': project_ships, 'turn_ship_builds': turn_ship_builds, 'message': message}
    return render(request, "designingships.html", output)


def error_function(*args):
    session_user_city = args[0]
    new_ship_element = args[1]
    new_ship_project = args[2]
    ship_amount = args[3]
    id_element = new_ship_element.id_element_pattern
    class_element = new_ship_element.class_element
    amount_element = len(
        ElementShip.objects.filter(id_project_ship=new_ship_project.id, class_element=class_element,
                                    id_element_pattern=id_element)) * int(ship_amount)
    warehouse_element = WarehouseElement.objects.filter(user_city=session_user_city,
                                                         element_class=class_element,
                                                         element_id=id_element).first()
    warehouse_element_amount = int(warehouse_element.amount)

    if warehouse_element_amount < amount_element:
        error = True
    else:
        error = False
    return error