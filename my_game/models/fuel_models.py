# -*- coding: utf-8 -*-

from django.db import models
from my_game.models import MyUser


class BasicFuel(models.Model):
    class Meta:
        db_table = 'basic_fuel'
        verbose_name = u'Топливо'
        verbose_name_plural = u'Топливо'

    fuel_name = models.CharField(max_length=50, verbose_name=u'Название')
    description = models.CharField(max_length=500, verbose_name=u'Описание')
    fuel_mass = models.IntegerField(verbose_name=u'Масса')
    fuel_size = models.IntegerField(verbose_name=u'Размер')
    fuel_efficiency = models.IntegerField(verbose_name=u'Эфективность топлива')
    fuel_class = models.IntegerField(verbose_name=u'Класс топлива')
    fuel_id = models.IntegerField(default=0, verbose_name=u'Идентификатор топлива')
    price_internal_currency = models.IntegerField(default=25, verbose_name=u'Цена в валюте')
    price_veriarit = models.IntegerField(default=0, verbose_name=u'Цена в вариатите')
    price_inneilit = models.IntegerField(default=0, verbose_name=u'Цена в иннэилите')
    price_renniit = models.IntegerField(default=0, verbose_name=u'Цена в ренниите')
    price_cobalt = models.IntegerField(default=0, verbose_name=u'Цена в кобальте')
    price_chemical = models.IntegerField(default=0, verbose_name=u'Цена в химических реактивах')

    def __unicode__(self):
        return self.fuel_name


class FuelPattern(models.Model):
    class Meta:
        db_table = 'fuel_pattern'

    user = models.ForeignKey(MyUser,db_index=True, default=2)
    fuel_name = models.CharField(max_length=50)
    basic_fuel = models.ForeignKey(BasicFuel)
    fuel_mass = models.IntegerField()
    fuel_size = models.IntegerField()
    fuel_efficiency = models.IntegerField()
    fuel_class = models.IntegerField()
    fuel_id = models.IntegerField(default=0)
    price_internal_currency = models.IntegerField(default=25, verbose_name=u'Цена в валюте')
    price_veriarit = models.IntegerField(default=0, verbose_name=u'Цена в вариатите')
    price_inneilit = models.IntegerField(default=0, verbose_name=u'Цена в иннэилите')
    price_renniit = models.IntegerField(default=0, verbose_name=u'Цена в ренниите')
    price_cobalt = models.IntegerField(default=0, verbose_name=u'Цена в кобальте')
    price_chemical = models.IntegerField(default=0, verbose_name=u'Цена в химических реактивах')

    def __unicode__(self):
        return self.fuel_name
