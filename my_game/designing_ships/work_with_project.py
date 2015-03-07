# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from django.shortcuts import render
from my_game.models import MyUser, User_city, Warehouse
from my_game.models import Hull_pattern
from my_game.models import Warehouse_element
from my_game import function
from my_game.models import Project_ship, Element_ship, Turn_ship_build
from my_game.models import Hull_pattern, Shield_pattern, Generator_pattern, Engine_pattern, \
    Armor_pattern, Module_pattern, Weapon_pattern


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
                            finish_time_build=finish_time,
                            process_id = 1

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

        hulls = {}

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
                  'hulls': hulls, 'project_ships': project_ships, 'turn_ship_builds': turn_ship_builds,
                  'message': message}
        return render(request, "designingships.html", output)
