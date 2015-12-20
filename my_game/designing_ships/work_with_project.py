# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from django.shortcuts import render
from my_game.models import MyUser, UserCity
from my_game.models import WarehouseElement
from my_game import function
from my_game.models import ProjectShip, ElementShip, TurnShipBuild
from my_game.models import HullPattern
from my_game.space_forces.view_ship_project import view_ship_project


def work_with_project(request):
    if "live" not in request.session:
        return render(request, "index.html", {})
    else:
        session_user = MyUser.objects.filter(id=int(request.session['user'])).first()
        session_user_city = UserCity.objects.filter(id=int(request.session['user_city'])).first()
        function.check_all_queues(session_user)
        message = ''
        if request.POST.get('create_ship'):
            ship_id = int(request.POST.get('hidden_ship'))
            amount_ship = int(request.POST.get('amount'))
            len_turn_create_ship = len(TurnShipBuild.objects.filter(user=session_user, user_city=session_user_city))
            if len_turn_create_ship < 5:
                ship_pattern = ProjectShip.objects.filter(id=ship_id).first()
                warehouse_hull = WarehouseElement.objects.filter(user=session_user, user_city=session_user_city,
                                                                 element_class=1,
                                                                 element_id=ship_pattern.hull_pattern.id).first()
                if warehouse_hull is not None and warehouse_hull.amount >= amount_ship:
                    error = 0
                    for i in range(2, 9):
                        element_ships = ElementShip.objects.filter(project_ship=ship_pattern, class_element=i).order_by(
                            'element_pattern_id')
                        work_element_id = 0
                        if element_ships:
                            for element_ship in element_ships:
                                element_id = element_ship.element_pattern_id
                                if element_id != work_element_id:
                                    number_element = len(
                                        ElementShip.objects.filter(project_ship=ship_pattern, class_element=i,
                                                                   element_pattern_id=element_id))
                                    j = i
                                    if i == 7:
                                        j = 6
                                    warehouse_element = WarehouseElement.objects.filter(user=session_user,
                                                                                        user_city=session_user_city,
                                                                                        element_class=j,
                                                                                        element_id=element_id).first()
                                    if warehouse_element <= number_element * amount_ship:
                                        error += 1
                                    work_element_id = element_id
                    if error == 0:
                        last_ship_build = TurnShipBuild.objects.filter(user=session_user,
                                                                       user_city=session_user_city).last()
                        if last_ship_build is not None:
                            start_time = last_ship_build.finish_time_build
                        else:
                            start_time = datetime.now()
                        finish_time = start_time + timedelta(seconds=(ship_pattern.time_build * amount_ship))
                        turn_create_ship = TurnShipBuild(
                            user=session_user,
                            user_city=session_user_city,
                            project_ship=ship_pattern,
                            amount=amount_ship,
                            start_time_build=start_time,
                            finish_time_build=finish_time,
                            process_id=1
                        )
                        turn_create_ship.save()
                        warehouse_hull = WarehouseElement.objects.filter(user=session_user, user_city=session_user_city,
                                                                         element_class=1,
                                                                         element_id=ship_pattern.hull_pattern.id).first()
                        new_amount = warehouse_hull.amount - amount_ship
                        WarehouseElement.objects.filter(user=session_user, user_city=session_user_city, element_class=1,
                                                        element_id=ship_pattern.hull_pattern).update(amount=new_amount)

                        element_ships = ElementShip.objects.filter(project_ship=ship_pattern).order_by('class_element')
                        for element_ship in element_ships:
                            if element_ship.class_element != 7:
                                class_element = element_ship.class_element
                            else:
                                class_element = 6
                            element_id = element_ship.element_pattern_id
                            warehouse_element = WarehouseElement.objects.filter(user=session_user,
                                                                                user_city=session_user_city,
                                                                                element_class=class_element,
                                                                                element_id=element_id).first()
                            new_amount = warehouse_element.amount - amount_ship
                            WarehouseElement.objects.filter(user=session_user,
                                                            user_city=session_user_city,
                                                            element_class=class_element,
                                                            element_id=element_id).update(
                                amount=new_amount)
                        message = 'Сборка корабля начата'
                    else:
                        message = 'На складе не хватает комплектующих'
                else:
                    message = 'На складе не хватает комплектующих'
            else:
                message = 'Очередь занята'

        if request.POST.get('delete_pattern'):
            ship_id = request.POST.get('hidden_ship')
            ProjectShip.objects.filter(id=ship_id).delete()
            ElementShip.objects.filter(project_ship=ship_id).all().delete()
            message = 'Проект удален'

        if request.POST.get('view_ship_project'):
            output = view_ship_project(request)
            return render(request, "designingships.html", output)

        user_citys = UserCity.objects.filter(user=session_user)
        hulls = HullPattern.objects.filter(user=session_user).order_by('basic_pattern')
        project_ships = ProjectShip.objects.filter(user=session_user).order_by('id')
        turn_ship_builds = TurnShipBuild.objects.filter(user=session_user, user_city=session_user_city)
        request.session['user'] = session_user.id
        request.session['user_city'] = session_user_city.id
        request.session['live'] = True
        output = {'user': session_user, 'warehouse': session_user_city.warehouse, 'user_city': session_user_city,
                  'user_citys': user_citys, 'hulls': hulls, 'project_ships': project_ships,
                  'turn_ship_builds': turn_ship_builds, 'message': message}
        return render(request, "designingships.html", output)
