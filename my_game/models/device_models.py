# -*- coding: utf-8 -*-

from django.db import models
from my_game.models import MyUser


class BasicDevice(models.Model):
    class Meta:
        db_table = 'basic_device'
        verbose_name = u'Устройство'
        verbose_name_plural = u'Устройства'

    CHOICES_CLASS_DEVICE = (
        (1, 'Колонизаторы'),
        (2, 'Геологические устройства')
        )

    device_name = models.CharField(max_length=50, verbose_name=u'Название')
    description = models.CharField(max_length=500, verbose_name=u'Описание')
    device_health = models.IntegerField(verbose_name=u'Количество жизни')
    param1 = models.IntegerField(verbose_name=u'Параметр 1', help_text=u'Время колонизации')
    param2 = models.IntegerField(verbose_name=u'Параметр 2')
    param3 = models.IntegerField(verbose_name=u'Параметр 3')
    device_mass = models.IntegerField(verbose_name=u'Масса')
    device_size = models.IntegerField(verbose_name=u'Размер')
    power_consuption = models.IntegerField(verbose_name=u'Потребление энергии')
    device_class = models.IntegerField(verbose_name=u'Класс устройства', choices=CHOICES_CLASS_DEVICE)
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
        return self.device_name


class DevicePattern(models.Model):
    class Meta:
        db_table = 'device_pattern'

    user = models.ForeignKey(MyUser, db_index=True)
    basic_device = models.ForeignKey(BasicDevice)
    device_name = models.CharField(max_length=50, default='New device')
    device_health = models.IntegerField()
    param1 = models.IntegerField()
    param2 = models.IntegerField()
    param3 = models.IntegerField()
    device_mass = models.IntegerField()
    device_size = models.IntegerField()
    power_consuption = models.IntegerField()
    device_class = models.IntegerField()
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
