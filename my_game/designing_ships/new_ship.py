# -*- coding: utf-8 -*-


from django.shortcuts import render
from my_game.models import MyUser, User_city, Warehouse, User_variables
from my_game.models import Hull_pattern, Shield_pattern, Generator_pattern, Engine_pattern, \
    Armor_pattern, Module_pattern, Weapon_pattern

from my_game import function
from my_game.models import Project_ship, Element_ship, Turn_ship_build
from my_game.designing_ships import verification_project


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
        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('id_resource')
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
            output = {'user': user, 'warehouses': warehouses, 'user_city': user_city, 'user_citys': user_citys,
                      'chosen_hull': chosen_hull, 'chosen_name': chosen_name, 'armors': armors,
                      'shields': shields, 'engines': engines, 'generators': generators, 'weapons': weapons,
                      'main_weapons': main_weapons, 'modules': modules, 'hulls': hulls,
                      'turn_ship_builds': turn_ship_builds}
            return render(request, "design_new_ship.html", output)

        if request.POST.get('create_ship_pattern'):
            chosen_hull_id = int(request.POST.get('chosen_hull'))
            chosen_name = request.POST.get('chosen_hull_name')
            # verification element

            full_request = request.POST
            myDict = dict(full_request.iterlists())
            chosen_hull = Hull_pattern.objects.filter(user=session_user, id=chosen_hull_id).first()
            hulls = Hull_pattern.objects.filter(user=session_user).order_by('basic_id', 'id')

            verification = verification_project.verification(session_user, session_user_city, chosen_hull,
                                                             chosen_hull_id, myDict)
            if verification == True:

                new_pattern_ship = Project_ship(
                    user=session_user,
                    name=chosen_name,
                    hull_id=chosen_hull_id
                )
                new_pattern_ship.save()
                pattern_ship_id = new_pattern_ship.pk
                user_variables = User_variables.objects.filter(id=1).first()
                time_build = user_variables.basic_time_build_ship
                hull = Hull_pattern.objects.filter(user=session_user, id=chosen_hull_id).first()
                mass = hull.mass
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
                system_fuel = 0
                intersystem_fuel = 0
                giper_energy = 0
                null_energy = 0
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
                            system_fuel = system_fuel + engine.power_consuption
                            intersystem_power = intersystem_fuel + engine.power_consuption
                            giper_energy = giper_energy + engine.power_consuption
                            null_energy = null_energy + engine.power_consuption
                            time_build = time_build * 1.1
                            mass = mass + engine.mass

                ship_pattern = Project_ship.objects.filter(id=pattern_ship_id).update(system_power=system_power,
                                                                                      intersystem_power=intersystem_power,
                                                                                      giper_power=giper_power,
                                                                                      null_power=null_power,
                                                                                      system_fuel=system_fuel,
                                                                                      intersystem_fuel=intersystem_fuel,
                                                                                      giper_energy=giper_energy,
                                                                                      null_energy=null_energy)

                generator_fuel = 0
                generator_energy = 0
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
                            generator_fuel = generator_fuel + generator.fuel_necessary
                            generator_energy = generator_energy + generator.produced_energy
                            ship_pattern = Project_ship.objects.filter(id=pattern_ship_id).update(
                                generator_fuel=generator_fuel, generator_energy=generator_energy)

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
                                class_element=7,
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

                ship_pattern = Project_ship.objects.filter(id=pattern_ship_id).update(time_build=time_build, mass=mass)
                turn_ship_builds = Turn_ship_build.objects.filter(user=session_user, user_city=session_user_city)
                project_ships = Project_ship.objects.filter(user=session_user).order_by('id')
                output = {'user': user, 'warehouses': warehouses, 'user_city': user_city, 'user_citys': user_citys,
                          'hulls': hulls, 'project_ships': project_ships, 'turn_ship_builds': turn_ship_builds}
            else:
                message_error = 'Ошибка создания проекта'
                turn_ship_builds = Turn_ship_build.objects.filter(user=session_user, user_city=session_user_city)
                project_ships = Project_ship.objects.filter(user=session_user).order_by('id')
                output = {'user': user, 'warehouses': warehouses, 'user_city': user_city, 'user_citys': user_citys,
                          'chosen_hull': chosen_hull, 'chosen_name': chosen_name, 'armors': armors,
                          'shields': shields, 'engines': engines, 'generators': generators, 'weapons': weapons,
                          'main_weapons': main_weapons, 'modules': modules, 'hulls': hulls,
                          'turn_ship_builds': turn_ship_builds, 'massage_error': message_error}
    request.session['userid'] = session_user
    request.session['user_city'] = session_user_city
    request.session['live'] = True
    return render(request, "designingships.html", output)