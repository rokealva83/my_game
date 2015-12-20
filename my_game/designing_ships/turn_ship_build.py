# -*- coding: utf-8 -*-


from django.utils import timezone
from my_game.models import UserCity
from my_game.models import WarehouseElement
from my_game.models import ProjectShip, TurnShipBuild, Ship, ElementShip


def verification_turn_ship_build(request):
    user = request
    user_citys = UserCity.objects.filter(user=user).all()
    for user_city in user_citys:
        turn_ship_build = TurnShipBuild.objects.filter(user=user, user_city=user_city).first()
        if turn_ship_build:
            time = timezone.now()
            time_start = turn_ship_build.start_time_build
            delta_time = time - time_start
            new_delta = delta_time.total_seconds()
            delta_time = turn_ship_build.finish_time_build - turn_ship_build.start_time_build
            delta = delta_time.total_seconds()
            if new_delta > delta:
                if turn_ship_build.process_id == 1:
                    dock = Ship.objects.filter(project_ship=turn_ship_build.project_ship, fleet_status=0).first()
                    create_ship = turn_ship_build.project_ship
                    if dock is not None:
                        new_amount = dock.amount_ship + turn_ship_build.amount
                        Ship.objects.filter(project_ship=turn_ship_build.project_ship, fleet_status=0).update(
                            amount_ship=new_amount)
                    else:
                        dock = Ship(
                            user=user,
                            project_ship=create_ship,
                            ship_name=create_ship.project_name,
                            amount_ship=turn_ship_build.amount,
                            fleet_status=0,
                            place_id=user_city.id
                        )
                        dock.save()
                    TurnShipBuild.objects.filter(id=turn_ship_build.id).delete()

                elif turn_ship_build.process_id == 2:
                    element_ships = ElementShip.objects.filter(project_ship=turn_ship_build.project_ship)
                    for element_ship in element_ships:
                        warehouse_element = WarehouseElement.objects.filter(element_class=element_ship.class_element,
                                                                            element_id=element_ship.element_pattern_id).first()
                        new_amount = warehouse_element.amount + (1 * turn_ship_build.amount)
                        WarehouseElement.objects.filter(element_class=element_ship.class_element,
                                                        element_id=element_ship.element_pattern_id).update(
                            amount=new_amount)

                elif turn_ship_build.process_id == 3:
                    element_ships = ElementShip.objects.filter(project_ship=turn_ship_build.project_ship)
                    for element_ship in element_ships:
                        if element_ship.class_element == 7:
                            class_element = 6
                        else:
                            class_element = element_ship.class_element
                        warehouse_element = WarehouseElement.objects.filter(element_class=class_element,
                                                                            element_id=element_ship.element_pattern_id).first()

                        new_amount = warehouse_element.amount + (1 * turn_ship_build.amount)
                        WarehouseElement.objects.filter(element_class=class_element,
                                                        element_id=element_ship.element_pattern_id).update(
                            amount=new_amount)
                    dock = Ship.objects.filter(project_ship=turn_ship_build.project_ship).first()
                    create_ship = ProjectShip.objects.filter(user=user, id=turn_ship_build.project_ship).first()
                    if dock is not None:
                        new_amount = dock.amount_ship + turn_ship_build.amount
                        Ship.objects.filter(project_ship=turn_ship_build.project_ship).update(amount_ship=new_amount)
                    else:
                        dock = Ship(
                            user=user,
                            project_ship=turn_ship_build.project_ship,
                            ship_name=create_ship.project_name,
                            amount_ship=turn_ship_build.amount,
                            fleet_status=0,
                            place_id=user_city.id
                        )
                        dock.save()
                    TurnShipBuild.objects.filter(id=turn_ship_build.id).delete()
