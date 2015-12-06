# -*- coding: utf-8 -*-

from django.db import models
from my_game.models import MyUser


class BasicArmor(models.Model):
    class Meta:
        db_table = 'basic_armor'
        verbose_name = u'Бронь'
        verbose_name_plural = u'Бронь'

    armor_name = models.CharField(max_length=50, verbose_name=u'Название')
    description = models.CharField(max_length=500, verbose_name=u'Описание')
    armor_health = models.IntegerField(verbose_name=u'Количество жизни')
    value_energy_resistance = models.IntegerField(verbose_name=u'Отражение энергитического урона')
    value_phisical_resistance = models.IntegerField(verbose_name=u'Отражение физического урона')
    armor_power = models.IntegerField(verbose_name=u'Сила брони')
    armor_regeneration = models.IntegerField(verbose_name=u'Востановление брони')
    armor_mass = models.IntegerField(verbose_name=u'Масса')
    price_internal_currency = models.IntegerField(default=25, verbose_name=u'Цена в валюте')
    price_nickel = models.IntegerField(default=0, verbose_name=u'Цена в никеле')
    price_iron = models.IntegerField(default=0, verbose_name=u'Цена в железе')
    price_cooper = models.IntegerField(default=0, verbose_name=u'Цена в меди')
    price_aluminum = models.IntegerField(default=0, verbose_name=u'Цена в алюминии')
    price_veriarit = models.IntegerField(default=0, verbose_name=u'Цена в вариатите')
    price_inneilit = models.IntegerField(default=0, verbose_name=u'Цена в иннэилите')
    price_renniit = models.IntegerField(default=0, verbose_name=u'Цена в ренниите')
    price_cobalt = models.IntegerField(default=0, verbose_name=u'Цена в кобальте')
    price_construction_material = models.IntegerField(default=0, verbose_name=u'Цена в строительных материалах')
    price_chemical = models.IntegerField(default=0, verbose_name=u'Цена в химических реактивах')
    price_high_strength_allov = models.IntegerField(default=0, verbose_name=u'Цена в высокопрочных сплавах')
    price_nanoelement = models.IntegerField(default=0, verbose_name=u'Цена в наноелементах')
    price_microprocessor_element = models.IntegerField(default=0, verbose_name=u'Цена в микропроцессорных елементах')
    price_fober_optic_element = models.IntegerField(default=0, verbose_name=u'Цена в оптоволоконных елементах')
    min_all_scientic = models.IntegerField(default=0, verbose_name=u'Минимальный уровень науки')
    min_math = models.IntegerField(default=0, verbose_name=u'Минимальный уровень математики')
    min_phis = models.IntegerField(default=0, verbose_name=u'Минимальный уровень физики')
    min_biol = models.IntegerField(default=0, verbose_name=u'Минимальный уровень биологии')
    min_energy = models.IntegerField(default=0, verbose_name=u'Минимальный уровень химии')
    min_radio = models.IntegerField(default=0, verbose_name=u'Минимальный уровень електротехники')
    min_nanotech = models.IntegerField(default=0, verbose_name=u'Минимальный уровень нанотехнологий')
    min_astronomy = models.IntegerField(default=0, verbose_name=u'Минимальный уровень астрономии')
    min_logist = models.IntegerField(default=0, verbose_name=u'Минимальный уровень логистики')

    def __unicode__(self):
        return self.armor_name


class ArmorPattern(models.Model):
    class Meta:
        db_table = 'armor_pattern'

    user = models.ForeignKey(MyUser, db_index=True)
    basic_pattern = models.ForeignKey(BasicArmor)
    element_name = models.CharField(max_length=50, default='New armor')
    armor_health = models.FloatField()
    value_energy_resistance = models.FloatField()
    value_phisical_resistance = models.FloatField()
    armor_power = models.FloatField()
    armor_regeneration = models.FloatField()
    armor_mass = models.FloatField()
    price_internal_currency = models.IntegerField(default=25)
    price_nickel = models.IntegerField(default=0, verbose_name=u'Цена в никеле')
    price_iron = models.IntegerField(default=0, verbose_name=u'Цена в железе')
    price_cooper = models.IntegerField(default=0, verbose_name=u'Цена в меди')
    price_aluminum = models.IntegerField(default=0, verbose_name=u'Цена в алюминии')
    price_veriarit = models.IntegerField(default=0, verbose_name=u'Цена в вариатите')
    price_inneilit = models.IntegerField(default=0, verbose_name=u'Цена в иннэилите')
    price_renniit = models.IntegerField(default=0, verbose_name=u'Цена в ренниите')
    price_cobalt = models.IntegerField(default=0, verbose_name=u'Цена в кобальте')
    price_construction_material = models.IntegerField(default=0, verbose_name=u'Цена в строительных материалах')
    price_chemical = models.IntegerField(default=0, verbose_name=u'Цена в химических реактивах')
    price_high_strength_allov = models.IntegerField(default=0, verbose_name=u'Цена в высокопрочных сплавах')
    price_nanoelement = models.IntegerField(default=0, verbose_name=u'Цена в наноелементах')
    price_microprocessor_element = models.IntegerField(default=0, verbose_name=u'Цена в микропроцессорных елементах')
    price_fober_optic_element = models.IntegerField(default=0, verbose_name=u'Цена в оптоволоконных елементах')
    bought_template = models.BooleanField(default=False)
