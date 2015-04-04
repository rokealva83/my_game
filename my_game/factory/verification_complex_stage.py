# -*- coding: utf-8 -*-

from django.utils import timezone
from datetime import datetime, timedelta
from my_game.models import Turn_complex_production, Manufacturing_complex
from my_game.models import Factory_installed
from my_game.models import Warehouse_element
from my_game.factory import factory_function


def verification_complex_stage(request):
    user = request
    manufacturing_complexs = Manufacturing_complex.objects.filter(user=user)
    for manufacturing_complex in manufacturing_complexs:
        check = 0
        while check == 0:
            check = 1
            complex_id = manufacturing_complex.id
            turn_productions = Turn_complex_production.objects.filter(complex_id=complex_id)
            for turn_production in turn_productions:
                time = timezone.now()
                time_start = turn_production.start_time_production
                delta_time = time - time_start
                new_delta = delta_time.seconds
                delta = turn_production.time
                if new_delta > delta:

                    work_factory = Factory_installed.objects.filter(id=turn_production.factory_id).first()
                    warehouse = Warehouse_element.objects.filter(user_city=manufacturing_complex.user_city,
                                                                 element_id=turn_production.element_id,
                                                                 element_class=work_factory.production_class).first()
                    if warehouse is not None:
                        new_amount = warehouse.amount + 1
                        warehouse = Warehouse_element.objects.filter(id=warehouse.id).update(amount=new_amount)
                    else:
                        warehouse = Warehouse_element(
                            user=user,
                            user_city=manufacturing_complex.user_city,
                            element_class=work_factory.production_class,
                            element_id=turn_production.element_id,
                            amount=1
                        )
                        warehouse.save()
                    complex_id = turn_production.complex_id
                    factory_id = turn_production.factory_id
                    element_id = turn_production.element_id
                    time_start = turn_production.start_time_production + timedelta(seconds=turn_production.time)
                    turn_production_delete = Turn_complex_production.objects.filter(id=turn_production.id).delete()
                    message = factory_function.complex_production_module(complex_id, factory_id, element_id, time_start)
                    if message == 1 and check == 1:
                        check = 1
                    elif message == 0:
                        check = 0





