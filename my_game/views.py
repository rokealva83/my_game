# -*- coding: utf-8 -*-

import math
import random
from datetime import datetime

from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from datetime import datetime, timedelta, date, time as dt_time
from models import Galaxy, System, Planet, MyUser, User_city, Warehouse, User_scientic, Turn_production, Turn_building, \
    Turn_assembly_pieces
from models import Basic_scientic, Turn_scientic, Basic_factory
from models import Hull_pattern, Shell_pattern, Shield_pattern, Generator_pattern, Engine_pattern, \
    Armor_pattern, Module_pattern, Factory_pattern, Weapon_pattern, Factory_installed
from models import Warehouse_factory, Warehouse_element
import function
import scientic_work
import scientic_func
import verification_func
from models import User_variables
from models import Project_ship, Element_ship, Turn_ship_build, Ship, Fleet


def home(request):
    return render(request, "index.html", {})


def cancel(request):
    return render(request, "index.html", {})


def auth(request):
    if request.method == "POST" and request.POST.get('add_button') is not None:
        user_name_post = request.POST.get('name')
        password_post = request.POST.get('pass')
        user_name_auth = User.objects.filter(username=user_name_post).first()
        if user_name_auth is not None:
            if user_name_auth.password == password_post:
                user = MyUser.objects.filter(user_id=user_name_auth.id).first()
                user_id = user.pk
                warehouse = Warehouse.objects.filter(user=int(user_name_auth.id)).first()
                user_city = User_city.objects.filter(user=int(user_name_auth.id)).first()
                user_citys = User_city.objects.filter(user=int(user_name_auth.id))
                planet = Planet.objects.filter(id = user_city.planet_id).first()
                function.check_all_queues(user_id)
                output = {'user': user, 'warehouse': warehouse, 'user_city': user_city, 'user_citys': user_citys, 'planet':planet}
                request.session['userid'] = user_name_auth.id
                request.session['user_city'] = user_city.id
                request.session['live'] = True
                return render(request, "civilization.html", output)
        return render(request, "index.html", {})
    return render(request, "index.html", {})


def gener(request):
    return render(request, "admin/generation.html", {})


def generation(request):
    if request.method == "POST" and request.POST.get('add_button') is not None:
        system_id = 1
        r = 5
        a = 45
        star = int(request.POST.get('star', None))
        iter = 0
        gal = [[0, 0, 0, 0, 0, 0, 0, 0]]
        x2 = 0
        y2 = 0
        z2 = 0
        size2 = 0
        galaxy = Galaxy(
            x=0,
            y=0,
            z=0
        )
        galaxy.save()
        while (system_id <= star):
            # coordinates of systems
            # print "coordinates of systems"
            mark = 1
            while mark > 0:
                mark = 0
                sys = []
                sys.append(int(system_id))

                # generate coordinates
                Zm = random.randint(0, 20)
                x = 2 * (r + Zm) * math.cos(a)
                Zm = random.randint(0, 20)
                y = 1.5 * (r + Zm) * math.sin(a)
                z = random.randint(-30, 30)
                system_size = random.randint(4000, 9000)
                system_size = float(system_size)
                system_size = system_size / 1000
                sys.append(int(x))
                sys.append(int(y))
                sys.append(int(z))
                sys.append(system_size)

                # classification of stars
                k = random.random()
                if k > 0.05:
                    star_type = 0
                else:
                    star_type = 1
                sys.append(star_type)

                # valid_test
                for i in range(iter):
                    j = 2
                    x2 = gal[i][j]
                    y2 = gal[i][j + 1]
                    z2 = gal[i][j + 2]
                    size2 = gal[i][j + 3]
                ligth = math.sqrt((x - x2) ** 2 + (y - y2) ** 2 + (z - z2) ** 2)
                size = system_size + size2
                if 2 * size > ligth:
                    mark = mark + 1

            # radius orbite of planet (static-files)
            radius_star = round(system_size / 3 * 1000, 2)
            radius = (system_size * 1000 - (radius_star)) / 12

            system = System(
                galaxy_id=1,
                x=x,
                y=y,
                z=z,
                system_type=star_type,
                system_size=system_size,
                star_size=radius_star
            )
            system.save()

            # the number of planets
            k = random.random()
            if 0.01 > k:
                n = 0
            else:
                if 0.01 <= k <= 0.1:
                    n = random.randint(1, 4)
                else:
                    if 0.1 < k < 0.3:
                        n = random.randint(10, 12)
                    else:
                        n = random.randint(5, 9)

            plans = [[0, 0, 0, 0, 0]]
            # valid test
            for ii in range(n):
                q = ii
                mark1 = 1
                while mark1 > 0:
                    planet_id = random.randint(1, 12)
                    mark1 = 0
                    for jj in range(q + 1):
                        w = int(plans[jj][0])
                        if planet_id == w:
                            mark1 = mark1 + 1

                # generate planet koordinate and radius orbite
                plan = []
                plan.append(planet_id)
                aa = random.randint(1, 360)
                dev = random.randint(-25, 25)
                orb_radius = radius_star + planet_id * radius
                xx = orb_radius * math.cos(aa)
                yy = orb_radius * math.sin(aa)
                zz = random.randint(-15, 15)
                plan.append(int(xx))
                plan.append(int(yy))
                plan.append(zz)

                # generate size and classification of planet
                planet_type = 0
                planet_size = radius / random.randint(8, 12)
                planet_type = random.randint(1, 5)
                plan.append(planet_type)
                plan.append(round(planet_size, 3))

                planet_area = 4 * math.pi * planet_size
                planet_work_area = planet_area * 0.65 * 100
                plan.append(round(planet_work_area))


                # angle and the motion vector of the planets in the system
                planet_displacement_vector = round(random.randint(0, 1))
                if planet_displacement_vector == 0:
                    planet_displacement_vector = -1
                planet_offset_angle = round(360.000000 / random.randint(200, 1000), 8)
                plan.append(planet_offset_angle)
                plan.append(planet_displacement_vector)

                planet = Planet(
                    system_id=system_id,
                    x=xx,
                    y=yy,
                    z=zz,
                    planet_num=planet_id,
                    planet_type=planet_type,
                    planet_size=planet_size,
                    orb_radius=orb_radius,
                    area_planet=planet_area,
                    work_area_planet=planet_work_area,
                    planet_displacement_vector=planet_displacement_vector,
                    planet_offset_angle=planet_offset_angle
                )
                planet.save()
                plans.append(plan)
                plans.sort()
            gal.append(sys)
            system_id = system_id + 1
            iter = iter + 1
            r = r + 1
            a = a + 15
    return HttpResponse("Hello, World")


