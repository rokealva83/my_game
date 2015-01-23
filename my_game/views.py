# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.template import Context
import math
import random
import sys
import string
from datetime import datetime, timedelta, date, time as dt_time
import time
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.contrib.sessions.models import Session
from models import Galaxy, System, Planet, MyUser, User_city, Warehouse, Race, User_scientic, Basic_scientic, \
    Turn_scientic, Turn_production, Turn_building
from models import Basic_scientic, Turn_scientic, Basic_armor, Basic_engine, Basic_factory, Basic_generator, \
    Basic_hull, Basic_module, Basic_shell, Basic_shield, Basic_weapon
from models import Hull_pattern, Shell_pattern, Shield_pattern, Generator_pattern, Engine_pattern, \
    Armor_pattern, Module_pattern, Factory_pattern, Weapon_pattern, Factory_installed
import function


def home(request):
    return render(request, "index.html", {})


def registr(request):
    return render(request, "registration.html", {})


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
                warehouse = Warehouse.objects.filter(user=int(user_name_auth.id)).first()
                user_city = User_city.objects.filter(user=int(user_name_auth.id)).first()
                output = {'user': user, 'warehouse': warehouse, 'city': user_city}
                request.session['userid'] = user_name_auth.id
                request.session['user_city'] = user_city.id
                request.session['live'] = True
                return render(request, "civilization.html", output)
        return render(request, "index.html", {})
    return render(request, "index.html", {})


def registration(request):
    if request.method == "POST" and request.POST.get('add_button') is not None:
        u_name = request.POST.get('name')
        ma = request.POST.get('mail')
        # valid name & E-mail
        us_name = MyUser.objects.filter(user_name=u_name).first()
        mai = MyUser.objects.filter(e_mail=ma).first()
        if us_name is not None or mai is not None:
            return HttpResponse()
        else:

            user = User(
                username=request.POST.get('name'),
                password=request.POST.get('pass'),
                last_login=datetime.today(),
                date_joined=datetime.today(),
                email=ma,
            )
            user.save()
            id_user = user.pk
            user_lucky = random.randint(1, 10)
            time_check = user.last_login
            last_time_check =datetime(time_check.year, time_check.month, time_check.day, 0, 0, 0, 0)

            myuser = MyUser(
                user_id=id_user,
                user_name=request.POST.get('name'),
                password=request.POST.get('pass'),
                race_id=request.POST.get('rac'),
                alliance_id=0,
                union_id=0,
                internal_currency=1000,
                e_mail=ma,
                referal_code=request.POST.get('name'),
                user_luckyness=user_lucky,
                last_time_check = last_time_check,
                last_time_scan_scient = last_time_check,
            )
            myuser.save()

            scientic = User_scientic(
                user=id_user,
                time_study_math=Basic_scientic.objects.get(scientic_id=1).time_study,
                time_study_phis=Basic_scientic.objects.get(scientic_id=2).time_study,
                time_study_biol=Basic_scientic.objects.get(scientic_id=3).time_study,
                time_study_ener=Basic_scientic.objects.get(scientic_id=2).time_study,
                time_study_radio=Basic_scientic.objects.get(scientic_id=4).time_study,
                time_study_nano=Basic_scientic.objects.get(scientic_id=3).time_study,
                time_study_astr=Basic_scientic.objects.get(scientic_id=1).time_study,
                time_study_logis=Basic_scientic.objects.get(scientic_id=4).time_study,
            )
            scientic.save()
            planeta = Planet.objects.filter(planet_type=int(request.POST.get('rac')), planet_free=1).first()
            warehouse = Warehouse(
                user=id_user,
            )
            warehouse.save()
            warehouse_id = warehouse.pk

            user_city = User_city(
                user=id_user,
                system_id=planeta.system_id,
                planet=planeta,
                x=planeta.x,
                y=planeta.y,
                z=planeta.z,
                city_size_free=planeta.work_area_planet,
                founding_date=datetime.today(),
                extraction_date=datetime.today()
            )
            user_city.save()
            user
            busy_id = planeta.id
            planet = Planet.objects.filter(pk=busy_id).update(planet_free=0)
            user_city = User_city.objects.filter(user = id_user).first()
            warehouse = Warehouse.objects.filter(user = id_user).update(user_city = user_city.id)

            basic_factorys = Basic_factory.objects.all()
            for basic_factory in basic_factorys:
                if basic_factory.production_class > 9:
                    factory_pattern = Factory_pattern(
                        user = id_user,
                        basic_id = basic_factory.id,
                        name = basic_factory.name,
                        price_internal_currency = basic_factory.price_internal_currency,
                        price_resource1 = basic_factory.price_resource1,
                        price_resource2 = basic_factory.price_resource2,
                        price_resource3 = basic_factory.price_resource3,
                        price_resource4 = basic_factory.price_resource4,
                        price_mineral1 = basic_factory.price_mineral1,
                        price_mineral2 = basic_factory.price_mineral2,
                        price_mineral3 = basic_factory.price_mineral3,
                        price_mineral4 = basic_factory.price_mineral4,
                        cost_expert_deployment = basic_factory.cost_expert_deployment,
                        time_deployment = basic_factory.time_deployment,
                        production_class = basic_factory.production_class,
                        production_id = basic_factory.production_id,
                        time_production =basic_factory.time_production,
                        size = basic_factory.size,
                        mass = basic_factory.mass,
                        power_consumption = basic_factory.power_consumption
                        )
                    factory_pattern.save()
            factory_patterns = Factory_pattern.objects.filter(user = id_user)
            for factory_pattern in factory_patterns:
                if factory_pattern.production_id == 1 or factory_pattern.production_id == 2:
                    factory_instelled = Factory_installed(
                            user = id_user,
                            user_city = user_city.id,
                            factory_pattern_id = factory_pattern.id,
                            name = factory_pattern.name,
                            time_deployment = factory_pattern.time_deployment,
                            production_class = factory_pattern.production_class,
                            production_id = factory_pattern.production_id,
                            time_production = factory_pattern.time_production,
                            size = factory_pattern.size,
                            mass = factory_pattern.mass,
                            power_consumption = factory_pattern.power_consumption
                        )
                    factory_instelled.save()
            factory_instelleds = Factory_installed.objects.filter(user = id_user)
            use_energy = 0
            for factory_instelled in factory_instelleds:
                if factory_instelled.production_class == 12:
                    user_city = User_city.objects.filter(user = id_user).update(power = factory_instelled.power_consumption)
                else:
                    use_energy = use_energy + factory_instelled.power_consumption
            user_city = User_city.objects.filter(user = id_user).update(use_energy = use_energy)


    elif request.POST.get('cancel_button') is not None:
        return HttpResponseRedirect(reverse('home'))
    return HttpResponseRedirect(reverse('home'))


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

