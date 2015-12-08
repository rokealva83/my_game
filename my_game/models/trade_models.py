# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from my_game.models import MyUser
from my_game.models import UserCity
from my_game.models import Fleet
from my_game.models import Planet


class TradeSpace(models.Model):
    class Meta:
        db_table = 'trade_space'

    name = models.CharField(max_length=64)
    user = models.ForeignKey(MyUser, db_index=True, blank=True, default=None)
    password = models.CharField(max_length=64, blank=True, default=None)
    tax = models.IntegerField()


class TradeElement(models.Model):
    class Meta:
        db_table = 'trade_element'

    name = models.CharField(max_length=50)
    user = models.ForeignKey(MyUser, db_index=True)
    buyer = models.IntegerField(default=0)
    trade_space = models.ForeignKey(TradeSpace, null=True, default=None)
    class_element = models.IntegerField()
    element_id = models.IntegerField()
    amount = models.IntegerField()
    min_amount = models.IntegerField()
    cost = models.IntegerField(default=0)
    cost_element = models.IntegerField()
    diplomacy = models.IntegerField(default=0)
    x = models.IntegerField()
    y = models.IntegerField()
    z = models.IntegerField()
    user_city = models.ForeignKey(UserCity)
    planet = models.ForeignKey(Planet, null=True, default=None)
    mass_element = models.IntegerField(default=0)
    size_element = models.IntegerField(default=0)


class DeliveryQueue(models.Model):
    class Meta:
        db_table = 'delivery_queue'

    user = models.ForeignKey(MyUser, db_index=True)
    user_city = models.IntegerField()
    name = models.CharField(max_length=50, default='new')
    class_element = models.IntegerField()
    element_id = models.IntegerField()
    amount = models.IntegerField()
    method = models.IntegerField()
    status = models.IntegerField()
    x = models.IntegerField()
    y = models.IntegerField()
    z = models.IntegerField()
    mass_element = models.IntegerField(default=0)
    size_element = models.IntegerField(default=0)


class TradeTeleport(models.Model):
    class Meta:
        db_table = 'trade_teleport'

    user = models.ForeignKey(MyUser, db_index=True)
    user_city = models.IntegerField()
    name = models.CharField(max_length=50, default='new')
    class_element = models.IntegerField()
    element_id = models.IntegerField()
    amount = models.IntegerField()
    start_teleport = models.DateTimeField()
    finish_teleport = models.DateTimeField()


class TradeFlight(models.Model):
    class Meta:
        db_table = 'trade_flight'

    user = models.ForeignKey(MyUser, db_index=True)
    user_city = models.ForeignKey(UserCity, db_index=True)
    fleet = models.ForeignKey(Fleet)
    flightplan = models.IntegerField()
    name = models.CharField(max_length=50)
    class_element = models.IntegerField()
    element_id = models.IntegerField()
    amount = models.IntegerField()
    mass = models.IntegerField(default=0)
    size = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    start_x = models.IntegerField()
    start_y = models.IntegerField()
    start_z = models.IntegerField()
    finish_x = models.IntegerField()
    finish_y = models.IntegerField()
    finish_z = models.IntegerField()
    flight_time = models.IntegerField(default=0)
    start_time = models.DateTimeField(default=timezone.now, blank=True)
    finish_time = models.DateTimeField(default=timezone.now, blank=True)
    planet = models.IntegerField(default=0)
