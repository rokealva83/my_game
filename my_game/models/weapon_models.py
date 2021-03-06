# -*- coding: utf-8 -*-

from django.db import models
from my_game.models import MyUser


class BasicWeapon(models.Model):
    class Meta:
        db_table = 'basic_weapon'
        verbose_name = u'Оружие'
        verbose_name_plural = u'Оружие'

    CHOICES_WEAPON_CLASS = (
        (1, '1.Энергетическое'),
        (2, '2.Энергетический главный калибр'),
        (3, '3.Кинетическое'),
        (4, '4.Кинетический главный калибр'),
    )

    CHOICES_SHELL_CLASS = (
        (0, 'Энергия'),
        (1, 'Снаряды'),
        (2, 'Ракеты'),
        (3, 'Торпеды')
        )

    weapon_name = models.CharField(max_length=50, verbose_name=u'Название')
    description = models.CharField(max_length=500, verbose_name=u'Описание')
    weapon_health = models.IntegerField(verbose_name=u'Количество жизни')
    weapon_energy_damage = models.IntegerField(default=0, verbose_name=u'Энергетический урон')
    weapon_regenerations = models.IntegerField(default=0, verbose_name=u'Время перезарядки')
    number_of_bursts = models.IntegerField(default=0, verbose_name=u'Количество залпов')
    weapon_range = models.IntegerField(default=0, verbose_name=u'Дальность')
    weapon_accuracy = models.IntegerField(default=0, verbose_name=u'Точность')
    weapon_mass = models.IntegerField(default=0, verbose_name=u'Масса')
    weapon_size = models.IntegerField(verbose_name=u'Размер')
    power_consuption = models.IntegerField(verbose_name=u'Потребление энергии')
    weapon_class = models.IntegerField(default=1, verbose_name=u'Класс оружия', choices=CHOICES_WEAPON_CLASS)
    shell_class = models.IntegerField(default=0, verbose_name=u'Класс боеприпаса', choices=CHOICES_SHELL_CLASS)
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
        return self.weapon_name


class WeaponPattern(models.Model):
    class Meta:
        db_table = 'weapon_pattern'

    user = models.ForeignKey(MyUser, db_index=True)
    basic_pattern = models.ForeignKey(BasicWeapon)
    element_name = models.CharField(max_length=50, default='New weapon')
    weapon_health = models.IntegerField()
    weapon_energy_damage = models.IntegerField(default=0)
    weapon_regenerations = models.IntegerField(default=0)
    number_of_bursts = models.IntegerField(default=0)
    weapon_range = models.IntegerField(default=0)
    weapon_accuracy = models.IntegerField(default=0)
    weapon_mass = models.IntegerField()
    weapon_size = models.IntegerField()
    power_consuption = models.IntegerField()
    weapon_class = models.IntegerField(default=1)
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
