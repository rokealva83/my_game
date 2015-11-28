# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone


class Race(models.Model):
    class Meta:
        db_table = 'race'
        verbose_name = u'Раса'
        verbose_name_plural = u'Расы'

    race_name = models.CharField(max_length=50, default='Race', verbose_name=u'Название')
    description = models.CharField(max_length=4096, verbose_name=u'Описание')
    engine_system = models.FloatField(verbose_name=u'Системные двигатели')
    engine_intersystem = models.FloatField(verbose_name=u'Межсистемные двигатели')
    engine_giper = models.FloatField(verbose_name=u'Гиперпространственные двигатели')
    engine_null = models.FloatField(verbose_name=u'Двигатели Нуль-Т перехода')
    generator = models.FloatField(verbose_name=u'Генераторы')
    armor = models.FloatField(verbose_name=u'Броня')
    shield = models.FloatField(verbose_name=u'Щиты')
    weapon_attack = models.FloatField(verbose_name=u'Оружие атаки')
    weapon_defense = models.FloatField(verbose_name=u'Оружие защиты')
    exploration = models.FloatField(verbose_name=u'Исследования')
    disguse = models.FloatField(verbose_name=u'Маскировка')
    auximilary = models.FloatField(verbose_name=u'Устройства')
    image = models.ImageField(upload_to='race', verbose_name=u'Картинка')


class Union(models.Model):
    class Meta:
        db_table = 'union'
        verbose_name = u'Союз'
        verbose_name_plural = u'Союзы'

    union_name = models.CharField(max_length=50, default='', verbose_name=u'Название')


class Alliance(models.Model):
    class Meta:
        db_table = 'alliance'
        verbose_name = u'Альянс'
        verbose_name_plural = u'Альянсы'

    alliance_name = models.CharField(max_length=32, default='', verbose_name=u'Название')
    union = models.ForeignKey(Union, null=True, default=None, verbose_name=u'Союз')


class MyUser(models.Model):
    class Meta:
        db_table = 'my_user'
        verbose_name = u'Пользователь'
        verbose_name_plural = u'Пользователи'

    user_id = models.IntegerField(db_index=True)
    user_name = models.CharField(db_index=True, max_length=20, unique=True, verbose_name=u'Имя игрока')
    password = models.CharField(max_length=50, verbose_name=u'Пароль')
    race = models.ForeignKey(Race, verbose_name=u'Раса')
    alliance = models.ForeignKey(Alliance, null=True, default=None, verbose_name=u'Альянс')
    union = models.ForeignKey(Union, null=True, default=None, verbose_name=u'Союз')
    internal_currency = models.IntegerField(default=0, verbose_name=u'Внутренняя валюта')
    foreigh_currency = models.IntegerField(default=0, verbose_name=u'Внешняя валюта')
    real_currency = models.IntegerField(default=0, verbose_name=u'Реальная валюта')
    e_mail = models.CharField(db_index=True, max_length=50, unique=True, verbose_name=u'Почта')
    referal_code = models.CharField(max_length=50, verbose_name=u'Реферальная ссылка')
    user_luckyness = models.IntegerField(verbose_name=u'Удача')
    last_time_check = models.DateTimeField(verbose_name=u'Последня проверка добычи')
    last_time_scan_scient = models.DateTimeField(verbose_name=u'Последняя проверка исследований')
    premium_account = models.BooleanField(default=0, verbose_name=u'Премиум аккаунт')
    time_left_premium = models.DateTimeField(default=timezone.now, verbose_name=u'Время действия преемиум аккаунта')

    def __unicode__(self):
        return self.user_name


class UserScientic(models.Model):
    class Meta:
        db_table = 'user_scientic'

    user = models.ForeignKey(MyUser, db_index=True)
    mathematics_up = models.IntegerField(default=0)
    time_study_math = models.IntegerField()
    phisics_up = models.IntegerField(default=0)
    time_study_phis = models.IntegerField()
    biologic_chimics_up = models.IntegerField(default=0)
    time_study_biol = models.IntegerField()
    energetics_up = models.IntegerField(default=0)
    time_study_ener = models.IntegerField()
    radionics_up = models.IntegerField(default=0)
    time_study_radio = models.IntegerField()
    nanotech_up = models.IntegerField(default=0)
    time_study_nano = models.IntegerField()
    astronomy_up = models.IntegerField(default=0)
    time_study_astr = models.IntegerField()
    logistic_up = models.IntegerField(default=0)
    time_study_logis = models.IntegerField()
    all_scientic = models.IntegerField(default=0)


class Mail(models.Model):
    class Meta:
        db_table = 'mail'

    user = models.ForeignKey(MyUser, db_index=True)
    recipient = models.IntegerField()
    time = models.DateTimeField(default=timezone.now, blank=True)
    status = models.IntegerField()
    category = models.IntegerField()
    login_recipient = models.CharField(max_length=64)
    title = models.CharField(max_length=32)
    message = models.CharField(max_length=8192)
