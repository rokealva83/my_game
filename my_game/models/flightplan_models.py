# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from my_game.models import MyUser
from my_game.models import Fleet


class Flightplan(models.Model):
    class Meta:
        db_table = 'flightplan'

    user = models.ForeignKey(MyUser, db_index=True)
    fleet = models.ForeignKey(Fleet, db_index=True)
    class_command = models.IntegerField()
    command_id = models.IntegerField()
    status = models.IntegerField()


class FlightplanFlight(models.Model):
    class Meta:
        db_table = 'flightplan_flight'

    user = models.ForeignKey(MyUser, db_index=True)
    fleet = models.ForeignKey(Fleet, db_index=True)
    flightplan = models.ForeignKey(Flightplan)
    command_id = models.IntegerField()
    start_x = models.IntegerField()
    start_y = models.IntegerField()
    start_z = models.IntegerField()
    finish_x = models.IntegerField()
    finish_y = models.IntegerField()
    finish_z = models.IntegerField()
    system_flight = models.BooleanField(default=True)
    flight_time = models.IntegerField(default=0)
    start_time = models.DateTimeField(default=timezone.now, blank=True)
    system_id = models.IntegerField(default=0)
    planet_id = models.IntegerField(default=0)


class FlightplanHold(models.Model):
    class Meta:
        db_table = 'flightplan_hold'

    user = models.ForeignKey(MyUser, db_index=True)
    fleet = models.ForeignKey(Fleet, db_index=True)
    flightplan = models.ForeignKey(Flightplan)
    command_id = models.IntegerField()
    class_element = models.IntegerField(default=0)
    element_id = models.IntegerField(default=0)
    amount = models.IntegerField()
    start_time = models.DateTimeField(default=timezone.now, blank=True)
    time = models.IntegerField(default=0)
    name = models.CharField(max_length=50, default='')


class FlightplanProduction(models.Model):
    class Meta:
        db_table = 'flightplan_production'

    user = models.ForeignKey(MyUser, db_index=True)
    fleet = models.ForeignKey(Fleet, db_index=True)
    flightplan = models.ForeignKey(Flightplan)
    command_id = models.IntegerField()
    production_per_minute = models.IntegerField()
    start_time = models.DateTimeField(default=timezone.now, blank=True)
    time_extraction = models.IntegerField(default=0)


class FlightplanRefill(models.Model):
    class Meta:
        db_table = 'flightplan_refill'

    user = models.ForeignKey(MyUser, db_index=True)
    fleet = models.ForeignKey(Fleet, db_index=True)
    flightplan = models.ForeignKey(Flightplan)
    command_id = models.IntegerField()
    fleet_refill_id = models.IntegerField()
    class_refill = models.IntegerField(default=0)
    class_element = models.IntegerField(default=0)
    element_id = models.IntegerField(default=0)
    amount = models.IntegerField()
    start_time = models.DateTimeField(default=timezone.now, blank=True)
    time_refill = models.IntegerField(default=0)
    name = models.CharField(max_length=50, default='')


class FlightplanBuildRepair(models.Model):
    class Meta:
        db_table = 'flightplan_build_repair'

    fleet = models.ForeignKey(Fleet, db_index=True)
    flightplan = models.ForeignKey(Flightplan)
    command_id = models.IntegerField()
    fleet_repair_id = models.IntegerField()
    start_time = models.DateTimeField(default=timezone.now, blank=True)
    time = models.IntegerField(default=0)


class FlightplanScan(models.Model):
    class Meta:
        db_table = 'flightplan_scan'

    user = models.ForeignKey(MyUser, db_index=True)
    fleet = models.ForeignKey(Fleet, db_index=True)
    flightplan = models.ForeignKey(Flightplan)
    command_id = models.IntegerField()
    range_scanning = models.IntegerField()
    start_time = models.DateTimeField(default=timezone.now, blank=True)
    time_scanning = models.IntegerField(default=0)


class FlightplanColonization(models.Model):
    class Meta:
        db_table = 'flightplan_colonization'

    fleet = models.ForeignKey(Fleet, db_index=True)
    flightplan = models.ForeignKey(Flightplan)
    command_id = models.IntegerField()
    start_time = models.DateTimeField(default=timezone.now, blank=True)
    time = models.IntegerField()


class FlightplanFight(models.Model):
    class Meta:
        db_table = 'flightplan_fight'

    user = models.ForeignKey(MyUser, db_index=True)
    fleet = models.ForeignKey(Fleet, db_index=True)
    flightplan = models.ForeignKey(Flightplan)
    command_id = models.IntegerField()
    fleet_attack_id = models.IntegerField()
    fight_id = models.IntegerField()
