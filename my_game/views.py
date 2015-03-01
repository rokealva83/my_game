# -*- coding: utf-8 -*-

import math
import random
from datetime import datetime, timedelta

from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth.models import User

from my_game.models import Galaxy, System, Planet, MyUser, User_city, Warehouse, Turn_production, Turn_building, \
    Turn_assembly_pieces
from my_game.models import Hull_pattern, Shell_pattern, Shield_pattern, Generator_pattern, Engine_pattern, \
    Armor_pattern, Module_pattern, Factory_pattern, Weapon_pattern, Factory_installed
from my_game.models import Warehouse_factory, Warehouse_element
import function
import verification_func
from my_game.models import Project_ship, Element_ship, Turn_ship_build, Ship, Fleet


def home(request):
    return render(request, "index.html", {})


def cancel(request):
    return render(request, "index.html", {})


def designingships(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        warehouse = Warehouse.objects.filter(user=session_user).first()
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = User_city.objects.filter(user=int(session_user))
        hulls = Hull_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')
        project_ships = Project_ship.objects.filter(user=session_user).order_by('id')
        turn_ship_builds = Turn_ship_build.objects.filter(user=session_user, user_city=session_user_city)
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouse': warehouse, 'user_city': user_city, 'user_citys': user_citys,
                  'hulls': hulls, 'project_ships': project_ships, 'turn_ship_builds': turn_ship_builds}
        return render(request, "designingships.html", output)


