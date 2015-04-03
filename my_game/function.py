# -*- coding: utf-8 -*-

from django.utils import timezone
from my_game.models import MyUser
import verification_func
from my_game.knowledge.scientific_verification_queue import check_scientific_verification_queue
import my_game.building.assembly_line_workpieces as assembly_line_workpieces
import my_game.building.verification_construction as verification_construction
import my_game.factory.verification_stage_production as verification_stage_production
import my_game.designing_ships.turn_ship_build as turn_ship_build
import my_game.flying.verification_flight_list as verification_flight_list
import my_game.trade.verification_trade as verification_trade



def check_all_queues(request):
    user = int(request)
    check_scientific_verification_queue(user)
    verification_construction.verification_phase_of_construction(user)
    now_date = timezone.now()
    time_update = MyUser.objects.filter(user_id=user).first().last_time_check
    elapsed_time_full = now_date - time_update
    elapsed_time_seconds = elapsed_time_full.seconds
    time_update = now_date
    if elapsed_time_seconds > 300:
        verification_func.verification_of_resources(user, elapsed_time_seconds, time_update)
    verification_trade.verification_trade(user)
    verification_flight_list.verification_flight_list(user)
    assembly_line_workpieces.check_assembly_line_workpieces(user)
    verification_stage_production.verification_stage_production(user)
    turn_ship_build.verification_turn_ship_build(user)

