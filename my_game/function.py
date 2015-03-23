# -*- coding: utf-8 -*-

from django.utils import timezone
from my_game.models import MyUser
import verification_func


def check_all_queues(request):
    user = int(request)
    verification_func.check_scientific_verification_queue(user)
    verification_func.verification_phase_of_construction(user)
    now_date = timezone.now()
    time_update = MyUser.objects.filter(user_id=user).first().last_time_check
    elapsed_time_full = now_date - time_update
    elapsed_time_seconds = elapsed_time_full.seconds
    time_update = now_date
    if elapsed_time_seconds > 300:
        verification_func.verification_of_resources(user, elapsed_time_seconds, time_update)
    verification_func.verification_trade(user)
    verification_func.verification_flight_list(user)
    verification_func.check_assembly_line_workpieces(user)
    verification_func.verification_stage_production(user)
    verification_func.verification_turn_ship_build(user)

