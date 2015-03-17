# -*- coding: utf-8 -*-

import random

from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from datetime import datetime
from my_game.models import Planet
from my_game.models import User_variables
from my_game.models import MyUser
from my_game.models import User_city, Warehouse, User_scientic, Basic_scientic, Basic_factory, Factory_pattern, \
    Factory_installed
from my_game import function


def registration(request):
    return render(request, "registration.html", {})


def add_user(request):
    if request.method == "POST" and request.POST.get('add_button') is not None:
        u_name = request.POST.get('name')
        ma = request.POST.get('mail')
        # valid name & E-mail
        us_name = MyUser.objects.filter(user_name=u_name).first()
        mai = MyUser.objects.filter(e_mail=ma).first()
        if us_name is not None or mai is not None:
            return HttpResponse()
        else:
            user_variables = User_variables.objects.filter(id = 1).first()
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
            last_time_check = datetime(time_check.year, time_check.month, time_check.day, 0, 0, 0, 0)

            myuser = MyUser(
                user_id=id_user,
                user_name=request.POST.get('name'),
                password=request.POST.get('pass'),
                race_id=request.POST.get('rac'),
                alliance_id=0,
                union_id=0,
                internal_currency=user_variables.registr_internal_currency,
                e_mail=ma,
                referal_code=request.POST.get('name'),
                user_luckyness=user_lucky,
                last_time_check=last_time_check,
                last_time_scan_scient=last_time_check,
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
            busy_id = planeta.id
            planet = Planet.objects.filter(pk=busy_id).update(planet_free=0)
            user_city = User_city.objects.filter(user=id_user).first()


            warehouse = Warehouse(
                user = id_user,
                user_city = user_city.id,
                id_resource = 1,
                amount = user_variables.registr_resource1
            )
            warehouse.save()
            warehouse = Warehouse(
                user = id_user,
                user_city = user_city.id,
                id_resource = 2,
                amount = user_variables.registr_resource2
            )
            warehouse.save()

            basic_factorys = Basic_factory.objects.all()
            for basic_factory in basic_factorys:
                if basic_factory.production_class > 9:
                    factory_pattern = Factory_pattern(
                        user=id_user,
                        basic_id=basic_factory.id,
                        name=basic_factory.name,
                        price_internal_currency=basic_factory.price_internal_currency,
                        price_resource1=basic_factory.price_resource1,
                        price_resource2=basic_factory.price_resource2,
                        price_resource3=basic_factory.price_resource3,
                        price_resource4=basic_factory.price_resource4,
                        price_mineral1=basic_factory.price_mineral1,
                        price_mineral2=basic_factory.price_mineral2,
                        price_mineral3=basic_factory.price_mineral3,
                        price_mineral4=basic_factory.price_mineral4,
                        cost_expert_deployment=basic_factory.cost_expert_deployment,
                        assembly_workpiece=basic_factory.assembly_workpiece,
                        time_deployment=basic_factory.time_deployment,
                        production_class=basic_factory.production_class,
                        production_id=basic_factory.production_id,
                        time_production=basic_factory.time_production,
                        size=basic_factory.size,
                        mass=basic_factory.mass,
                        power_consumption=basic_factory.power_consumption
                    )
                    factory_pattern.save()
            factory_patterns = Factory_pattern.objects.filter(user=id_user)
            for factory_pattern in factory_patterns:
                if factory_pattern.production_id == 1 or factory_pattern.production_id == 2:
                    factory_instelled = Factory_installed(
                        user=id_user,
                        user_city=user_city.id,
                        factory_pattern_id=factory_pattern.id,
                        name=factory_pattern.name,
                        time_deployment=factory_pattern.time_deployment,
                        production_class=factory_pattern.production_class,
                        production_id=factory_pattern.production_id,
                        time_production=factory_pattern.time_production,
                        size=factory_pattern.size,
                        mass=factory_pattern.mass,
                        power_consumption=factory_pattern.power_consumption
                    )
                    factory_instelled.save()
            factory_instelleds = Factory_installed.objects.filter(user=id_user)
            use_energy = 0
            use_area = 0
            for factory_instelled in factory_instelleds:
                use_area = factory_instelled.size + use_area
                if factory_instelled.production_class == 12:
                    user_city = User_city.objects.filter(user=id_user).update(power=factory_instelled.power_consumption)
                else:
                    use_energy = use_energy + factory_instelled.power_consumption
            user_city = User_city.objects.filter(user=id_user).first()
            free_area = user_city.city_size_free - use_area
            user_city = User_city.objects.filter(user=id_user).update(use_energy=use_energy, city_size_free=free_area)


    elif request.POST.get('cancel_button') is not None:
        return render(request, "index.html", {})
    return render(request, "index.html", {})


def auth(request):
    if request.method == "POST" and request.POST.get('add_button') is not None:
        user_name_post = request.POST.get('name')
        password_post = request.POST.get('pass')
        user_name_auth = User.objects.filter(username=user_name_post).first()
        if user_name_auth is not None:
            if user_name_auth.password == password_post:
                user = MyUser.objects.filter(user_id=user_name_auth.id).first()
                user_id = user.user_id
                user_city = User_city.objects.filter(user = user_id).first()
                warehouses = Warehouse.objects.filter(user=user_id, user_city = user_city.id).order_by('id_resource')
                user_city = User_city.objects.filter(user=int(user_name_auth.id)).first()
                user_citys = User_city.objects.filter(user=int(user_name_auth.id))
                planet = Planet.objects.filter(id=user_city.planet_id).first()
                function.check_all_queues(user_id)
                output = {'user': user, 'warehouses': warehouses, 'user_city': user_city, 'user_citys': user_citys,
                          'planet': planet}
                request.session['userid'] = user_name_auth.id
                request.session['user_city'] = user_city.id
                request.session['live'] = True
                return render(request, "civilization.html", output)
        else:
            message = 'Неверно введено имя или пароль пользователя'
            output = {'message': message}
        return render(request, "index.html", output)
    return render(request, "index.html", {})