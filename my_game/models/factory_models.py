# -*- coding: utf-8 -*-

from django.db import models
from my_game.models import MyUser
from my_game.models import ManufacturingComplex
from my_game.models import UserCity


class BasicFactory(models.Model):
    class Meta:
        db_table = 'basic_factory'
        verbose_name = u'Фабрика'
        verbose_name_plural = u'Фабрики'

    factory_name = models.CharField(max_length=50, verbose_name=u'Название')
    description = models.CharField(max_length=500, verbose_name=u'Описание')
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
    production_class = models.IntegerField(verbose_name=u'Класс продукции')
    production_id = models.IntegerField(verbose_name=u'Идентификатор продукции')
    time_production = models.IntegerField(verbose_name=u'Время производства')
    factory_size = models.IntegerField(verbose_name=u'Размер')
    factory_mass = models.IntegerField(verbose_name=u'Вес')
    power_consumption = models.IntegerField(default=0, verbose_name=u'Потребление энергии',
                                            help_text=u'Потребление энергии, а в случае с електростанциями - производство')

    def __unicode__(self):
        return self.factory_name


class FactoryPattern(models.Model):
    class Meta:
        db_table = 'factory_pattern'

    user = models.ForeignKey(MyUser, db_index=True)
    basic_factory = models.ForeignKey(BasicFactory)
    factory_name = models.CharField(max_length=64, default='New factory')
    price_internal_currency = models.IntegerField(default=25)
    price_construction_material = models.IntegerField(default=0, verbose_name=u'Цена в строительных материалах')
    price_chemical = models.IntegerField(default=0, verbose_name=u'Цена в химических реактивах')
    price_high_strength_allov = models.IntegerField(default=0, verbose_name=u'Цена в высокопрочных сплавах')
    price_nanoelement = models.IntegerField(default=0, verbose_name=u'Цена в наноелементах')
    price_microprocessor_element = models.IntegerField(default=0, verbose_name=u'Цена в микропроцессорных елементах')
    price_fober_optic_element = models.IntegerField(default=0, verbose_name=u'Цена в оптоволоконных елементах')
    cost_expert_deployment = models.IntegerField(default=10)
    assembly_workpiece = models.IntegerField(default=10)
    time_deployment = models.IntegerField()
    production_class = models.IntegerField()
    production_id = models.IntegerField()
    time_production = models.FloatField()
    factory_size = models.IntegerField()
    factory_mass = models.IntegerField()
    power_consumption = models.IntegerField(default=0)
    bought_template = models.BooleanField(default=False)


class WarehouseFactoryResource(models.Model):
    class Meta:
        db_table = 'warehouse_factory_resource'

    res_nickel = models.IntegerField(default=0)
    res_iron = models.IntegerField(default=0)
    res_cooper = models.IntegerField(default=0)
    res_aluminum = models.IntegerField(default=0)
    res_variarit = models.IntegerField(default=0)
    res_inneilit = models.IntegerField(default=0)
    res_renniit = models.IntegerField(default=0)
    res_cobalt = models.IntegerField(default=0)
    mat_construction_material = models.IntegerField(default=0)
    mat_chemical = models.IntegerField(default=0)
    mat_high_strength_allov = models.IntegerField(default=0)
    mat_nanoelement = models.IntegerField(default=0)
    mat_microprocessor_element = models.IntegerField(default=0)
    mat_fober_optic_element = models.IntegerField(default=0)


class WarehouseFactory(models.Model):
    class Meta:
        db_table = 'warehouse_factory'

    user = models.ForeignKey(MyUser, db_index=True)
    user_city = models.ForeignKey(UserCity, db_index=True)
    factory = models.ForeignKey(FactoryPattern, db_index=True)
    amount = models.IntegerField(default=0)


class FactoryInstalled(models.Model):
    class Meta:
        db_table = 'factory_installed'

    user = models.ForeignKey(MyUser, db_index=True)
    user_city = models.ForeignKey(UserCity, db_index=True)
    factory_pattern = models.ForeignKey(FactoryPattern)
    complex_status = models.BooleanField(default=0)
    manufacturing_complex = models.ForeignKey(ManufacturingComplex, null=True, default=None)
    factory_warehouse = models.ForeignKey(WarehouseFactoryResource)
    production_class = models.IntegerField(default=11)
    production_id = models.IntegerField(default=0)