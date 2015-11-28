# -*- coding: utf-8 -*-

from django.db import models
from my_game.models import MyUser
from my_game.models import HullPattern
from my_game.models import Fleet
from my_game.models import UserCity

class ProjectShip(models.Model):
    class Meta:
        db_table = 'project_ship'

    user = models.ForeignKey(MyUser, db_index=True)
    project_name = models.CharField(max_length=32)
    hull_pattern = models.ForeignKey(HullPattern, default=None)
    system_power = models.IntegerField(default=0)
    system_fuel = models.IntegerField(default=0)
    intersystem_power = models.IntegerField(default=0)
    intersystem_fuel = models.IntegerField(default=0)
    giper_power = models.IntegerField(default=0)
    giper_energy = models.IntegerField(default=0)
    giper_accuracy = models.FloatField(default=0.9)
    null_power = models.IntegerField(default=0)
    null_energy = models.IntegerField(default=0)
    null_accuracy = models.FloatField(default=0.9)
    generator_fuel = models.IntegerField(default=0)
    generator_energy = models.IntegerField(default=0)
    maneuverability = models.FloatField(default=0)
    time_build = models.IntegerField(default=0)
    ship_mass = models.IntegerField(default=500)


class ElementShip(models.Model):
    class Meta:
        db_table = 'element_ship'

    project_ship = models.ForeignKey(ProjectShip, db_index=True)
    class_element = models.IntegerField(db_index=True)
    element_pattern_id = models.IntegerField()
    position = models.IntegerField()
    element_health = models.IntegerField()


class Ship(models.Model):
    class Meta:
        db_table = 'ship'

    user = models.ForeignKey(MyUser, db_index=True)
    project_ship = models.ForeignKey(ProjectShip, db_index=True)
    ship_name = models.CharField(max_length=32, default='New ship')
    amount_ship = models.IntegerField()
    fleet_status = models.BooleanField(default=0)
    place_id = models.IntegerField()


class DamageShip(models.Model):
    class Meta:
        db_table = 'damage_ship'

    user = models.ForeignKey(MyUser, db_index=True)
    fleet = models.ForeignKey(Fleet)
    project_ship = models.ForeignKey(ProjectShip)


class DamageElement(models.Model):
    class Meta:
        db_table = 'damage_element'

    damage_ship = models.ForeignKey(DamageShip, db_index=True)
    element_id = models.IntegerField()
    health = models.IntegerField()


class WarehouseShip(models.Model):
    class Meta:
        db_table = 'warehouse_ship'

    user = models.ForeignKey(MyUser, db_index=True)
    user_city = models.ForeignKey(UserCity, db_index=True)
    ship = models.ForeignKey(Ship)
    amount = models.IntegerField(default=0)