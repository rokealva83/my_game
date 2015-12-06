# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity, Warehouse, UserVariables
from my_game.models import HullPattern, ShieldPattern, GeneratorPattern, EnginePattern, \
    ArmorPattern, ModulePattern, WeaponPattern
from my_game.models import ProjectShip, ElementShip, TurnShipBuild
from my_game.designing_ships import verification_project


def new_ship(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        armors = {}
        shields = {}
        engines = {}
        generators = {}
        weapons = {}
        main_weapons = {}
        modules = {}
        hulls = {}
        output = {}
        warehouses = Warehouse.objects.filter(user=session_user, user_city=session_user_city).order_by('resource_id')
        user_citys = UserCity.objects.filter(user=session_user)

        if request.POST.get('create_pattern'):
            chosen_hull_id = request.POST.get('choice_pattern')
            chosen_name = request.POST.get('ship_name')
            chosen_hull = HullPattern.objects.filter(user=session_user, id=chosen_hull_id).first()
            armors = ArmorPattern.objects.filter(user=session_user).all()
            shields = ShieldPattern.objects.filter(user=session_user).all()
            engines = EnginePattern.objects.filter(user=session_user).all()
            generators = GeneratorPattern.objects.filter(user=session_user).all()
            weapons = WeaponPattern.objects.filter(user=session_user).all()
            main_weapons = WeaponPattern.objects.filter(user=session_user).all()
            modules = ModulePattern.objects.filter(user=session_user).all()
            turn_ship_builds = TurnShipBuild.objects.filter(user=session_user, user_city=session_user_city)
            output = {'user': session_user, 'warehouses': warehouses, 'user_city': session_user_city,
                      'user_citys': user_citys,
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
            chosen_hull = HullPattern.objects.filter(user=session_user, id=chosen_hull_id).first()
            hulls = HullPattern.objects.filter(user=session_user).all()

            verification = verification_project.verification(chosen_hull, myDict)
            if verification:
                project_ship = ProjectShip(
                    user=session_user,
                    name=chosen_name,
                    hull_pattern=chosen_hull
                )
                project_ship.save()
                user_variables = UserVariables.objects.get(id=1)
                time_build = user_variables.basic_time_build_ship
                mass = chosen_hull.hull_mass
                choice_armor = myDict.get('choice_armor')
                choice_armor_side = myDict.get('choice_armor_side')
                if choice_armor:
                    for i in range(chosen_hull.armor):
                        if choice_armor[i]:
                            armor = ArmorPattern.objects.filter(id=choice_armor[i]).first()
                            element = ElementShip(
                                project_ship=project_ship,
                                class_element=2,
                                element_pattern_id=choice_armor[i],
                                position=choice_armor_side[i],
                                element_health=armor.armor_health
                            )
                            element.save()
                            time_build = time_build * 1.1
                            mass = mass + armor.armor_mass

                choice_shield = myDict.get('choice_shield')
                choice_shield_side = myDict.get('choice_shield_side')
                if choice_shield:
                    for i in range(chosen_hull.shield):
                        if choice_shield[i]:
                            shield = ShieldPattern.objects.filter(id=choice_shield[i]).first()
                            element = ElementShip(
                                project_ship=project_ship,
                                class_element=3,
                                element_pattern_id=choice_shield[i],
                                position=choice_shield_side[i],
                                element_health=shield.shield_health
                            )
                            element.save()
                            time_build = time_build * 1.1
                            mass = mass + shield.shield_mass

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
                            engine = EnginePattern.objects.filter(id=choice_engine[i]).first()
                            element = ElementShip(
                                project_ship=project_ship,
                                class_element=4,
                                element_pattern_id=choice_engine[i],
                                position=2,
                                element_health=engine.engine_health
                            )
                            element.save()
                            system_power = system_power + engine.system_power
                            intersystem_power = intersystem_power + engine.intersystem_power
                            giper_power = giper_power + engine.giper_power
                            null_power = null_power + engine.nullT_power
                            system_fuel = system_fuel + engine.power_consuption
                            intersystem_fuel = intersystem_fuel + engine.power_consuption
                            giper_energy = giper_energy + engine.power_consuption
                            null_energy = null_energy + engine.power_consuption
                            time_build = time_build * 1.1
                            mass = mass + engine.engine_mass

                ProjectShip.objects.filter(id=project_ship.id).update(system_power=system_power,
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
                            generator = GeneratorPattern.objects.filter(id=choice_generator[i]).first()
                            element = ElementShip(
                                project_ship=project_ship,
                                class_element=5,
                                element_pattern_id=choice_generator[i],
                                position=0,
                                element_health=generator.generator_health
                            )
                            element.save()
                            time_build = time_build * 1.1
                            mass = mass + generator.generator_mass
                            generator_fuel = generator_fuel + generator.fuel_necessary
                            generator_energy = generator_energy + generator.produced_energy
                            ProjectShip.objects.filter(id=project_ship.id).update(generator_fuel=generator_fuel,
                                                                                  generator_energy=generator_energy)

                choice_weapon = myDict.get('choice_weapon')
                choice_weapon_side = myDict.get('choice_weapon_side')
                if choice_weapon:
                    for i in range(chosen_hull.main_weapon):
                        if int(choice_weapon[i]) != 0:
                            weapon = WeaponPattern.objects.filter(id=choice_weapon[i]).first()
                            element = ElementShip(
                                project_ship=project_ship,
                                class_element=6,
                                element_pattern_id=choice_weapon[i],
                                position=choice_weapon_side[i],
                                element_health=weapon.weapon_health
                            )
                            element.save()
                            time_build = time_build * 1.1
                            mass = mass + weapon.weapon_mass

                choice_main_weapon = myDict.get('choice_main_weapon')
                choice_main_weapon_side = myDict.get('choice_main_weapon_side')
                if choice_main_weapon:
                    for i in range(chosen_hull.main_weapon):
                        if int(choice_main_weapon[i]) != 0:
                            weapon = WeaponPattern.objects.filter(id=choice_weapon[i]).first()
                            element = ElementShip(
                                project_ship=project_ship,
                                class_element=7,
                                element_pattern_id=choice_main_weapon[i],
                                position=choice_main_weapon_side[i],
                                element_health=weapon.weapon_health
                            )
                            element.save()
                            time_build = time_build * 1.1
                            mass = mass + weapon.weapon_mass

                choice_module = myDict.get('choice_module')
                if choice_module:
                    for i in range(chosen_hull.module):
                        if int(choice_module[i]) != 0:
                            module = ModulePattern.objects.filter(id=choice_module[i]).first()
                            element = ElementShip(
                                project_ship=project_ship,
                                class_element=8,
                                element_pattern_id=choice_module[i],
                                position=0,
                                element_health=module.module_health
                            )
                            element.save()
                            time_build = time_build * 1.1
                            mass = mass + module.module_mass

                ProjectShip.objects.filter(id=project_ship.id).update(time_build=time_build, ship_mass=mass)
                turn_ship_builds = TurnShipBuild.objects.filter(user=session_user, user_city=session_user_city)
                project_ships = ProjectShip.objects.filter(user=session_user).order_by('id')
                output = {'user': session_user, 'warehouses': warehouses, 'user_city': session_user_city,
                          'user_citys': user_citys,
                          'hulls': hulls, 'project_ships': project_ships, 'turn_ship_builds': turn_ship_builds}
            else:
                message_error = 'Ошибка создания проекта'
                turn_ship_builds = TurnShipBuild.objects.filter(user=session_user, user_city=session_user_city)
                project_ships = ProjectShip.objects.filter(user=session_user).order_by('id')
                output = {'user': session_user, 'warehouses': warehouses, 'user_city': session_user_city,
                          'user_citys': user_citys, 'chosen_hull': chosen_hull, 'chosen_name': chosen_name,
                          'armors': armors, 'shields': shields, 'engines': engines, 'generators': generators,
                          'weapons': weapons, 'main_weapons': main_weapons, 'modules': modules, 'hulls': hulls,
                          'turn_ship_builds': turn_ship_builds, 'massage_error': message_error,
                          'project_ships': project_ships}
    request.session['user'] = session_user.id
    request.session['user_city'] = session_user_city.id
    request.session['live'] = True
    return render(request, "designingships.html", output)