3
def civilization(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        warehouse = Warehouse.objects.filter(user=session_user).first()
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouse': warehouse, 'city': user_city}
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
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'scientic': scientic, 'warehouse': warehouse, 'city': user_city,
                  'turn_scientics': turn_scientics}
        return render(request, "scientic.html", output)


def scientic_up(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        if request.method == "POST":
            number_scientic = len(Turn_scientic.objects.filter(user=session_user))
            if number_scientic < 3:
                warehouse = Warehouse.objects.filter(user=session_user).first()
                level_up = int(request.POST.get("scient"))
                scientic = int(request.POST.get("name_scient"))
                scien = Basic_scientic.objects.get(scientic_id=scientic)
                time_studys = int(scien.time_study)
                if level_up == 1:
                    time_study_turn = time_studys
                    cost_study_resource1 = int(scien.cost_resource1)
                    cost_study_resource2 = int(scien.cost_resource2)
                    cost_study_resource3 = int(scien.cost_resource3)
                    cost_study_resource4 = int(scien.cost_resource4)
                    cost_study_mineral1 = int(scien.cost_mineral1)
                    cost_study_mineral2 = int(scien.cost_mineral2)
                    cost_study_mineral3 = int(scien.cost_mineral3)
                    cost_study_mineral4 = int(scien.cost_mineral4)
                else:
                    time_study_turn = int(time_studys * int(math.exp(level_up) / 5))
                    cost_study_resource1 = int(scien.cost_resource1 * math.exp(level_up) / 5)
                    cost_study_resource2 = int(scien.cost_resource2 * math.exp(level_up) / 5)
                    cost_study_resource3 = int(scien.cost_resource3 * math.exp(level_up) / 5)
                    cost_study_resource4 = int(scien.cost_resource4 * math.exp(level_up) / 5)
                    cost_study_mineral1 = int(scien.cost_mineral1 * math.exp(level_up) / 5)
                    cost_study_mineral2 = int(scien.cost_mineral2 * math.exp(level_up) / 5)
                    cost_study_mineral3 = int(scien.cost_mineral3 * math.exp(level_up) / 5)
                    cost_study_mineral4 = int(scien.cost_mineral4 * math.exp(level_up) / 5)

                if warehouse.resource1 >= cost_study_resource1 and warehouse.resource2 >= cost_study_resource2 and \
                                warehouse.resource3 >= cost_study_resource3 and warehouse.resource4 >= cost_study_resource4 and \
                                warehouse.mineral1 >= cost_study_mineral1 and warehouse.mineral2 >= cost_study_mineral2 and \
                                warehouse.mineral3 >= cost_study_mineral3 and warehouse.mineral4 >= cost_study_mineral4:
                    new_resource1 = warehouse.resource1 - cost_study_resource1
                    new_resource2 = warehouse.resource2 - cost_study_resource2
                    new_resource3 = warehouse.resource3 - cost_study_resource3
                    new_resource4 = warehouse.resource4 - cost_study_resource4
                    new_mineral1 = warehouse.mineral1 - cost_study_mineral1
                    new_mineral2 = warehouse.mineral2 - cost_study_mineral2
                    new_mineral3 = warehouse.mineral3 - cost_study_mineral3
                    new_mineral4 = warehouse.mineral4 - cost_study_mineral4
                    warehouse = Warehouse.objects.filter(user=session_user).update(resource1=new_resource1, \
                                                                                   resource2=new_resource2, \
                                                                                   resource3=new_resource3, \
                                                                                   resource4=new_resource4, \
                                                                                   mineral1=new_mineral1, \
                                                                                   mineral2=new_mineral2, \
                                                                                   mineral3=new_mineral3, \
                                                                                   mineral4=new_mineral4)

                    turn_scientic = Turn_scientic.objects.filter(user=session_user).last()
                    if turn_scientic:
                        finish_time = turn_scientic.finish_time_science + timedelta(seconds=time_study_turn)
                    else:
                        finish_time = datetime.now() + timedelta(seconds=time_study_turn)

                    if scientic == 1:
                        turn_scientic = Turn_scientic(
                            user=session_user,
                            mathematics_up=level_up,
                            start_time_science=datetime.now(),
                            finish_time_science=finish_time,
                        )
                    if scientic == 2:
                        turn_scientic = Turn_scientic(
                            user=session_user,
                            phisics_up=level_up,
                            start_time_science=datetime.now(),
                            finish_time_science=finish_time,
                        )
                    if scientic == 3:
                        turn_scientic = Turn_scientic(
                            user=session_user,
                            biologic_chimics_up=level_up,
                            start_time_science=datetime.now(),
                            finish_time_science=finish_time,
                        )
                    if scientic == 4:
                        turn_scientic = Turn_scientic(
                            user=session_user,
                            energetics_up=level_up,
                            start_time_science=datetime.now(),
                            finish_time_science=finish_time,
                        )
                    if scientic == 5:
                        turn_scientic = Turn_scientic(
                            user=session_user,
                            radionics_up=level_up,
                            start_time_science=datetime.now(),
                            finish_time_science=finish_time,
                        )
                    if scientic == 6:
                        turn_scientic = Turn_scientic(
                            user=session_user,
                            nanotech_up=level_up,
                            start_time_science=datetime.now(),
                            finish_time_science=finish_time,
                        )
                    if scientic == 7:
                        turn_scientic = Turn_scientic(
                            user=session_user,
                            astronomy_up=level_up,
                            start_time_science=datetime.now(),
                            finish_time_science=finish_time,
                        )
                    if scientic == 8:
                        turn_scientic = Turn_scientic(
                            user=session_user,
                            logistic_up=level_up,
                            start_time_science=datetime.now(),
                            finish_time_science=finish_time,
                        )
                    turn_scientic.save()
        warehouse = Warehouse.objects.filter(user=session_user).first()
        user_city = User_city.objects.filter(user=session_user).first()
        scientic = User_scientic.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        turn_scientics = Turn_scientic.objects.filter(user=session_user)
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'scientic': scientic, 'warehouse': warehouse, 'city': user_city,
                  'turn_scientics': turn_scientics}
        return render(request, "scientic.html", output)


def warehouse(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        warehouse = Warehouse.objects.filter(user=session_user).first()
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouse': warehouse, 'city': user_city}
    return render(request, "warehouse.html", output)


def building(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = int(request.session['userid'])
        session_user_city = int(request.session['user_city'])
        function.check_all_queues(session_user)
        warehouse = Warehouse.objects.filter(user=session_user).first()
        user_city = User_city.objects.filter(user=session_user).first()
        user = MyUser.objects.filter(user_id=session_user).first()
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouse': warehouse}
        return render(request, "building.html", output)


def choice_biuld(request):
    return     


def rename(request):
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
        armor_patterns = Armor_pattern.objects.filter(user=session_user)
        request.session['userid'] = session_user
        request.session['user_city'] = session_user_city
        request.session['live'] = True
        output = {'user': user, 'warehouse': warehouse, "armor_patterns": armor_patterns}
        return render(request, "building.html", output)


def choice_module(request):
    rrrr = request.POST.get("choice")
    return ()