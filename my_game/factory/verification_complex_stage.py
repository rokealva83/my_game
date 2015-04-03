
# -*- coding: utf-8 -*-

from django.utils import timezone
from my_game.models import User_city
from my_game.models import Turn_complex_production
from my_game.models import Factory_installed
from my_game.models import Warehouse_element


def verification_stage_production(request):
    user = request
    user_citys = User_city.objects.filter(user=user)
    for user_city in user_citys:
        city_id = user_city.id
        turn_productions = Turn_production.objects.filter(user=user, user_city=user_city.id).order_by(
            'start_time_production')
        for turn_production in turn_productions:
            time = timezone.now()
            time_start = turn_production.start_time_production
            delta_time = time - time_start
            new_delta = delta_time.seconds
            delta_time = turn_production.finish_time_production - turn_production.start_time_production
            delta = delta_time.seconds
            if new_delta > delta:
                work_factory = Factory_installed.objects.filter(id=turn_production.factory_id).first()
                warehouse = Warehouse_element.objects.filter(element_id=turn_production.element_id,
                                                             element_class=work_factory.production_class).first()
                if warehouse is not None:
                    new_amount = warehouse.amount + turn_production.amount_element
                    warehouse = Warehouse_element.objects.filter(element_id=turn_production.element_id).update(
                        amount=new_amount)
                else:
                    warehouse = Warehouse_element(
                        user=user,
                        user_city=user_city.id,
                        element_class=work_factory.production_class,
                        element_id=turn_production.element_id,
                        amount=turn_production.amount_element
                    )
                    warehouse.save()
                turn_production_delete = Turn_production.objects.filter(id=turn_production.id).delete()