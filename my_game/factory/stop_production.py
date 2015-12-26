# -*- coding: utf-8 -*-

from django.shortcuts import render
from my_game.models import MyUser, UserCity, TurnProduction
from my_game.models import FactoryInstalled
from my_game.models import WarehouseFactory
from my_game.models import ManufacturingComplex
from my_game.factory import verification_stage_production
from my_game.building import assembly_line_workpieces
from my_game.factory.rename_element_pattern import rename_element_pattern
from my_game.factory.production_module import production_module
from my_game.models import TurnProduction


def stop_production(turn_id):
    turn_obj = TurnProduction.objects.filter(id=turn_id).first()

    message = 'Производство остановлено(not worked)'

    return message