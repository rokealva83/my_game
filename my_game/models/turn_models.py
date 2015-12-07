# -*- coding: utf-8 -*-

from django.db import models
from my_game.models import MyUser, UserCity, ProjectShip, ManufacturingComplex, FactoryInstalled, FactoryPattern, BuildingPattern


class TurnBuilding(models.Model):
    class Meta:
        db_table = 'turn_building'

    user = models.ForeignKey(MyUser, db_index=True)
    user_city = models.ForeignKey(UserCity, db_index=True)
    factory = models.IntegerField(default=0)
    class_id = models.IntegerField(default=0)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    z = models.IntegerField(default=0)
    start_time_deployment = models.DateTimeField()
    finish_time_deployment = models.DateTimeField()


class TurnScientic(models.Model):
    class Meta:
        db_table = 'turn_scientic'

    user = models.ForeignKey(MyUser, db_index=True)
    mathematics_up = models.IntegerField(default=0)
    phisics_up = models.IntegerField(default=0)
    biologic_chimics_up = models.IntegerField(default=0)
    energetics_up = models.IntegerField(default=0)
    radionics_up = models.IntegerField(default=0)
    nanotech_up = models.IntegerField(default=0)
    astronomy_up = models.IntegerField(default=0)
    logistic_up = models.IntegerField(default=0)
    start_time_science = models.DateTimeField()
    finish_time_science = models.DateTimeField()


class TurnProduction(models.Model):
    class Meta:
        db_table = 'turn_production'

    user = models.ForeignKey(MyUser, db_index=True)
    user_city = models.ForeignKey(UserCity, db_index=True)
    factory = models.ForeignKey(FactoryInstalled)
    element_id = models.IntegerField()
    amount_element = models.IntegerField(default=1)
    start_time_production = models.DateTimeField()
    finish_time_production = models.DateTimeField()


class TurnComplexProduction(models.Model):
    class Meta:
        db_table = 'turn_complex_production'

    manufacturing_complex = models.ForeignKey(ManufacturingComplex)
    factory = models.ForeignKey(FactoryInstalled)
    element_id = models.IntegerField()
    start_time_production = models.DateTimeField()
    time = models.IntegerField()


class TurnAssemblyPiecesFactory(models.Model):
    class Meta:
        db_table = 'turn_assembly_pieces_factory'

    user = models.ForeignKey(MyUser, db_index=True)
    user_city = models.ForeignKey(UserCity, db_index=True)
    pattern = models.ForeignKey(FactoryPattern)
    class_id = models.IntegerField(default=0)
    amount_assembly = models.IntegerField(default=0)
    start_time_assembly = models.DateTimeField()
    finish_time_assembly = models.DateTimeField()

class TurnAssemblyPiecesBuilding(models.Model):
    class Meta:
        db_table = 'turn_assembly_pieces_building'

    user = models.ForeignKey(MyUser, db_index=True)
    user_city = models.ForeignKey(UserCity, db_index=True)
    pattern = models.ForeignKey(BuildingPattern)
    class_id = models.IntegerField(default=0)
    amount_assembly = models.IntegerField(default=0)
    start_time_assembly = models.DateTimeField()
    finish_time_assembly = models.DateTimeField()


class TurnShipBuild(models.Model):
    class Meta:
        db_table = 'turn_ship_build'

    user = models.ForeignKey(MyUser, db_index=True)
    user_city = models.ForeignKey(UserCity, db_index=True)
    process_id = models.IntegerField(default=0)
    project_ship = models.ForeignKey(ProjectShip)
    amount = models.IntegerField(default=0)
    start_time_build = models.DateTimeField()
    finish_time_build = models.DateTimeField()
