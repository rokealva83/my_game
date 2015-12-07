# -*- coding: utf-8 -*-

from django.utils import timezone
from my_game.models import TurnAssemblyPiecesFactory, TurnAssemblyPiecesBuilding
from my_game.models import WarehouseFactory, WarehouseBuilding


def check_assembly_line_workpieces(request):
    user = request
    factory_turn_assembly_pieceses = TurnAssemblyPiecesFactory.objects.filter(user=user).all()
    building_turn_assembly_pieceses = TurnAssemblyPiecesBuilding.objects.filter(user=user).all()
    turn_assemblys = [factory_turn_assembly_pieceses, building_turn_assembly_pieceses]
    time = timezone.now()
    # перебор елементов очереди
    for turn_assembly_pieceses in turn_assemblys:
        for turn_assembly_pieces in turn_assembly_pieceses:
            time_start = turn_assembly_pieces.start_time_assembly
            if time > time_start:
                delta_time = time - time_start
                new_delta = delta_time.total_seconds()
                delta_time = turn_assembly_pieces.finish_time_assembly - turn_assembly_pieces.start_time_assembly
                delta = delta_time.total_seconds()
                if turn_assembly_pieces.class_id != 21:
                    warehouse_factory = WarehouseFactory.objects.filter(factory=turn_assembly_pieces.pattern).first()
                else:
                    warehouse_factory = WarehouseBuilding.objects.filter(building=turn_assembly_pieces.pattern).first()
                # проверка времени
                if new_delta > delta:
                    if warehouse_factory is not None:
                        amount_assembly = turn_assembly_pieces.amount_assembly + warehouse_factory.amount
                        setattr(warehouse_factory, 'amount', amount_assembly)
                        warehouse_factory.save()
                    else:
                        if turn_assembly_pieces.class_id != 21:
                            new_factory = WarehouseFactory(
                                user=turn_assembly_pieces.user,
                                user_city=turn_assembly_pieces.user_city,
                                factory=turn_assembly_pieces.pattern,
                                amount=turn_assembly_pieces.amount_assembly
                            )
                            new_factory.save()
                            TurnAssemblyPiecesFactory.objects.filter(id=turn_assembly_pieces.id).delete()
                        else:
                            new_building = WarehouseBuilding(
                                user=turn_assembly_pieces.user,
                                user_city=turn_assembly_pieces.user_city,
                                building=turn_assembly_pieces.pattern,
                                amount=turn_assembly_pieces.amount_assembly
                            )
                            new_building.save()
                            TurnAssemblyPiecesBuilding.objects.filter(id=turn_assembly_pieces.id).delete()