# -*- coding: utf-8 -*-

from django.db import models


class UserVariables(models.Model):
    class Meta:
        db_table = 'user_variables'
        verbose_name = u'Глобальная переменная'
        verbose_name_plural = u'Глобальные переменные'

    registr_internal_currency = models.IntegerField(verbose_name=u'Валюта при регистрации')
    registr_nickel = models.IntegerField(default=0, verbose_name=u'Цена в никеле')
    registr_iron = models.IntegerField(default=0, verbose_name=u'Цена в железе')
    registr_cooper = models.IntegerField(default=0, verbose_name=u'Цена в меди')
    registr_aluminum = models.IntegerField(default=0, verbose_name=u'Цена в алюминии')
    registr_veriarit = models.IntegerField(default=0, verbose_name=u'Цена в вариатите')
    registr_inneilit = models.IntegerField(default=0, verbose_name=u'Цена в иннэилите')
    registr_renniit = models.IntegerField(default=0, verbose_name=u'Цена в ренниите')
    registr_cobalt = models.IntegerField(default=0, verbose_name=u'Цена в кобальте')
    registr_construction_material = models.IntegerField(default=0, verbose_name=u'Цена в строительных материалах')
    registr_chemical = models.IntegerField(default=0, verbose_name=u'Цена в химических реактивах')
    registr_high_strength_allov = models.IntegerField(default=0, verbose_name=u'Цена в высокопрочных сплавах')
    registr_nanoelement = models.IntegerField(default=0, verbose_name=u'Цена в наноелементах')
    registr_microprocessor_element = models.IntegerField(default=0, verbose_name=u'Цена в микропроцессорных елементах')
    registr_fober_optic_element = models.IntegerField(default=0, verbose_name=u'Цена в оптоволоконных елементах')
    basic_time_build_ship = models.IntegerField(verbose_name=u'Базовое время сборки корабля')
    koef_ship_element_time = models.FloatField(verbose_name=u'Коефициент увеличения времени сборки корабля')
    minimum_scan_time = models.IntegerField(verbose_name=u'Минимальное время сканирования')
    max_turn_assembly_pieces_basic = models.IntegerField(verbose_name=u'Базовая очередь сборки заготовок')
    max_turn_assembly_pieces_premium = models.IntegerField(verbose_name=u'Премиумная очередь сборки заготовок')
    max_turn_building_basic = models.IntegerField(verbose_name=u'Базовая очередь строительства')
    max_turn_building_premium = models.IntegerField(verbose_name=u'Премиумная очередь строительства')
    max_turn_production_basic = models.IntegerField(verbose_name=u'Базовая очередь производства')
    max_turn_production_premium = models.IntegerField(verbose_name=u'Премиумная очередь производства')
    max_turn_scientic_basic = models.IntegerField(verbose_name=u'Базовая очередь иследований')
    max_turn_scientic_premium = models.IntegerField(verbose_name=u'Премиумная очередь иследований')
    max_turn_ship_build_basic = models.IntegerField(verbose_name=u'Базовая очередь сборки кораблей')
    max_turn_ship_build_premium = models.IntegerField(verbose_name=u'Премиумная очередь сборки кораблей')
    time_check_new_technology = models.IntegerField(verbose_name=u'Период открытия новой технологии')
    min_scientic_level = models.IntegerField(verbose_name=u'Минимальный научный уровень')
    tax_per_person = models.FloatField(verbose_name=u'Налог')
    koef_price_increace_modern_element = models.FloatField(verbose_name=u'Коефициент увеличения цены при модернизации')


class BasicResource(models.Model):
    class Meta:
        db_table = 'basic_resource'
        verbose_name = u'Ресурс'
        verbose_name_plural = u'Ресурсы'

    resource_name = models.CharField(max_length=50, verbose_name=u'Название')
    description = models.CharField(max_length=1000, verbose_name=u'Описание')


class BasicMaterial(models.Model):
    class Meta:
        db_table = 'basic_material'
        verbose_name = u'Материал'
        verbose_name_plural = u'Материалы'

    material_name = models.CharField(max_length=50, verbose_name=u'Название')
    description = models.CharField(max_length=1000, verbose_name=u'Описание')
    price_internal_currency = models.IntegerField(default=25, verbose_name=u'Цена в валюте')
    price_nickel = models.IntegerField(default=0, verbose_name=u'Цена в никеле')
    price_iron = models.IntegerField(default=0, verbose_name=u'Цена в железе')
    price_cooper = models.IntegerField(default=0, verbose_name=u'Цена в меди')
    price_aluminum = models.IntegerField(default=0, verbose_name=u'Цена в алюминии')
    price_veriarit = models.IntegerField(default=0, verbose_name=u'Цена в вариатите')
    price_inneilit = models.IntegerField(default=0, verbose_name=u'Цена в иннэилите')
    price_renniit = models.IntegerField(default=0, verbose_name=u'Цена в ренниите')
    price_cobalt = models.IntegerField(default=0, verbose_name=u'Цена в кобальте')
    time_production = models.IntegerField(verbose_name=u'Время производства')
    material_size = models.IntegerField(verbose_name=u'Размер')
    material_mass = models.IntegerField(verbose_name=u'Вес')


class BasicScientic(models.Model):
    class Meta:
        db_table = 'basic_scientic'
        verbose_name = u'Наука'
        verbose_name_plural = u'Науки'

    scientic_id = models.AutoField(primary_key=True)
    scientic_name = models.CharField(max_length=128, verbose_name=u'Название')
    description = models.CharField(max_length=4096, verbose_name=u'Описание')
    time_study = models.IntegerField(verbose_name=u'Время изучения')
    price_internal_currency = models.IntegerField(default=25, verbose_name=u'Цена в валюте')
    price_nickel = models.IntegerField(default=0, verbose_name=u'Цена в никеле')
    price_iron = models.IntegerField(default=0, verbose_name=u'Цена в железе')
    price_cooper = models.IntegerField(default=0, verbose_name=u'Цена в меди')
    price_aluminum = models.IntegerField(default=0, verbose_name=u'Цена в алюминии')
    price_veriarit = models.IntegerField(default=0, verbose_name=u'Цена в вариатите')
    price_inneilit = models.IntegerField(default=0, verbose_name=u'Цена в иннэилите')
    price_renniit = models.IntegerField(default=0, verbose_name=u'Цена в ренниите')
    price_cobalt = models.IntegerField(default=0, verbose_name=u'Цена в кобальте')

    def __unicode__(self):
        return self.description