def civilization(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        warehouse = Warehouse.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_city = User_city.objects.filter(user=int(session_user)).first()
        user_citys = User_city.objects.filter(user=int(session_user))
        planet = Planet.objects.filter(id=user_city.planet_id).first()
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouse': warehouse, 'user_city': user_city, 'user_citys': user_citys,
                  'planet': planet}
        return render(request, "civilization.html", output)


def scientic(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        warehouse = Warehouse.objects.filter(user=session_user).first()
        user_city = User_city.objects.filter(user=session_user).first()
        scientic = User_scientic.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        turn_scientics = Turn_scientic.objects.filter(user=session_user)
        user_citys = User_city.objects.filter(user=int(session_user))
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'scientic': scientic, 'warehouse': warehouse, 'user_city': user_city,
                  'turn_scientics': turn_scientics, 'user_citys': user_citys}
        return render(request, "scientic.html", output)


def scientic_up(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        if request.method == "POST":
            level_up = int(request.POST.get("scient"))
            scientic = int(request.POST.get("name_scient"))
            scientic_work.scien_up(session_user, level_up, scientic)
        warehouse = Warehouse.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_city = User_city.objects.filter(user=session_user).first()
        scientic = User_scientic.objects.filter(user=session_user).first()
        turn_scientics = Turn_scientic.objects.filter(user=session_user)
        user_citys = User_city.objects.filter(user=int(session_user))
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'scientic': scientic, 'warehouse': warehouse, 'user_city': user_city,
                  'turn_scientics': turn_scientics, 'user_citys': user_citys}
        return render(request, "scientic.html", output)


