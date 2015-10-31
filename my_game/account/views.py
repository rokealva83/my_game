# -*- coding: utf-8 -*-

import random
from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from datetime import datetime
from my_game.models import Planet
from my_game.models import UserVariables
from my_game.models import MyUser, Race
from my_game.models import UserCity, Warehouse, UserScientic, BasicScientic, BasicFactory, FactoryPattern, FactoryInstalled

from my_game import function


def registration(request):
    races = Race.objects.all()
    return render(request, "registration.html", {'races': races})


# функция добавления нового игрока
def add_user(request):
    if request.method == "POST" and request.POST.get('add_button') is not None:
        new_user_name = request.POST.get('name')
        new_user_email = request.POST.get('mail')
        # проверка имени и емейла на уникальность
        user_name = MyUser.objects.filter(user_name=new_user_name).first()
        user_email = MyUser.objects.filter(e_mail=new_user_email).first()
        if user_name is not None or user_email is not None:
            return HttpResponse()
        else:
            user_variables = UserVariables.objects.filter(id=1).first()
            user = User(
                username=new_user_name,
                password=request.POST.get('pass'),
                last_login=datetime.today(),
                date_joined=datetime.today(),
                email=new_user_email,
            )
            user.save()
            user_id = user.pk
            user_lucky = random.randint(1, 10)
            time_check = user.last_login
            last_time_check = datetime(time_check.year, time_check.month, time_check.day, 0, 0, 0, 0)
            race = Race.objects.filter(id=request.POST.get('rac')).first()

            myuser = MyUser(
                user_id=user_id,
                user_name=new_user_name,
                password=request.POST.get('pass'),
                race=race,
                internal_currency=user_variables.registr_internal_currency,
                e_mail=new_user_email,
                referal_code=new_user_name,
                user_luckyness=user_lucky,
                last_time_check=last_time_check,
                last_time_scan_scient=last_time_check,
            )
            myuser.save()

            # добавление пользователю науки
            scientic = UserScientic(
                user=myuser,
                time_study_math=BasicScientic.objects.get(scientic_id=1).time_study,
                time_study_phis=BasicScientic.objects.get(scientic_id=2).time_study,
                time_study_biol=BasicScientic.objects.get(scientic_id=3).time_study,
                time_study_ener=BasicScientic.objects.get(scientic_id=2).time_study,
                time_study_radio=BasicScientic.objects.get(scientic_id=4).time_study,
                time_study_nano=BasicScientic.objects.get(scientic_id=3).time_study,
                time_study_astr=BasicScientic.objects.get(scientic_id=1).time_study,
                time_study_logis=BasicScientic.objects.get(scientic_id=4).time_study,
            )
            scientic.save()
            planet = Planet.objects.filter(planet_type=int(request.POST.get('rac')), planet_free=1).first()
            # установка начального города и добавление склада. Добавление начальных строений
            user_city = UserCity(
                user=myuser,
                system=planet.system,
                planet=planet,
                x=planet.global_x,
                y=planet.global_y,
                z=planet.global_z,
                city_size_free=planet.work_area_planet,
                founding_date=datetime.today(),
                extraction_date=datetime.today()
            )
            user_city.save()
            planet = Planet.objects.filter(pk=user_city.planet.id).update(planet_free=0)

            warehouse = Warehouse(
                user=myuser,
                user_city=user_city,
                resource_id=1,
                amount=user_variables.registr_resource1
            )
            warehouse.save()
            warehouse = Warehouse(
                user=myuser,
                user_city=user_city,
                resource_id=2,
                amount=user_variables.registr_resource2
            )
            warehouse.save()
            warehouse = Warehouse(
                user=myuser,
                user_city=user_city,
                resource_id=3,
                amount=user_variables.registr_resource3
            )
            warehouse.save()
            warehouse = Warehouse(
                user=myuser,
                user_city=user_city,
                resource_id=4,
                amount=user_variables.registr_resource4
            )
            warehouse.save()
            warehouse = Warehouse(
                user=myuser,
                user_city=user_city,
                resource_id=5,
                amount=user_variables.registr_mineral1
            )
            warehouse.save()
            warehouse = Warehouse(
                user=myuser,
                user_city=user_city,
                resource_id=6,
                amount=user_variables.registr_mineral2
            )
            warehouse.save()
            warehouse = Warehouse(
                user=myuser,
                user_city=user_city,
                resource_id=7,
                amount=user_variables.registr_mineral3
            )
            warehouse.save()
            warehouse = Warehouse(
                user=myuser,
                user_city=user_city,
                resource_id=8,
                amount=user_variables.registr_mineral4
            )
            warehouse.save()

            basic_factorys = BasicFactory.objects.all()
            for basic_factory in basic_factorys:
                if basic_factory.production_class > 9:
                    factory_pattern = FactoryPattern(
                        user=myuser,
                        basic_factory=basic_factory,
                        factory_name=basic_factory.factory_name,
                        price_internal_currency=basic_factory.price_internal_currency,
                        price_resource1=basic_factory.price_resource1,
                        price_resource2=basic_factory.price_resource2,
                        price_resource3=basic_factory.price_resource3,
                        price_resource4=basic_factory.price_resource4,
                        cost_expert_deployment=basic_factory.price_expert_deployment,
                        assembly_workpiece=basic_factory.assembly_workpiece,
                        time_deployment=basic_factory.time_deployment,
                        production_class=basic_factory.production_class,
                        production_id=basic_factory.production_id,
                        time_production=basic_factory.time_production,
                        factory_size=basic_factory.factory_size,
                        factory_mass=basic_factory.factory_mass,
                        power_consumption=basic_factory.power_consumption
                    )
                    factory_pattern.save()
            factory_patterns = FactoryPattern.objects.filter(user=myuser)
            for factory_pattern in factory_patterns:
                if factory_pattern.production_id == 1 or factory_pattern.production_id == 2:
                    factory_instelled = FactoryInstalled(
                        user=myuser,
                        user_city=user_city,
                        factory_pattern=factory_pattern,
                    )
                    factory_instelled.save()
            factory_instelleds = FactoryInstalled.objects.filter(user=myuser)
            use_energy = 0
            use_area = 0
            for factory_instelled in factory_instelleds:
                use_area = factory_instelled.factory_pattern.factory_size + use_area
                if factory_instelled.factory_pattern.production_class == 12:
                    user_city_update = UserCity.objects.filter(user=myuser).update(power=factory_instelled.factory_pattern.power_consumption)
                else:
                    use_energy = use_energy + factory_instelled.factory_pattern.power_consumption
            free_area = user_city.city_size_free - use_area
            user_city_update = UserCity.objects.filter(user=myuser).update(use_energy=use_energy, city_size_free=free_area)

    elif request.POST.get('cancel_button') is not None:
        return render(request, "index.html", {})
    return render(request, "index.html", {})


# функция авторизации
def user_auth(request):
    if request.method == "POST" and request.POST.get('add_button') is not None:
        user_name_post = request.POST.get('name')
        password_post = request.POST.get('pass')
        user_name_auth = User.objects.filter(username=user_name_post).first()
        if user_name_auth is not None:
            if user_name_auth.password == password_post:
                user = MyUser.objects.filter(user_id=user_name_auth.id).first()
                user_city = UserCity.objects.filter(user=user).first()
                warehouses = Warehouse.objects.filter(user=user, user_city=user_city).order_by('resource_id')
                user_citys = UserCity.objects.filter(user=user)
                planet = user_city.planet
                race = user.race
                # function.check_all_queues(user)
                output = {'user': user, 'race': race, 'warehouses': warehouses, 'user_city': user_city,
                          'user_citys': user_citys, 'planet': planet}
                request.session['user'] = user.id
                request.session['user_city'] = user_city.id
                request.session['live'] = True
                return render(request, "civilization.html", output)
            else:
                message = 'Неверно введено имя или пароль пользователя'
                output = {'message': message}
                return render(request, "index.html", output)
    return render(request, "index.html", {})
