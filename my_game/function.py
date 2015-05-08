# -*- coding: utf-8 -*-

import verification_func
from my_game.models import MyUser
from my_game.knowledge.scientific_verification_queue import check_scientific_verification_queue
import my_game.building.assembly_line_workpieces as assembly_line_workpieces
import my_game.building.verification_construction as verification_construction
import my_game.factory.verification_stage_production as verification_stage_production
import my_game.factory.verification_complex_stage as verification_complex_stage
import my_game.designing_ships.turn_ship_build as turn_ship_build
import flightplan.verification_flight_list as verification_flight_list
import my_game.trade.verification_trade as verification_trade


def check_all_queues(request):
    user = int(request)
    check_scientific_verification_queue(user)
    verification_construction.verification_phase_of_construction(user)
    verification_func.verification_of_resources(user)
    verification_trade.verification_trade(user)
    verification_flight_list.verification_flight_list(user)
    assembly_line_workpieces.check_assembly_line_workpieces(user)
    verification_stage_production.verification_stage_production(user)
    verification_complex_stage.verification_complex_stage(user)
    turn_ship_build.verification_turn_ship_build(user)



def check_all_user():
    users = MyUser.objects.all()
    for user in users:
        user = int(user.user_id)
        check_scientific_verification_queue(user)
        verification_construction.verification_phase_of_construction(user)
        verification_func.verification_of_resources(user)
        verification_trade.verification_trade(user)
        verification_flight_list.verification_flight_list(user)
        assembly_line_workpieces.check_assembly_line_workpieces(user)
        verification_stage_production.verification_stage_production(user)
        verification_complex_stage.verification_complex_stage(user)
        turn_ship_build.verification_turn_ship_build(user)