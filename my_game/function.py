# -*- coding: utf-8 -*-

from django.utils import timezone
from my_game.models import MyUser
import verification_func
from knowledge import scientific_verification_queue
from building import verification_construction, assembly_line_workpieces
from factory import verification_stage_production
from designing_ships import turn_ship_build
from flying import verification_flight_list
from trade import verification_trade



def check_all_queues(request):
    user = int(request)
    scientific_verification_queue.check_scientific_verification_queue(user)
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

