# -*- coding: utf-8 -*-

from django.db import models
from my_game.models import MyUser


class BasicModule(models.Model):
    class Meta:
        db_table = 'basic_module'
        verbose_name = u'Модуль'
        verbose_name_plural = u'Модули'

    module_name = models.CharField(max_length=50, verbose_name=u'Название')
    description = models.CharField(max_length=500, verbose_name=u'Описание')
    module_health = models.IntegerField(verbose_name=u'Количество жизни')
    param1 = models.IntegerField(verbose_name=u'Параметр 1')
    param2 = models.IntegerField(verbose_name=u'Параметр 2')
    param3 = models.IntegerField(verbose_name=u'Параметр 3')
    module_mass = models.IntegerField(verbose_name=u'Масса')
    module_size = models.IntegerField(verbose_name=u'Размер')
    power_consuption = models.IntegerField(verbose_name=u'Потребление энергии')
    module_class = models.IntegerField(verbose_name=u'Класс модуля')
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
        return self.module_name


class ModulePattern(models.Model):
    class Meta:
        db_table = 'module_pattern'

    user = models.ForeignKey(MyUser, db_index=True)
    basic_module = models.ForeignKey(BasicModule)
    module_name = models.CharField(max_length=50, default='New module')
    module_health = models.IntegerField(verbose_name=u'')
    param1 = models.IntegerField(verbose_name=u'')
    param2 = models.IntegerField(verbose_name=u'')
    param3 = models.IntegerField(verbose_name=u'')
    module_mass = models.IntegerField(verbose_name=u'')
    module_size = models.IntegerField(verbose_name=u'')
    power_consuption = models.IntegerField(verbose_name=u'')
    module_class = models.IntegerField(verbose_name=u'')
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