def warehouse(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        warehouse = Warehouse.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_city = User_city.objects.filter(user=session_user).first()
        user_citys = User_city.objects.filter(user=int(session_user))
        warehouse_factorys = Warehouse_factory.objects.filter(user=session_user, user_city=session_user_city).order_by(
            'production_class', 'production_id')
        factory_patterns = Factory_pattern.objects.filter(user=session_user)
        warehouse_elements = Warehouse_element.objects.filter(user=session_user, user_city=session_user_city).order_by(
            'element_class', 'element_id')
        hull_patterns = Hull_pattern.objects.filter(user=session_user)
        armor_patterns = Armor_pattern.objects.filter(user=session_user)
        shield_patterns = Shield_pattern.objects.filter(user=session_user)
        engine_patterns = Engine_pattern.objects.filter(user=session_user)
        generator_patterns = Generator_pattern.objects.filter(user=session_user)
        weapon_patterns = Weapon_pattern.objects.filter(user=session_user)
        shell_patterns = Shell_pattern.objects.filter(user=session_user)
        module_patterns = Module_pattern.objects.filter(user=session_user)
        # device_patterns = Device_pattern.objects.filter(user = session_user)
        attribute_factorys = ("cost_expert_deployment", "assembly_workpiece", "time_deployment", "production_class", \
                              "production_id", "time_production", "size", "mass", "power_consumption")
        attribute_hulls = ("health", "generator", "engine", "weapon", "armor", "shield", "main_weapon", "module", \
                           "hold_size", "size", "mass", "power_consuption")
        attribute_armors = ("health", "value_energy_resistance", "value_phisical_resistance", "power", "regeneration", \
                            "mass")
        attribute_shields = ("health", "value_energy_resistance", "value_phisical_resistance", "number_of_emitter", \
                             "regeneration", "mass", "size", "power_consuption")
        attribute_engines = ("health", "system_power", "intersystem_power", "giper_power", "nullT_power", \
                             "regeneration", "mass", "size", "power_consuption")
        attribute_generators = ("health", "produced_energy", "fuel_necessary", "mass", "size")
        attribute_weapons = ("health", "energy_damage", "regenerations", "number_of_bursts", "range", "accuracy", \
                             "mass", "size", "power_consuption")
        attribute_shells = ("phisical_damage", "speed", "mass", "size")
        attribute_modules = ("health", "param1", "param2", "param3", "mass", "size", "power_consuption")

    request.session['userid'] = session_user
    request.session['user_city'] = session_user_city
    request.session['live'] = True
    output = {'user': user, 'warehouse': warehouse, 'user_city': user_city, 'user_citys': user_citys,
              'warehouse_factorys': warehouse_factorys, 'factory_patterns': factory_patterns,
              'warehouse_elements': warehouse_elements, 'hull_patterns': hull_patterns,
              'armor_patterns': armor_patterns, 'shield_patterns': shield_patterns,
              'engine_patterns': engine_patterns, 'generator_patterns': generator_patterns,
              'weapon_patterns': weapon_patterns, 'shell_patterns': shell_patterns, 'module_patterns': module_patterns,
              'attribute_factorys': attribute_factorys, 'attribute_hulls': attribute_hulls,
              'attribute_armors': attribute_armors, 'attribute_shields': attribute_shields,
              'attribute_engines': attribute_engines, 'attribute_generators': attribute_generators,
              'attribute_weapons': attribute_weapons, 'attribute_shells': attribute_shells,
              'attribute_modules': attribute_modules, }
    return render(request, "warehouse.html", output)


def building(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        turn_assembly_piecess = Turn_assembly_pieces.objects.filter(user=session_user, user_city=session_user_city)
        turn_buildings = Turn_building.objects.filter(user=session_user, user_city=session_user_city)
        warehouse = Warehouse.objects.filter(user=session_user).first()
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = User_city.objects.filter(user=int(session_user))
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouse': warehouse, 'user_city': user_city,
                  'turn_assembly_piecess': turn_assembly_piecess, 'turn_buildings': turn_buildings,
                  'user_citys': user_citys}
        return render(request, "building.html", output)


def choice_build(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        verification_func.check_assembly_line_workpieces(session_user)
        factory_patterns = {}
        attributes = ("name", "price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                      "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                      "cost_expert_deployment", "assembly_workpiece", "time_deployment", "production_class",
                      "production_id", "time_production", "size", "mass", "power_consumption")
        if request.POST.get('housing_unit') is not None:
            factory_patterns = Factory_pattern.objects.filter(user=session_user, production_class=10).order_by(
                'production_id')
        if request.POST.get('mine') is not None:
            factory_patterns = Factory_pattern.objects.filter(user=session_user, production_class=11).order_by(
                'production_id')
        if request.POST.get('energy_unit') is not None:
            factory_patterns = Factory_pattern.objects.filter(user=session_user, production_class=12).order_by(
                'production_id')
        if request.POST.get('hull') is not None:
            factory_patterns = Factory_pattern.objects.filter(user=session_user, production_class=1).order_by(
                'production_id')
        if request.POST.get('armor') is not None:
            factory_patterns = Factory_pattern.objects.filter(user=session_user, production_class=2).order_by(
                'production_id')
        if request.POST.get('shield') is not None:
            factory_patterns = Factory_pattern.objects.filter(user=session_user, production_class=3).order_by(
                'production_id')
        if request.POST.get('engine') is not None:
            factory_patterns = Factory_pattern.objects.filter(user=session_user, production_class=4).order_by(
                'production_id')
        if request.POST.get('generator') is not None:
            factory_patterns = Factory_pattern.objects.filter(user=session_user, production_class=5).order_by(
                'production_id')
        if request.POST.get('weapon') is not None:
            factory_patterns = Factory_pattern.objects.filter(user=session_user, production_class=6).order_by(
                'production_id')
        if request.POST.get('shell') is not None:
            factory_patterns = Factory_pattern.objects.filter(user=session_user, production_class=7).order_by(
                'production_id')
        if request.POST.get('module') is not None:
            factory_patterns = Factory_pattern.objects.filter(user=session_user, production_class=8).order_by(
                'production_id')
            # if request.POST.get('device') is not None:
        # factory_patterns = Factory_pattern.objects.filter(user=session_user, production_class=9).order_by('production_id')
        turn_assembly_piecess = Turn_assembly_pieces.objects.filter(user=session_user, user_city=session_user_city)
        turn_buildings = Turn_building.objects.filter(user=session_user, user_city=session_user_city)
        warehouse = Warehouse.objects.filter(user=session_user).first()
        warehouse_elements = Warehouse_factory.objects.filter(user=session_user, user_city=session_user_city)
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = User_city.objects.filter(user=int(session_user))
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouse': warehouse, 'user_city': user_city, 'factory_patterns': factory_patterns,
                  'attributes': attributes, 'turn_assembly_piecess': turn_assembly_piecess,
                  'turn_buildings': turn_buildings, 'warehouse_elements': warehouse_elements, 'user_citys': user_citys}

        return render(request, "building.html", output)


def working(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        verification_func.check_assembly_line_workpieces(session_user)
        message = ''

        if request.POST.get('rename_factory_pattern') is not None:
            new_name = request.POST.get('rename_factory_pattern')
            pattern_id = request.POST.get('hidden_factory')
            message = function.rename_factory_pattern(new_name, pattern_id)

        if request.POST.get('upgrade_factory_pattern') is not None:
            number = request.POST.get('number')
            speed = request.POST.get('speed')
            pattern_id = request.POST.get('hidden_factory')
            message = function.upgrade_factory_pattern(number, speed, pattern_id)

        if request.POST.get('delete_factory_pattern') is not None:
            pattern_id = request.POST.get('hidden_factory')
            message = function.delete_factory_pattern(pattern_id)

        if request.POST.get('making_factory_unit') is not None:
            amount_factory_unit = request.POST.get('amount_factory')
            pattern_id = request.POST.get('hidden_factory')
            message = function.making_factory_unit(session_user, session_user_city, amount_factory_unit, pattern_id)

        if request.POST.get('install_factory_unit') is not None:
            pattern_id = request.POST.get('hidden_factory')
            message = function.install_factory_unit(session_user, session_user_city, pattern_id)

        turn_assembly_piecess = Turn_assembly_pieces.objects.filter(user=session_user, user_city=session_user_city)
        turn_buildings = Turn_building.objects.filter(user=session_user, user_city=session_user_city)
        warehouse = Warehouse.objects.filter(user=session_user).first()
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouse': warehouse, 'user_city': user_city, 'message': message,
                  'turn_assembly_piecess': turn_assembly_piecess, 'turn_buildings': turn_buildings}
        return render(request, "building.html", output)


def factory(request):
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
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouse': warehouse, 'user_city': user_city, 'user_citys': user_citys}
        return render(request, "factory.html", output)


def choice_element(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        verification_func.check_assembly_line_workpieces(session_user)
        verification_func.verification_stage_production(session_user)
        if request.POST.get('hull') is not None:
            attributes = ("name", "price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "health", "generator", "engine", "weapon", "armor", "shield", "main_weapon", "module",
                          "hold_size", "size", "mass", "power_consuption")
            factory_installeds = Factory_installed.objects.filter(user=session_user, production_class=1).order_by(
                'production_id')
            element_patterns = Hull_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        if request.POST.get('armor') is not None:
            attributes = ("name", "price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "health", "value_energy_resistance", "value_phisical_resistance", "power", "regeneration",
                          "mass")
            factory_installeds = Factory_installed.objects.filter(user=session_user, production_class=2).order_by(
                'production_id')
            element_patterns = Armor_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        if request.POST.get('shield') is not None:
            attributes = ("name", "price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "health", "value_energy_resistance", "value_phisical_resistance", "number_of_emitter",
                          "regeneration",
                          "mass", "size", "power_consuption")
            factory_installeds = Factory_installed.objects.filter(user=session_user, production_class=3).order_by(
                'production_id')
            element_patterns = Shield_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        if request.POST.get('engine') is not None:
            attributes = ("name", "price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "health", "system_power", "intersystem_power", "giper_power", "nullT_power", "regeneration",
                          "mass", "size", "power_consuption")
            factory_installeds = Factory_installed.objects.filter(user=session_user, production_class=4).order_by(
                'production_id')
            element_patterns = Engine_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        if request.POST.get('generator') is not None:
            attributes = ("name", "price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "health", "produced_energy", "fuel_necessary", "mass", "size")
            factory_installeds = Factory_installed.objects.filter(user=session_user, production_class=5).order_by(
                'production_id')
            element_patterns = Generator_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        if request.POST.get('weapon') is not None:
            attributes = ("name", "price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "health", "energy_damage", "regenerations", "number_of_bursts", "range", "accuracy", "mass",
                          "size", "power_consuption")
            factory_installeds = Factory_installed.objects.filter(user=session_user, production_class=6).order_by(
                'production_id')
            element_patterns = Weapon_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        if request.POST.get('shell') is not None:
            attributes = ("name", "price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "phisical_damage", "speed", "mass", "size")
            factory_installeds = Factory_installed.objects.filter(user=session_user, production_class=7).order_by(
                'production_id')
            element_patterns = Shell_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        if request.POST.get('module') is not None:
            attributes = ("name", "price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
                          "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
                          "health", "param1", "param2", "param3", "mass", "size", "power_consuption")
            factory_installeds = Factory_installed.objects.filter(user=session_user, production_class=8).order_by(
                'production_id')
            element_patterns = Module_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')

            # if request.POST.get('device') is not None:
        # attributes = ("name", "price_internal_currency", "price_resource1", "price_resource2", "price_resource3",
        # "price_resource4", "price_mineral1", "price_mineral2", "price_mineral3", "price_mineral4",
        # "health", "produced_energy", "fuel_necessary",  "mass", "size", "power_consuption")
        # factory_installeds = Factory_installed.objects.filter(user=session_user, production_class=9).order_by(
        # 'production_id')
        # element_patterns = Device_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')

        warehouse = Warehouse.objects.filter(user=session_user).first()
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        turn_productions = Turn_production.objects.filter(user=session_user, user_city=session_user_city)
        user_citys = User_city.objects.filter(user=int(session_user))
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouse': warehouse, 'user_city': user_city,
                  'factory_installeds': factory_installeds, 'element_patterns': element_patterns,
                  'attributes': attributes, 'turn_productions': turn_productions, 'user_citys': user_citys}
        return render(request, "factory.html", output)
    return render(request, "index.html", {})


def production(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        verification_func.check_assembly_line_workpieces(session_user)
        if request.POST.get('rename_element_pattern'):
            new_name = request.POST.get('new_name')
            pattern_id = request.POST.get('hidden_factory')
            element_id = request.POST.get('hidden_element')
            message = function.rename_element_pattern(session_user, session_user_city, pattern_id, element_id, new_name)

        if request.POST.get('buttom_amount_element'):
            factory_id = request.POST.get('hidden_factory')
            element_id = request.POST.get('hidden_element')
            amount_element = request.POST.get('amount_element')
            message = function.production_module(session_user, session_user_city, factory_id, element_id,
                                                 amount_element)

        if request.POST.get('disassembling'):
            factory_id = request.POST.get('hidden_factory')
            turn_production = Turn_production.objects.filter(factory_id=factory_id).first()
            user_city = User_city.objects.filter(id=session_user_city).first()
            if turn_production:
                message = 'На фабрике идет производство. Удаление невозможно'
            else:
                delete_factory = Factory_installed.objects.filter(id=factory_id).first()
                return_factory = Warehouse_factory.objects.filter(factory_id=delete_factory.factory_pattern_id).first()
                new_amount = return_factory.amount + 1
                return_factory = Warehouse_factory.objects.filter(factory_id=delete_factory.factory_pattern_id).update(
                    amount=new_amount)
                new_energy = user_city.use_energy - delete_factory.power_consumption
                user_city = User_city.objects.filter(id=session_user_city).update(use_energy=new_energy)
                delete_factory = Factory_installed.objects.filter(id=factory_id).delete()
                message = 'Фабрика удалена'

        turn_productions = Turn_production.objects.filter(user=session_user, user_city=session_user_city)
        warehouse = Warehouse.objects.filter(user=session_user).first()
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        user_citys = User_city.objects.filter(user=int(session_user))
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouse': warehouse, 'user_city': user_city, 'message': message,
                  'turn_productions': turn_productions, 'user_citys': user_citys}
        return render(request, "factory.html", output)


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