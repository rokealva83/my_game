# -*- coding: utf-8 -*-

from django.utils import timezone
from my_game.models import UserCity
from my_game.models import TurnProduction
from my_game.models import FactoryInstalled
from my_game.models import WarehouseElement


def verification_stage_production(request):
    user = request
    user_citys = UserCity.objects.filter(user=user)
    for user_city in user_citys:
        turn_productions = TurnProduction.objects.filter(user=user, user_city=user_city.id).order_by(
            'start_time_production')
        for turn_production in turn_productions:
            time = timezone.now()
            time_start = turn_production.start_time_production
            delta_time = time - time_start
            new_delta = delta_time.total_seconds()
            delta_time = turn_production.finish_time_production - turn_production.start_time_production
            delta = delta_time.total_seconds()
            if new_delta > delta:
                warehouse = WarehouseElement.objects.filter(user_city=user_city, element_id=turn_production.element_id,
                                                            element_class=turn_production.factory.production_class).first()
                if warehouse:
                    new_amount = warehouse.amount + turn_production.amount_element
                    WarehouseElement.objects.filter(id=warehouse.id).update(amount=new_amount)
                else:
                    warehouse = WarehouseElement(
                        user=user,
                        user_city=user_city,
                        element_class=turn_production.factory.production_class,
                        element_id=turn_production.element_id,
                        amount=turn_production.amount_element
                    )
                    warehouse.save()
                TurnProduction.objects.filter(id=turn_production.id).delete()
