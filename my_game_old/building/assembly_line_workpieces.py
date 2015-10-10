# -*- coding: utf-8 -*-

from django.utils import timezone
from my_game.models import MyUser, UserCity
from my_game.models import TurnAssemblyPieces
from my_game.models import FactoryPattern, BuildingPattern
from my_game.models import WarehouseFactory


def check_assembly_line_workpieces(request):
    user = int(request)
    my_user = MyUser.objects.filter(user_id=user).first()
    turn_assembly_piecess = TurnAssemblyPieces.objects.filter(user=user)
    time = timezone.now()
    #перебор елементов очереди
    for turn_assembly_pieces in turn_assembly_piecess:
        time_start = turn_assembly_pieces.start_time_assembly
        delta_time = time - time_start
        new_delta = delta_time.seconds
        delta_time = turn_assembly_pieces.finish_time_assembly - turn_assembly_pieces.start_time_assembly
        delta = delta_time.seconds
        user_city = UserCity.objects.filter(user=user, id=turn_assembly_pieces.user_city).first()
        warehouse_factory = WarehouseFactory.objects.filter(factory_id=turn_assembly_pieces.pattern_id,
                                                             production_class=turn_assembly_pieces.class_id).first()
        #проверка времени
        if new_delta > delta:
            if warehouse_factory is not None:
                amount_assembly = turn_assembly_pieces.amount_assembly + warehouse_factory.amount
                warehouse_factory = WarehouseFactory.objects.filter(factory_id=turn_assembly_pieces.pattern_id,
                                                                     production_class=turn_assembly_pieces.class_id).update(
                    amount=amount_assembly)
            else:
                if turn_assembly_pieces.class_id != 13:
                    factory_pattern = FactoryPattern.objects.filter(id=turn_assembly_pieces.pattern_id,
                                                                     production_class=turn_assembly_pieces.class_id).first()
                else:
                    factory_pattern = BuildingPattern.objects.filter(id=turn_assembly_pieces.pattern_id,
                                                                      production_class=turn_assembly_pieces.class_id).first()
                new_factory = WarehouseFactory(
                    user=turn_assembly_pieces.user,
                    user_city=turn_assembly_pieces.user_city,
                    factory_id=turn_assembly_pieces.pattern_id,
                    production_class=factory_pattern.production_class,
                    production_id=factory_pattern.production_id,
                    time_production=factory_pattern.time_production,
                    amount=turn_assembly_pieces.amount_assembly,
                    size=factory_pattern.size,
                    mass=factory_pattern.mass,
                    power_consumption=factory_pattern.power_consumption
                )
                new_factory.save()
            end_turn_assembly_pieces = TurnAssemblyPieces.objects.filter(id=turn_assembly_pieces.id).delete()
