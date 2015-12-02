# -*- coding: utf-8 -*-

import random
from django.shortcuts import render
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from datetime import datetime
from my_game.models import Planet
from my_game.models import UserVariables
from my_game.models import MyUser, Race
from my_game.models import UserCity, Warehouse, UserScientic, BasicScientic, BasicFactory, FactoryPattern, \
    FactoryInstalled, WarehouseFactoryResource


def add_user(request):
    if request.method == "POST" and request.POST.get('add_button') is not None:
        new_user_name = request.POST.get('name')
        new_user_email = request.POST.get('mail')
        race = request.POST.get('rac')
        # проверка имени и емейла на уникальность
        user_name = MyUser.objects.filter(user_name=new_user_name).first()
        user_email = MyUser.objects.filter(e_mail=new_user_email).first()
        if user_name is not None or user_email is not None and race is not None:
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
            user_lucky = (random.randint(-15, 15))/100
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

            warehouse = Warehouse(
                user=myuser,
                res_nickel=user_variables.registr_nickel,
                res_iron=user_variables.registr_iron,
                res_cooper=user_variables.registr_cooper,
                res_aluminum=user_variables.registr_aluminum,
                res_variarit=user_variables.registr_veriarit,
                res_inneilit=user_variables.registr_inneilit,
                res_renniit=user_variables.registr_renniit,
                res_cobalt=user_variables.registr_cobalt,
                mat_construction_material=user_variables.registr_construction_material,
                mat_chemical=user_variables.registr_chemical,
                mat_high_strength_allov=user_variables.registr_high_strength_allov,
                mat_nanoelement=user_variables.registr_nanoelement,
                mat_microprocessor_element=user_variables.registr_microprocessor_element,
                mat_fober_optic_element=user_variables.registr_fober_optic_element,
            )
            warehouse.save()

            user_city = UserCity(
                user=myuser,
                system=planet.system,
                warehouse=warehouse,
                planet=planet,
                x=planet.global_x,
                y=planet.global_y,
                z=planet.global_z,
                city_size_free=planet.work_area_planet,
                founding_date=datetime.today(),
                extraction_date=datetime.today()
            )
            user_city.save()
            Planet.objects.filter(pk=user_city.planet.id).update(planet_free=0)

            basic_factorys = BasicFactory.objects.all()
            for basic_factory in basic_factorys:
                if basic_factory.production_class > 9:
                    factory_pattern = FactoryPattern(
                        user=myuser,
                        basic_factory=basic_factory,
                        factory_name=basic_factory.factory_name,
                        price_internal_currency=basic_factory.price_internal_currency,
                        price_construction_material=basic_factory.price_construction_material,
                        price_chemical=basic_factory.price_chemical,
                        price_high_strength_allov=basic_factory.price_high_strength_allov,
                        price_nanoelement=basic_factory.price_nanoelement,
                        price_microprocessor_element=basic_factory.price_microprocessor_element,
                        price_fober_optic_element=basic_factory.price_fober_optic_element,
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
                    warehouse_factory = WarehouseFactoryResource()
                    warehouse_factory.save()
                    factory_instelled = FactoryInstalled(
                        user=myuser,
                        user_city=user_city,
                        factory_pattern=factory_pattern,
                        factory_warehouse=warehouse_factory,
                        production_class=factory_pattern.production_class,
                        production_id=factory_pattern.production_id,
                    )
                    factory_instelled.save()
            factory_instelleds = FactoryInstalled.objects.filter(user=myuser)
            use_energy = 0
            use_area = 0
            for factory_instelled in factory_instelleds:
                use_area = factory_instelled.factory_pattern.factory_size + use_area
                if factory_instelled.factory_pattern.production_class == 12:
                    UserCity.objects.filter(user=myuser).update(
                        power=factory_instelled.factory_pattern.power_consumption)
                else:
                    use_energy = use_energy + factory_instelled.factory_pattern.power_consumption
            free_area = user_city.city_size_free - use_area
            UserCity.objects.filter(user=myuser).update(use_energy=use_energy, city_size_free=free_area)

    elif request.POST.get('cancel_button') is not None:
        return render(request, "index.html", {})
    return render(request, "index.html", {})