def new_ship(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        armors = {}
        shields = {}
        engines = {}
        generators = {}
        weapons = {}
        main_weapons = {}
        modules = {}
        chosen_name = {}
        chosen_hull = {}
        hulls = {}
        choice_armor = []
        warehouse = Warehouse.objects.filter(user=session_user).first()
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = User_city.objects.filter(user=int(session_user))

        if request.POST.get('create_pattern'):
            chosen_hull_id = request.POST.get('choice_pattern')
            chosen_name = request.POST.get('ship_name')
            chosen_hull = Hull_pattern.objects.filter(user=session_user, id=chosen_hull_id).first()
            armors = Armor_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')
            shields = Shield_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')
            engines = Engine_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')
            generators = Generator_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')
            weapons = Weapon_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')
            main_weapons = Weapon_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')
            modules = Module_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')
            turn_ship_builds = Turn_ship_build.objects.filter(user=session_user, user_city=session_user_city)
            output = {'user': user, 'warehouse': warehouse, 'user_city': user_city, 'user_citys': user_citys,
                      'chosen_hull': chosen_hull, 'chosen_name': chosen_name, 'armors': armors,
                      'shields': shields, 'engines': engines, 'generators': generators, 'weapons': weapons,
                      'main_weapons': main_weapons, 'modules': modules, 'hulls': hulls,
                      'turn_ship_builds': turn_ship_builds}

        if request.POST.get('create_ship_pattern'):
            chosen_hull_id = int(request.POST.get('chosen_hull'))
            chosen_name = request.POST.get('chosen_hull_name')
            chosen_hull = chosen_hull = Hull_pattern.objects.filter(user=session_user, id=chosen_hull_id).first()
            hulls = Hull_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')
            new_pattern_ship = Project_ship(
                user=session_user,
                name=chosen_name,
                hull_id=chosen_hull_id
            )
            new_pattern_ship.save()
            pattern_ship_id = new_pattern_ship.pk
            time_build = 300
            hull = Hull_pattern.objects.filter(user = session_user, id = chosen_hull_id).first()
            mass = hull.mass
            full_request = request.POST
            myDict = dict(full_request.iterlists())
            choice_armor = myDict.get('choice_armor')
            choice_armor_side = myDict.get('choice_armor_side')
            if choice_armor:
                for i in range(chosen_hull.armor):
                    if int(choice_armor[i]) != 0:
                        armor = Armor_pattern.objects.filter(id=choice_armor[i]).first()
                        element = Element_ship(
                            id_project_ship=pattern_ship_id,
                            class_element=2,
                            id_element_pattern=choice_armor[i],
                            position=choice_armor_side[i],
                            health=armor.health
                        )
                        element.save()
                        time_build = time_build * 1.1
                        mass = mass + armor.mass

            choice_shield = myDict.get('choice_shield')
            choice_shield_side = myDict.get('choice_shield_side')
            if choice_shield:
                for i in range(chosen_hull.shield):
                    if int(choice_shield[i]) != 0:
                        shield = Shield_pattern.objects.filter(id=choice_shield[i]).first()
                        element = Element_ship(
                            id_project_ship=pattern_ship_id,
                            class_element=3,
                            id_element_pattern=choice_shield[i],
                            position=choice_shield_side[i],
                            health=shield.health
                        )
                        element.save()
                        time_build = time_build * 1.1
                        mass = mass + shield.mass

            choice_engine = myDict.get('choice_engine')
            system_power = 0
            intersystem_power = 0
            giper_power = 0
            null_power = 0
            if choice_engine:
                for i in range(chosen_hull.engine):
                    if int(choice_engine[i]) != 0:
                        engine = Engine_pattern.objects.filter(id=choice_engine[i]).first()
                        element = Element_ship(
                            id_project_ship=pattern_ship_id,
                            class_element=4,
                            id_element_pattern=choice_engine[i],
                            position=2,
                            health=engine.health
                        )
                        element.save()
                        system_power = system_power + engine.system_power
                        intersystem_power = intersystem_power + engine.intersystem_power
                        giper_power = giper_power + engine.giper_power
                        null_power = null_power + engine.nullT_power
                        time_build = time_build * 1.1
                        mass = mass + engine.mass

            ship_pattern = Project_ship.objects.filter(id=pattern_ship_id).update(system_power=system_power,
                                                                                  intersystem_power=intersystem_power,
                                                                                  giper_power=giper_power,
                                                                                  null_power=null_power)

            choice_generator = myDict.get('choice_generator')
            if choice_generator:
                for i in range(chosen_hull.generator):
                    if int(choice_generator[i]) != 0:
                        generator = Generator_pattern.objects.filter(id=choice_generator[i]).first()
                        element = Element_ship(
                            id_project_ship=pattern_ship_id,
                            class_element=5,
                            id_element_pattern=choice_generator[i],
                            position=0,
                            health=generator.health
                        )
                        element.save()
                        time_build = time_build * 1.1
                        mass = mass + generator.mass

            choice_weapon = myDict.get('choice_weapon')
            choice_weapon_side = myDict.get('choice_weapon_side')
            if choice_weapon:
                for i in range(chosen_hull.main_weapon):
                    if int(choice_weapon[i]) != 0:
                        weapon = Weapon_pattern.objects.filter(id=choice_weapon[i]).first()
                        element = Element_ship(
                            id_project_ship=pattern_ship_id,
                            class_element=6,
                            id_element_pattern=choice_weapon[i],
                            position=choice_weapon_side[i],
                            health=weapon.health
                        )
                        element.save()
                        time_build = time_build * 1.1
                        mass = mass + weapon.mass

            choice_main_weapon = myDict.get('choice_main_weapon')
            choice_main_weapon_side = myDict.get('choice_main_weapon_side')
            if choice_main_weapon:
                for i in range(chosen_hull.main_weapon):
                    if int(choice_main_weapon[i]) != 0:
                        weapon = Weapon_pattern.objects.filter(id=choice_weapon[i]).first()
                        element = Element_ship(
                            id_project_ship=pattern_ship_id,
                            class_element=6,
                            id_element_pattern=choice_main_weapon[i],
                            position=choice_main_weapon_side[i],
                            health=weapon.health
                        )
                        element.save()
                        time_build = time_build * 1.1
                        mass = mass + weapon.mass

            choice_module = myDict.get('choice_module')
            if choice_module:
                for i in range(chosen_hull.module):
                    if int(choice_module[i]) != 0:
                        module = Module_pattern.objects.filter(id=choice_module[i]).first()
                        element = Element_ship(
                            id_project_ship=pattern_ship_id,
                            class_element=8,
                            id_element_pattern=choice_module[i],
                            position=0,
                            health=module.health
                        )
                        element.save()
                        time_build = time_build * 1.1
                        mass = mass + module.mass

            ship_pattern = Project_ship.objects.filter(id=pattern_ship_id).update(time_build=time_build, mass = mass)
            turn_ship_builds = Turn_ship_build.objects.filter(user=session_user, user_city=session_user_city)
            project_ships = Project_ship.objects.filter(user=session_user).order_by('id')
            output = {'user': user, 'warehouse': warehouse, 'user_city': user_city, 'user_citys': user_citys,
                      'hulls': hulls, 'project_ships': project_ships, 'turn_ship_builds': turn_ship_builds}

    request.session['userid'] = session_user
    request.session['user_city'] = session_user_city
    request.session['live'] = True
    return render(request, "designingships.html", output)


def work_with_project(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        if request.POST.get('create_ship'):
            ship_id = int(request.POST.get('hidden_ship'))
            amount_ship = int(request.POST.get('amount'))
            len_turn_create_ship = len(Turn_ship_build.objects.filter(user=session_user, user_city=session_user_city))
            if len_turn_create_ship < 5:
                ship_pattern = Project_ship.objects.filter(id=ship_id).first()
                warehouse_hull = Warehouse_element.objects.filter(user=session_user, user_city=session_user_city,
                                                                  element_class=1,
                                                                  element_id=ship_pattern.hull_id).first()
                if warehouse_hull.amount >= amount_ship:
                    error = 0
                    for i in range(2, 8):
                        element_ships = Element_ship.objects.filter(id_project_ship=ship_id, class_element=i).order_by(
                            'id_element_pattern')
                        work_element_id = 0
                        if element_ships:
                            for element_ship in element_ships:
                                id_element = element_ship.id_element_pattern
                                if id_element != work_element_id:
                                    number_element = len(
                                        Element_ship.objects.filter(id_project_ship=ship_id, class_element=i,
                                                                    id_element_pattern=id_element))
                                    warehouse_element = Warehouse_element.objects.filter(user=session_user,
                                                                                         user_city=session_user_city,
                                                                                         element_class=i,
                                                                                         element_id=id_element).first()
                                    if warehouse_element <= number_element * amount_ship:
                                        error = error + 1
                                    work_element_id = id_element

                    if error == 0:
                        last_ship_build = Turn_ship_build.objects.filter(user=session_user,
                                                                         user_city=session_user_city).last()
                        if last_ship_build is not None:
                            start_time = last_ship_build.finish_time_build
                        else:
                            start_time = datetime.now()

                        ship_pattern = Project_ship.objects.filter(id=ship_id).first()
                        finish_time = start_time + timedelta(seconds=ship_pattern.time_build)
                        turn_create_ship = Turn_ship_build(
                            user=session_user,
                            user_city=session_user_city,
                            ship_pattern=ship_id,
                            amount=amount_ship,
                            start_time_build=start_time,
                            finish_time_build=finish_time

                        )
                        turn_create_ship.save()
                        warehouse_hull = Warehouse_element.objects.filter(user=session_user,
                                                                          user_city=session_user_city, element_class=1,
                                                                          element_id=ship_pattern.hull_id).first()
                        new_amount = warehouse_hull.amount - amount_ship
                        warehouse_hull = Warehouse_element.objects.filter(user=session_user,
                                                                          user_city=session_user_city, element_class=1,
                                                                          element_id=ship_pattern.hull_id).update(
                            amount=new_amount)

                        element_ships = Element_ship.objects.filter(id_project_ship=ship_id).order_by('class_element')
                        for element_ship in element_ships:
                            class_element = element_ship.class_element
                            id_element = element_ship.id_element_pattern
                            warehouse_element = Warehouse_element.objects.filter(user=session_user,
                                                                                 user_city=session_user_city,
                                                                                 element_class=class_element,
                                                                                 element_id=id_element).first()
                            new_amount = warehouse_element.amount - amount_ship
                            warehouse_element = Warehouse_element.objects.filter(user=session_user,
                                                                                 user_city=session_user_city,
                                                                                 element_class=class_element,
                                                                                 element_id=id_element).update(
                                amount=new_amount)
                        message = 'Сборка корабля начата'


                    else:
                        message = 'На складе не хватает комплектующих'
                else:
                        message = 'На складе не хватает комплектующих'

        if request.POST.get('modificate_pattern'):
            amount_ship = request.POST.get('amount')
            message = 'На складе не хватает комплектующих'

        if request.POST.get('delete_pattern'):
            ship_id = request.POST.get('hidden_ship')
            delete_ship_pattern = Project_ship.objects.filter(id=ship_id).delete()
            delete_ship_element = Element_ship.objects.filter(id_project_ship=ship_id).all().delete()

        warehouse = Warehouse.objects.filter(user=session_user).first()
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = User_city.objects.filter(user=int(session_user))
        hulls = Hull_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')
        project_ships = Project_ship.objects.filter(user=session_user).order_by('id')
        turn_ship_builds = Turn_ship_build.objects.filter(user=session_user, user_city=session_user_city)
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouse': warehouse, 'user_city': user_city, 'user_citys': user_citys,
                  'hulls': hulls, 'project_ships': project_ships, 'turn_ship_builds': turn_ship_builds, 'message':message}
        return render(request, "designingships.html", output)


def space_forces(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        warehouse = Warehouse.objects.filter(user=session_user).first()
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = User_city.objects.filter(user=int(session_user))
        user_fleets = Fleet.objects.filter(user=session_user)
        ships = Ship.objects.filter(user = session_user, fleet_status = 0, place_id = session_user_city)
        ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1)
        command = 0
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouse': warehouse, 'user_city': user_city, 'user_citys': user_citys,
                  'user_fleets': user_fleets, 'ships': ships, 'ship_fleets':ship_fleets, 'command':command}
        return render(request, "space_forces.html", output)


def trade(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        warehouse = Warehouse.objects.filter(user=session_user).first()
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = User_city.objects.filter(user=int(session_user))
        user_fleets = Fleet.objects.filter(user=session_user)
        ships = Ship.objects.filter(user = session_user, fleet_status = 0, place_id = session_user_city)
        ship_fleets = Ship.objects.filter(user=session_user, fleet_status=1)
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouse': warehouse, 'user_city': user_city, 'user_citys': user_citys,
                  'user_fleets': user_fleets, 'ships': ships, 'ship_fleets':ship_fleets}
        return render(request, "trade.html", output)