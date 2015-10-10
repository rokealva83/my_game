# -*- coding: utf-8 -*-


from django.utils import timezone
from my_game.models import UserCity
from my_game.models import WarehouseElement
from my_game.models import ProjectShip, TurnShipBuild, Ship, ElementShip


def verification_turn_ship_build(request):
    user = request
    user_citys = UserCity.objects.filter(user=user)
    for user_city in user_citys:
        city_id = int(user_city.id)
        turn_ship_build = TurnShipBuild.objects.filter(user=user, user_city=user_city.id).first()
        if turn_ship_build:
            time = timezone.now()
            time_start = turn_ship_build.start_time_build
            delta_time = time - time_start
            new_delta = delta_time.seconds
            delta_time = turn_ship_build.finish_time_build - turn_ship_build.start_time_build
            delta = delta_time.seconds
            if new_delta > delta:
                if turn_ship_build.process_id == 1:
                    dock = Ship.objects.filter(id_project_ship=turn_ship_build.ship_pattern, fleet_status=0).first()
                    create_ship = ProjectShip.objects.filter(user=user, id=turn_ship_build.ship_pattern).first()
                    if dock is not None:
                        new_amount = dock.amount_ship + turn_ship_build.amount
                        dock = Ship.objects.filter(id_project_ship=turn_ship_build.ship_pattern, fleet_status=0).update(
                            amount_ship=new_amount)
                    else:
                        dock = Ship(
                            user=user,
                            id_project_ship=turn_ship_build.ship_pattern,
                            name=create_ship.name,
                            amount_ship=turn_ship_build.amount,
                            fleet_status=0,
                            place_id=city_id
                        )
                        dock.save()
                    turn_ship_build_delete = TurnShipBuild.objects.filter(id=turn_ship_build.id).delete()

                elif turn_ship_build.process_id == 2:
                    element_ships = ElementShip.objects.filter(id_project_ship=turn_ship_build.ship_pattern)
                    for element_ship in element_ships:
                        warehouse_element = WarehouseElement.objects.filter(element_class=element_ship.class_element,
                                                                             element_id=element_ship.id_element_pattern).first()
                        new_amount = warehouse_element.amount + (1 * turn_ship_build.amount)
                        warehouse_element = WarehouseElement.objects.filter(element_class=element_ship.class_element,
                                                                             element_id=element_ship.id_element_pattern).update(
                            amount=new_amount)

                elif turn_ship_build.process_id == 3:
                    element_ships = ElementShip.objects.filter(id_project_ship=turn_ship_build.ship_pattern)
                    for element_ship in element_ships:
                        if element_ship.class_element == 7:
                            class_element = 6
                        else:
                            class_element = element_ship.class_element
                        warehouse_element = WarehouseElement.objects.filter(element_class=class_element,
                                                                             element_id=element_ship.id_element_pattern).first()

                        new_amount = warehouse_element.amount + (1 * turn_ship_build.amount)
                        warehouse_element = WarehouseElement.objects.filter(element_class=class_element,
                                                                             element_id=element_ship.id_element_pattern).update(
                            amount=new_amount)
                    dock = Ship.objects.filter(id_project_ship=turn_ship_build.ship_pattern).first()
                    create_ship = ProjectShip.objects.filter(user=user, id=turn_ship_build.ship_pattern).first()
                    if dock is not None:
                        new_amount = dock.amount_ship + turn_ship_build.amount
                        dock = Ship.objects.filter(id_project_ship=turn_ship_build.ship_pattern).update(
                            amount_ship=new_amount)
                    else:
                        dock = Ship(
                            user=user,
                            id_project_ship=turn_ship_build.ship_pattern,
                            name=create_ship.name,
                            amount_ship=turn_ship_build.amount,
                            fleet_status=0,
                            place_id=city_id
                        )
                        dock.save()
                    turn_ship_build_delete = TurnShipBuild.objects.filter(id=turn_ship_build.id).delete()
