# -*- coding: utf-8 -*-

from django.db import models
from my_game.models import MyUser, UserCity


class BasicBuilding(models.Model):
    class Meta:
        db_table = 'basic_building'
        verbose_name = u'Строение'
        verbose_name_plural = u'Строения'

    building_name = models.CharField(max_length=50, verbose_name=u'Название')
    description = models.CharField(max_length=500, verbose_name=u'Описание')
    production_class = models.IntegerField(verbose_name=u'Класс продукции')
    production_id = models.IntegerField(verbose_name=u'Идентификатор продукции')
    time_production = models.IntegerField(verbose_name=u'Время производства')
    warehouse = models.IntegerField(default=0, verbose_name=u'Склад')
    max_warehouse = models.IntegerField(default=500, verbose_name=u'Максимальный размер склада')
    price_internal_currency = models.IntegerField(default=25, verbose_name=u'Цена в валюте')
    price_construction_material = models.IntegerField(default=0, verbose_name=u'Цена в строительных материалах')
    price_chemical = models.IntegerField(default=0, verbose_name=u'Цена в химических реактивах')
    price_high_strength_allov = models.IntegerField(default=0, verbose_name=u'Цена в высокопрочных сплавах')
    price_nanoelement = models.IntegerField(default=0, verbose_name=u'Цена в наноелементах')
    price_microprocessor_element = models.IntegerField(default=0, verbose_name=u'Цена в микропроцессорных елементах')
    price_fober_optic_element = models.IntegerField(default=0, verbose_name=u'Цена в оптоволоконных елементах')
    price_expert_deployment = models.IntegerField(default=10, verbose_name=u'Количество сотрудников')
    assembly_workpiece = models.IntegerField(default=10, verbose_name=u'Время создания заготовки')
    time_deployment = models.IntegerField(verbose_name=u'Время развертывания')
    building_size = models.IntegerField(verbose_name=u'Размер')
    building_mass = models.IntegerField(verbose_name=u'Масса')
    power_consumption = models.IntegerField(default=0, verbose_name=u'Потребление энергии')

    def __unicode__(self):
        return self.building_name


class BuildingPattern(models.Model):
    class Meta:
        db_table = 'building_pattern'

    user = models.ForeignKey(MyUser, db_index=True)
    building_name = models.CharField(max_length=50)
    basic_building = models.ForeignKey(BasicBuilding)
    production_class = models.IntegerField()
    production_id = models.IntegerField()
    time_production = models.IntegerField()
    warehouse = models.IntegerField(default=0)
    max_warehouse = models.IntegerField(default=500)
    price_internal_currency = models.IntegerField(default=0)
    price_construction_material = models.IntegerField(default=0, verbose_name=u'Цена в строительных материалах')
    price_chemical = models.IntegerField(default=0, verbose_name=u'Цена в химических реактивах')
    price_high_strength_allov = models.IntegerField(default=0, verbose_name=u'Цена в высокопрочных сплавах')
    price_nanoelement = models.IntegerField(default=0, verbose_name=u'Цена в наноелементах')
    price_microprocessor_element = models.IntegerField(default=0, verbose_name=u'Цена в микропроцессорных елементах')
    price_fober_optic_element = models.IntegerField(default=0, verbose_name=u'Цена в оптоволоконных елементах')
    cost_expert_deployment = models.IntegerField(default=10)
    assembly_workpiece = models.IntegerField(default=10)
    time_deployment = models.IntegerField()
    building_size = models.IntegerField()
    building_mass = models.IntegerField()
    power_consumption = models.IntegerField(default=0)


class BuildingInstalled(models.Model):
    class Meta:
        db_table = 'building_installed'

    user = models.ForeignKey(MyUser, db_index=True)
    user_city = models.ForeignKey(UserCity, db_index=True)
    building_pattern = models.ForeignKey(BuildingPattern)
    production_class = models.IntegerField(default=21)
    production_id = models.IntegerField(default=1)
    warehouse = models.IntegerField(default=0)


class WarehouseBuilding(models.Model):
    class Meta:
        db_table = 'warehouse_building'

    user = models.ForeignKey(MyUser, db_index=True)
    user_city = models.ForeignKey(UserCity, db_index=True)
    building = models.ForeignKey(BuildingPattern, db_index=True)
    amount = models.IntegerField(default=0)
