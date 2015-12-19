# -*- coding: utf-8 -*-

from django.utils import timezone
from datetime import timedelta
from my_game.models import TurnComplexProduction, ManufacturingComplex
from my_game.models import WarehouseElement

from my_game.factory import complex_production_module


def verification_complex_stage(request):
    user = request
    manufacturing_complexs = ManufacturingComplex.objects.filter(user=user)
    for manufacturing_complex in manufacturing_complexs:
        check = 0
        while check == 0:
            check = 1
            turn_productions = TurnComplexProduction.objects.filter(manufacturing_complex=manufacturing_complex)
            for turn_production in turn_productions:
                time = timezone.now()
                time_start = turn_production.start_time_production
                delta_time = time - time_start
                new_delta = delta_time.total_seconds()
                delta = turn_production.time
                if new_delta > delta:

                    warehouse = WarehouseElement.objects.filter(user_city=manufacturing_complex.user_city,
                                                                element_id=turn_production.element_id,
                                                                element_class=turn_production.factory.production_class).first()
                    if warehouse is not None:
                        new_amount = warehouse.amount + 1
                        WarehouseElement.objects.filter(id=warehouse.id).update(amount=new_amount)
                    else:
                        warehouse = WarehouseElement(
                            user=user,
                            user_city=manufacturing_complex.user_city,
                            element_class=turn_production.factory.production_class,
                            element_id=turn_production.element_id,
                            amount=1
                        )
                        warehouse.save()
                    element_id = turn_production.element_id
                    time_start = turn_production.start_time_production + timedelta(seconds=turn_production.time)
                    TurnComplexProduction.objects.filter(id=turn_production.id).delete()
                    message = complex_production_module.complex_production_module(manufacturing_complex,
                                                                                  turn_production.factory, element_id,
                                                                                  time_start)
                    if message == 1 and check == 1:
                        check = 1
                    elif message == 0:
                        check = 0
