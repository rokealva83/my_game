# -*- coding: utf-8 -*-

from django.utils import timezone
from my_game.models import TurnAssemblyPieces
from my_game.models import FactoryPattern, BuildingPattern
from my_game.models import WarehouseFactory, WarehouseBuilding


def check_assembly_line_workpieces(request):
    user = request
    turn_assembly_piecess = TurnAssemblyPieces.objects.filter(user=user)
    time = timezone.now()
    #перебор елементов очереди
    for turn_assembly_pieces in turn_assembly_piecess:
        time_start = turn_assembly_pieces.start_time_assembly
        delta_time = time - time_start
        new_delta = delta_time.seconds
        delta_time = turn_assembly_pieces.finish_time_assembly - turn_assembly_pieces.start_time_assembly
        delta = delta_time.seconds
        if turn_assembly_pieces.class_id != 13:
            warehouse_factory = WarehouseFactory.objects.filter(factory=turn_assembly_pieces.pattern).first()
        else:
            warehouse_factory = WarehouseBuilding.objects.filter(factory=turn_assembly_pieces.pattern).first()
        #проверка времени
        if new_delta > delta:
            if warehouse_factory is not None:
                amount_assembly = turn_assembly_pieces.amount_assembly + warehouse_factory.amount
                if turn_assembly_pieces.class_id != 13:
                    WarehouseFactory.objects.filter(id=warehouse_factory.id).first().update(amount=amount_assembly)
                else:
                    WarehouseBuilding.objects.filter(id=warehouse_factory.id).first().update(amount=amount_assembly)
            else:
                if turn_assembly_pieces.class_id != 13:
                    new_factory = WarehouseFactory(
                        user=turn_assembly_pieces.user,
                        user_city=turn_assembly_pieces.user_city,
                        factory=turn_assembly_pieces.pattern,
                        amount=turn_assembly_pieces.amount_assembly
                    )
                    new_factory.save()
                else:
                    new_building = WarehouseBuilding(
                        user=turn_assembly_pieces.user,
                        user_city=turn_assembly_pieces.user_city,
                        factory=turn_assembly_pieces.pattern,
                        amount=turn_assembly_pieces.amount_assembly
                )
                    new_building.save()
            end_turn_assembly_pieces = TurnAssemblyPieces.objects.filter(id=turn_assembly_pieces.id).delete()
