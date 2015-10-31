# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from datetime import datetime


class UserVariables(models.Model):
    class Meta:
        db_table = 'user_variables'
        verbose_name = u'Глобальная переменная'
        verbose_name_plural = u'Глобальные переменные'

    registr_internal_currency = models.IntegerField(verbose_name=u'Валюта при регистрации')
    registr_resource1 = models.IntegerField(verbose_name=u'Ресурс при регистраци')
    registr_resource2 = models.IntegerField(verbose_name=u'Ресурс при регистраци')
    registr_resource3 = models.IntegerField(verbose_name=u'Ресурс при регистраци')
    registr_resource4 = models.IntegerField(verbose_name=u'Ресурс при регистраци')
    registr_mineral1 = models.IntegerField(verbose_name=u'Минерал при регистраци')
    registr_mineral2 = models.IntegerField(verbose_name=u'Минерал при регистраци')
    registr_mineral3 = models.IntegerField(verbose_name=u'Минерал при регистраци')
    registr_mineral4 = models.IntegerField(verbose_name=u'Минерал при регистраци')
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


class Galaxy(models.Model):
    class Meta:
        db_table = 'galaxy'

    x = models.IntegerField()
    y = models.IntegerField()
    z = models.IntegerField()


class System(models.Model):
    class Meta:
        db_table = 'system'

    galaxy = models.ForeignKey(Galaxy, )
    x = models.IntegerField(db_index=True)
    y = models.IntegerField(db_index=True)
    z = models.IntegerField(db_index=True)
    system_type = models.IntegerField()
    system_size = models.FloatField()
    star_size = models.FloatField()


class Planet(models.Model):
    class Meta:
        db_table = 'planet'

    system = models.ForeignKey(System, )
    global_x = models.IntegerField(db_index=True)
    global_y = models.IntegerField(db_index=True)
    global_z = models.IntegerField(db_index=True)
    system_x = models.IntegerField(db_index=True, default=0)
    system_y = models.IntegerField(db_index=True, default=0)
    system_z = models.IntegerField(db_index=True, default=0)
    planet_num = models.IntegerField()
    planet_name = models.CharField(max_length=20, default='New Planet')
    planet_type = models.IntegerField()
    planet_size = models.IntegerField()
    orb_radius = models.IntegerField()
    area_planet = models.IntegerField()
    work_area_planet = models.IntegerField()
    planet_displacement_vector = models.IntegerField(default=0)
    planet_offset_angle = models.FloatField(default=0)
    planet_free = models.BooleanField(default=True)

    def __unicode__(self):
        return self.planet_name


class PlanetType(models.Model):
    class Meta:
        db_table = 'planet_type'

    description = models.CharField(max_length=500, verbose_name=u'')
    gravity = models.CharField(max_length=20, verbose_name=u'')
    atmosphere = models.CharField(max_length=20, verbose_name=u'')


class UserCity(models.Model):
    class Meta:
        db_table = 'user_city'

    user = models.ForeignKey(MyUser, db_index=True, verbose_name=u'Город')
    system = models.ForeignKey(System, db_index=True, null=True, default=None, verbose_name=u'')
    planet = models.ForeignKey(Planet, db_index=True, null=True, default=None, verbose_name=u'')
    x = models.IntegerField()
    y = models.IntegerField()
    z = models.IntegerField()
    name_city = models.CharField(db_index=True, max_length=20, default='New City', verbose_name=u'')
    city_size_free = models.IntegerField(verbose_name=u'')
    population = models.IntegerField(default=150, verbose_name=u'')
    max_population = models.IntegerField(default=500, verbose_name=u'')
    founding_date = models.DateTimeField(verbose_name=u'')
    extraction_date = models.DateTimeField(verbose_name=u'')
    power = models.IntegerField(default=0, verbose_name=u'')
    use_energy = models.IntegerField(default=0, verbose_name=u'')


class Warehouse(models.Model):
    class Meta:
        db_table = 'warehouse'

    user = models.ForeignKey(MyUser, db_index=True)
    user_city = models.ForeignKey(UserCity, db_index=True)
    resource_id = models.IntegerField(default=0)
    amount = models.IntegerField(default=125000)


class BasicResource(models.Model):
    class Meta:
        db_table = 'basic_resource'
        verbose_name = u'Ресурс'
        verbose_name_plural = u'Ресурсы'

    resource_name = models.CharField(max_length=50, verbose_name=u'Название')
    description = models.CharField(max_length=1000, verbose_name=u'Описание')


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
    price_resource1 = models.IntegerField(default=0, verbose_name=u'Цена в никеле')
    price_resource2 = models.IntegerField(default=0, verbose_name=u'Цена в железе')
    price_resource3 = models.IntegerField(default=0, verbose_name=u'Цена в меди')
    price_resource4 = models.IntegerField(default=0, verbose_name=u'Цена в алюминии')
    price_mineral1 = models.IntegerField(default=0, verbose_name=u'Цена в вариатите')
    price_mineral2 = models.IntegerField(default=0, verbose_name=u'Цена в иннэилите')
    price_mineral3 = models.IntegerField(default=0, verbose_name=u'Цена в ренниите')
    price_mineral4 = models.IntegerField(default=0, verbose_name=u'Цена в кобальте')

    def __unicode__(self):
        return self.description


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


class BasicFactory(models.Model):
    class Meta:
        db_table = 'basic_factory'
        verbose_name = u'Фабрика'
        verbose_name_plural = u'Фабрики'

    factory_name = models.CharField(max_length=50, verbose_name=u'Название')
    description = models.CharField(max_length=500, verbose_name=u'Описание')
    price_internal_currency = models.IntegerField(default=25, verbose_name=u'Цена в валюте')
    price_resource1 = models.IntegerField(default=0, verbose_name=u'Цена в никеле')
    price_resource2 = models.IntegerField(default=0, verbose_name=u'Цена в железе')
    price_resource3 = models.IntegerField(default=0, verbose_name=u'Цена в меди')
    price_resource4 = models.IntegerField(default=0, verbose_name=u'Цена в алюминии')
    price_mineral1 = models.IntegerField(default=0, verbose_name=u'Цена в вариатите')
    price_mineral2 = models.IntegerField(default=0, verbose_name=u'Цена в иннэилите')
    price_mineral3 = models.IntegerField(default=0, verbose_name=u'Цена в ренниите')
    price_mineral4 = models.IntegerField(default=0, verbose_name=u'Цена в кобальте')
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
    price_resource1 = models.IntegerField(default=0)
    price_resource2 = models.IntegerField(default=0)
    price_resource3 = models.IntegerField(default=0)
    price_resource4 = models.IntegerField(default=0)
    price_mineral1 = models.IntegerField(default=0)
    price_mineral2 = models.IntegerField(default=0)
    price_mineral3 = models.IntegerField(default=0)
    price_mineral4 = models.IntegerField(default=0)
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


class BasicHull(models.Model):
    class Meta:
        db_table = 'basic_hull'
        verbose_name = u'Корпус'
        verbose_name_plural = u'Корпуса'

    hull_name = models.CharField(max_length=50, verbose_name=u'Название')
    description = models.CharField(max_length=500, verbose_name=u'Описание')
    hull_health = models.IntegerField(verbose_name=u'Количество здоровья')
    generator = models.IntegerField(verbose_name=u'Количество герераторов')
    engine = models.IntegerField(verbose_name=u'Количество двигателей')
    weapon = models.IntegerField(verbose_name=u'Количество оружия')
    armor = models.IntegerField(verbose_name=u'Количество брони')
    shield = models.IntegerField(verbose_name=u'Количество щитов')
    module = models.IntegerField(verbose_name=u'Количество модулей')
    main_weapon = models.IntegerField(verbose_name=u'Количество главного калибра')
    hold_size = models.IntegerField(verbose_name=u'Размер трюма')
    fuel_tank = models.IntegerField(default=0, verbose_name=u'Размер топливного бака')
    hull_mass = models.IntegerField(verbose_name=u'Масса')
    hull_size = models.IntegerField(verbose_name=u'Размер')
    power_consuption = models.IntegerField(verbose_name=u'Потребление энергии')
    price_internal_currency = models.IntegerField(default=25, verbose_name=u'Цена в валюте')
    price_resource1 = models.IntegerField(default=0, verbose_name=u'Цена в никеле')
    price_resource2 = models.IntegerField(default=0, verbose_name=u'Цена в железе')
    price_resource3 = models.IntegerField(default=0, verbose_name=u'Цена в меди')
    price_resource4 = models.IntegerField(default=0, verbose_name=u'Цена в алюминии')
    price_mineral1 = models.IntegerField(default=0, verbose_name=u'Цена в вариатите')
    price_mineral2 = models.IntegerField(default=0, verbose_name=u'Цена в иннэилите')
    price_mineral3 = models.IntegerField(default=0, verbose_name=u'Цена в ренниите')
    price_mineral4 = models.IntegerField(default=0, verbose_name=u'Цена в кобальте')
    min_all_scientic = models.IntegerField(default=0, verbose_name=u'Минимальный уровень науки')
    min_math = models.IntegerField(default=0, verbose_name=u'Минимальный уровень математики')
    min_phis = models.IntegerField(default=0, verbose_name=u'Минимальный уровень физики')
    min_biol = models.IntegerField(default=0, verbose_name=u'Минимальный уровень биологии')
    min_energy = models.IntegerField(default=0, verbose_name=u'Минимальный уровень енергетики')
    min_radio = models.IntegerField(default=0, verbose_name=u'Минимальный уровень електротехники')
    min_nanotech = models.IntegerField(default=0, verbose_name=u'Минимальный уровень нанотехнологий')
    min_astronomy = models.IntegerField(default=0, verbose_name=u'Минимальный уровень астрономии')
    min_logist = models.IntegerField(default=0, verbose_name=u'Минимальный уровень логистики')

    def __unicode__(self):
        return self.hull_name


class HullPattern(models.Model):
    class Meta:
        db_table = 'hull_pattern'

    user = models.ForeignKey(MyUser, db_index=True)
    basic_hull = models.ForeignKey(BasicHull)
    hull_name = models.CharField(max_length=50, default="New hull")
    hull_health = models.IntegerField()
    generator = models.IntegerField()
    engine = models.IntegerField()
    weapon = models.IntegerField()
    armor = models.IntegerField()
    shield = models.IntegerField()
    module = models.IntegerField(default=3)
    main_weapon = models.IntegerField()
    hold_size = models.IntegerField()
    fuel_tank = models.IntegerField(default=100)
    hull_mass = models.IntegerField()
    hull_size = models.IntegerField()
    power_consuption = models.IntegerField()
    price_internal_currency = models.IntegerField(default=25)
    price_resource1 = models.IntegerField(default=0)
    price_resource2 = models.IntegerField(default=0)
    price_resource3 = models.IntegerField(default=0)
    price_resource4 = models.IntegerField(default=0)
    price_mineral1 = models.IntegerField(default=0)
    price_mineral2 = models.IntegerField(default=0)
    price_mineral3 = models.IntegerField(default=0)
    price_mineral4 = models.IntegerField(default=0)
    bought_template = models.BooleanField(default=False)


class BasicEngine(models.Model):
    class Meta:
        db_table = 'basic_engine'
        verbose_name = u'Двигатель'
        verbose_name_plural = u'Двигатели'

    engine_name = models.CharField(max_length=50, verbose_name=u'Название')
    description = models.CharField(max_length=500, verbose_name=u'Описание')
    engine_health = models.IntegerField(verbose_name=u'Количество здоровья')
    system_power = models.IntegerField(verbose_name=u'Системная мощьность')
    intersystem_power = models.IntegerField(verbose_name=u'Межсистемная мощьность')
    giper_power = models.IntegerField(verbose_name=u'Гиперпространственная мощьность')
    nullT_power = models.IntegerField(verbose_name=u'Нуль-Т мощьность')
    engine_mass = models.IntegerField(verbose_name=u'Масса')
    engine_size = models.IntegerField(verbose_name=u'Размер')
    power_consuption = models.IntegerField(verbose_name=u'Потребление энергии')
    price_internal_currency = models.IntegerField(default=25, verbose_name=u'Цена в валюте')
    price_resource1 = models.IntegerField(default=0, verbose_name=u'Цена в никеле')
    price_resource2 = models.IntegerField(default=0, verbose_name=u'Цена в железе')
    price_resource3 = models.IntegerField(default=0, verbose_name=u'Цена в меди')
    price_resource4 = models.IntegerField(default=0, verbose_name=u'Цена в алюминии')
    price_mineral1 = models.IntegerField(default=0, verbose_name=u'Цена в вариатите')
    price_mineral2 = models.IntegerField(default=0, verbose_name=u'Цена в иннэилите')
    price_mineral3 = models.IntegerField(default=0, verbose_name=u'Цена в ренниите')
    price_mineral4 = models.IntegerField(default=0, verbose_name=u'Цена в кобальте')
    min_all_scientic = models.IntegerField(default=0, verbose_name=u'Минимальный уровень науки')
    min_math = models.IntegerField(default=0, verbose_name=u'Минимальный уровень математики')
    min_phis = models.IntegerField(default=0, verbose_name=u'Минимальный уровень физики')
    min_biol = models.IntegerField(default=0, verbose_name=u'Минимальный уровень биологии')
    min_energy = models.IntegerField(default=0, verbose_name=u'Минимальный уровень енергетики')
    min_radio = models.IntegerField(default=0, verbose_name=u'Минимальный уровень електротехники')
    min_nanotech = models.IntegerField(default=0, verbose_name=u'Минимальный уровень нанотехнологий')
    min_astronomy = models.IntegerField(default=0, verbose_name=u'Минимальный уровень астрономии')
    min_logist = models.IntegerField(default=0, verbose_name=u'Минимальный уровень логистики')

    def __unicode__(self):
        return self.engine_name


class EnginePattern(models.Model):
    class Meta:
        db_table = 'engine_pattern'

    user = models.ForeignKey(MyUser, db_index=True)
    basic_engine = models.IntegerField()
    engine_name = models.CharField(max_length=50, default='New engine')
    engine_health = models.FloatField()
    system_power = models.FloatField()
    intersystem_power = models.FloatField()
    giper_power = models.FloatField()
    nullT_power = models.FloatField()
    engine_mass = models.FloatField()
    engine_size = models.FloatField()
    power_consuption = models.FloatField()
    price_internal_currency = models.IntegerField(default=25)
    price_resource1 = models.IntegerField(default=0)
    price_resource2 = models.IntegerField(default=0)
    price_resource3 = models.IntegerField(default=0)
    price_resource4 = models.IntegerField(default=0)
    price_mineral1 = models.IntegerField(default=0)
    price_mineral2 = models.IntegerField(default=0)
    price_mineral3 = models.IntegerField(default=0)
    price_mineral4 = models.IntegerField(default=0)
    bought_template = models.BooleanField(default=False)


class BasicGenerator(models.Model):
    class Meta:
        db_table = 'basic_generator'
        verbose_name = u'Генератор'
        verbose_name_plural = u'Генераторы'

    generator_name = models.CharField(max_length=50, verbose_name=u'Название')
    description = models.CharField(max_length=500, verbose_name=u'Описание')
    generator_health = models.IntegerField(verbose_name=u'Количество жизни')
    produced_energy = models.IntegerField(verbose_name=u'Вырабатываемая энергия')
    fuel_necessary = models.IntegerField(verbose_name=u'Потребление топлива')
    generator_mass = models.IntegerField(verbose_name=u'Масса')
    generator_size = models.IntegerField(verbose_name=u'Размер')
    price_internal_currency = models.IntegerField(default=25, verbose_name=u'Цена в валюте')
    price_resource1 = models.IntegerField(default=0, verbose_name=u'Цена в никеле')
    price_resource2 = models.IntegerField(default=0, verbose_name=u'Цена в железе')
    price_resource3 = models.IntegerField(default=0, verbose_name=u'Цена в меди')
    price_resource4 = models.IntegerField(default=0, verbose_name=u'Цена в алюминии')
    price_mineral1 = models.IntegerField(default=0, verbose_name=u'Цена в вариатите')
    price_mineral2 = models.IntegerField(default=0, verbose_name=u'Цена в иннэилите')
    price_mineral3 = models.IntegerField(default=0, verbose_name=u'Цена в ренниите')
    price_mineral4 = models.IntegerField(default=0, verbose_name=u'Цена в кобальте')
    min_all_scientic = models.IntegerField(default=0, verbose_name=u'Минимальный уровень науки')
    min_math = models.IntegerField(default=0, verbose_name=u'Минимальный уровень математики')
    min_phis = models.IntegerField(default=0, verbose_name=u'Минимальный уровень физики')
    min_biol = models.IntegerField(default=0, verbose_name=u'Минимальный уровень биологии')
    min_energy = models.IntegerField(default=0, verbose_name=u'Минимальный уровень енергетики')
    min_radio = models.IntegerField(default=0, verbose_name=u'Минимальный уровень електротехники')
    min_nanotech = models.IntegerField(default=0, verbose_name=u'Минимальный уровень нанотехнологий')
    min_astronomy = models.IntegerField(default=0, verbose_name=u'Минимальный уровень астрономии')
    min_logist = models.IntegerField(default=0, verbose_name=u'Минимальный уровень логистики')

    def __unicode__(self):
        return self.generator_name


class GeneratorPattern(models.Model):
    class Meta:
        db_table = 'generator_pattern'

    user = models.ForeignKey(MyUser, db_index=True)
    basic_generator = models.ForeignKey(BasicGenerator)
    generator_name = models.CharField(max_length=50, default='New generator')
    generator_health = models.FloatField()
    produced_energy = models.FloatField()
    fuel_necessary = models.FloatField()
    generator_mass = models.FloatField()
    generator_size = models.FloatField()
    price_internal_currency = models.IntegerField(default=25)
    price_resource1 = models.IntegerField(default=0)
    price_resource2 = models.IntegerField(default=0)
    price_resource3 = models.IntegerField(default=0)
    price_resource4 = models.IntegerField(default=0)
    price_mineral1 = models.IntegerField(default=0)
    price_mineral2 = models.IntegerField(default=0)
    price_mineral3 = models.IntegerField(default=0)
    price_mineral4 = models.IntegerField(default=0)
    bought_template = models.BooleanField(default=False)


class BasicShield(models.Model):
    class Meta:
        db_table = 'basic_shield'
        verbose_name = u'Щит'
        verbose_name_plural = u'Щиты'

    shield_name = models.CharField(max_length=50, verbose_name=u'Название')
    description = models.CharField(max_length=500, verbose_name=u'Описание')
    shield_health = models.IntegerField(verbose_name=u'Количество жизни')
    value_energy_resistance = models.IntegerField(verbose_name=u'Отражение энергитического урона')
    value_phisical_resistance = models.IntegerField(verbose_name=u'Отражение физического урона')
    shield_regeneration = models.IntegerField(verbose_name=u'Востановление')
    number_of_emitter = models.IntegerField(verbose_name=u'Количество эмиттеров')
    shield_mass = models.IntegerField(verbose_name=u'Масса')
    shield_size = models.IntegerField(verbose_name=u'Размер')
    power_consuption = models.IntegerField(verbose_name=u'Потребление энергии')
    price_internal_currency = models.IntegerField(default=25, verbose_name=u'Цена в валюте')
    price_resource1 = models.IntegerField(default=0, verbose_name=u'Цена в никеле')
    price_resource2 = models.IntegerField(default=0, verbose_name=u'Цена в железе')
    price_resource3 = models.IntegerField(default=0, verbose_name=u'Цена в меди')
    price_resource4 = models.IntegerField(default=0, verbose_name=u'Цена в алюминии')
    price_mineral1 = models.IntegerField(default=0, verbose_name=u'Цена в вариатите')
    price_mineral2 = models.IntegerField(default=0, verbose_name=u'Цена в иннэилите')
    price_mineral3 = models.IntegerField(default=0, verbose_name=u'Цена в ренниите')
    price_mineral4 = models.IntegerField(default=0, verbose_name=u'Цена в кобальте')
    min_all_scientic = models.IntegerField(default=0, verbose_name=u'Минимальный уровень науки')
    min_math = models.IntegerField(default=0, verbose_name=u'Минимальный уровень математики')
    min_phis = models.IntegerField(default=0, verbose_name=u'Минимальный уровень физики')
    min_biol = models.IntegerField(default=0, verbose_name=u'Минимальный уровень биологии')
    min_energy = models.IntegerField(default=0, verbose_name=u'Минимальный уровень енергетики')
    min_radio = models.IntegerField(default=0, verbose_name=u'Минимальный уровень електротехники')
    min_nanotech = models.IntegerField(default=0, verbose_name=u'Минимальный уровень нанотехнологий')
    min_astronomy = models.IntegerField(default=0, verbose_name=u'Минимальный уровень астрономии')
    min_logist = models.IntegerField(default=0, verbose_name=u'Минимальный уровень логистики')

    def __unicode__(self):
        return self.shield_name


class ShieldPattern(models.Model):
    class Meta:
        db_table = 'shield_pattern'

    user = models.ForeignKey(MyUser, db_index=True)
    basic_shield = models.ForeignKey(BasicShield)
    shield_name = models.CharField(max_length=50, default='New shield')
    shield_health = models.FloatField()
    value_energy_resistance = models.FloatField()
    value_phisical_resistance = models.FloatField()
    shield_regeneration = models.FloatField()
    number_of_emitter = models.FloatField()
    shield_mass = models.FloatField()
    shield_size = models.FloatField()
    power_consuption = models.FloatField()
    price_internal_currency = models.IntegerField(default=25)
    price_resource1 = models.IntegerField(default=0)
    price_resource2 = models.IntegerField(default=0)
    price_resource3 = models.IntegerField(default=0)
    price_resource4 = models.IntegerField(default=0)
    price_mineral1 = models.IntegerField(default=0)
    price_mineral2 = models.IntegerField(default=0)
    price_mineral3 = models.IntegerField(default=0)
    price_mineral4 = models.IntegerField(default=0)
    bought_template = models.BooleanField(default=False)


class BasicWeapon(models.Model):
    class Meta:
        db_table = 'basic_weapon'
        verbose_name = u'Оружие'
        verbose_name_plural = u'Оружие'

    weapon_name = models.CharField(max_length=50, verbose_name=u'Название')
    description = models.CharField(max_length=500, verbose_name=u'Описание')
    weapon_health = models.IntegerField(verbose_name=u'Количество жизни')
    weapon_energy_damage = models.IntegerField(verbose_name=u'Энергетический урон')
    weapon_regenerations = models.IntegerField(verbose_name=u'Время перезарядки')
    number_of_bursts = models.IntegerField(verbose_name=u'Количество залпов')
    weapon_range = models.IntegerField(verbose_name=u'Дальность')
    weapon_accuracy = models.IntegerField(verbose_name=u'Точность')
    weapon_mass = models.IntegerField(verbose_name=u'Масса')
    weapon_size = models.IntegerField(verbose_name=u'Размер')
    power_consuption = models.IntegerField(verbose_name=u'Потребление энергии')
    weapon_class = models.IntegerField(default=1, verbose_name=u'Класс оружия')
    price_internal_currency = models.IntegerField(default=25, verbose_name=u'Цена в валюте')
    price_resource1 = models.IntegerField(default=0, verbose_name=u'Цена в никеле')
    price_resource2 = models.IntegerField(default=0, verbose_name=u'Цена в железе')
    price_resource3 = models.IntegerField(default=0, verbose_name=u'Цена в меди')
    price_resource4 = models.IntegerField(default=0, verbose_name=u'Цена в алюминии')
    price_mineral1 = models.IntegerField(default=0, verbose_name=u'Цена в вариатите')
    price_mineral2 = models.IntegerField(default=0, verbose_name=u'Цена в иннэилите')
    price_mineral3 = models.IntegerField(default=0, verbose_name=u'Цена в ренниите')
    price_mineral4 = models.IntegerField(default=0, verbose_name=u'Цена в кобальте')
    min_all_scientic = models.IntegerField(default=0, verbose_name=u'Минимальный уровень науки')
    min_math = models.IntegerField(default=0, verbose_name=u'Минимальный уровень математики')
    min_phis = models.IntegerField(default=0, verbose_name=u'Минимальный уровень физики')
    min_biol = models.IntegerField(default=0, verbose_name=u'Минимальный уровень биологии')
    min_energy = models.IntegerField(default=0, verbose_name=u'Минимальный уровень енергетики')
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
    basic_weapon = models.ForeignKey(BasicWeapon)
    weapon_name = models.CharField(max_length=50, default='New weapon')
    weapon_health = models.IntegerField()
    weapon_energy_damage = models.IntegerField()
    weapon_regenerations = models.IntegerField()
    number_of_bursts = models.IntegerField()
    weapon_range = models.IntegerField()
    weapon_accuracy = models.IntegerField()
    weapon_mass = models.IntegerField()
    weapon_size = models.IntegerField()
    power_consuption = models.IntegerField()
    weapon_class = models.IntegerField(default=1)
    price_internal_currency = models.IntegerField(default=25)
    price_resource1 = models.IntegerField(default=0)
    price_resource2 = models.IntegerField(default=0)
    price_resource3 = models.IntegerField(default=0)
    price_resource4 = models.IntegerField(default=0)
    price_mineral1 = models.IntegerField(default=0)
    price_mineral2 = models.IntegerField(default=0)
    price_mineral3 = models.IntegerField(default=0)
    price_mineral4 = models.IntegerField(default=0)
    bought_template = models.BooleanField(default=False)


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
    price_resource1 = models.IntegerField(default=0, verbose_name=u'Цена в никеле')
    price_resource2 = models.IntegerField(default=0, verbose_name=u'Цена в железе')
    price_resource3 = models.IntegerField(default=0, verbose_name=u'Цена в меди')
    price_resource4 = models.IntegerField(default=0, verbose_name=u'Цена в алюминии')
    price_mineral1 = models.IntegerField(default=0, verbose_name=u'Цена в вариатите')
    price_mineral2 = models.IntegerField(default=0, verbose_name=u'Цена в иннэилите')
    price_mineral3 = models.IntegerField(default=0, verbose_name=u'Цена в ренниите')
    price_mineral4 = models.IntegerField(default=0, verbose_name=u'Цена в кобальте')
    min_all_scientic = models.IntegerField(default=0, verbose_name=u'Минимальный уровень науки')
    min_math = models.IntegerField(default=0, verbose_name=u'Минимальный уровень математики')
    min_phis = models.IntegerField(default=0, verbose_name=u'Минимальный уровень физики')
    min_biol = models.IntegerField(default=0, verbose_name=u'Минимальный уровень биологии')
    min_energy = models.IntegerField(default=0, verbose_name=u'Минимальный уровень енергетики')
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
    basic_armor = models.ForeignKey(BasicArmor)
    armor_name = models.CharField(max_length=50, default='New armor')
    armor_health = models.FloatField()
    value_energy_resistance = models.FloatField()
    value_phisical_resistance = models.FloatField()
    armor_power = models.FloatField()
    armor_regeneration = models.FloatField()
    armor_mass = models.FloatField()
    price_internal_currency = models.IntegerField(default=25)
    price_resource1 = models.IntegerField(default=0)
    price_resource2 = models.IntegerField(default=0)
    price_resource3 = models.IntegerField(default=0)
    price_resource4 = models.IntegerField(default=0)
    price_mineral1 = models.IntegerField(default=0)
    price_mineral2 = models.IntegerField(default=0)
    price_mineral3 = models.IntegerField(default=0)
    price_mineral4 = models.IntegerField(default=0)
    bought_template = models.BooleanField(default=False)


class BasicShell(models.Model):
    class Meta:
        db_table = 'basic_shell'
        verbose_name = u'Боеприпас'
        verbose_name_plural = u'Боеприпасы'

    shell_name = models.CharField(max_length=50, verbose_name=u'Название')
    description = models.CharField(max_length=500, verbose_name=u'Описание')
    shell_phisical_damage = models.IntegerField(verbose_name=u'Физический урон')
    shell_speed = models.IntegerField(verbose_name=u'Скорость')
    shell_mass = models.IntegerField(verbose_name=u'Масса')
    shell_size = models.IntegerField(verbose_name=u'Размер')
    price_internal_currency = models.IntegerField(default=25, verbose_name=u'Цена в валюте')
    price_resource1 = models.IntegerField(default=0, verbose_name=u'Цена в никеле')
    price_resource2 = models.IntegerField(default=0, verbose_name=u'Цена в железе')
    price_resource3 = models.IntegerField(default=0, verbose_name=u'Цена в меди')
    price_resource4 = models.IntegerField(default=0, verbose_name=u'Цена в алюминии')
    price_mineral1 = models.IntegerField(default=0, verbose_name=u'Цена в вариатите')
    price_mineral2 = models.IntegerField(default=0, verbose_name=u'Цена в иннэилите')
    price_mineral3 = models.IntegerField(default=0, verbose_name=u'Цена в ренниите')
    price_mineral4 = models.IntegerField(default=0, verbose_name=u'Цена в кобальте')
    min_all_scientic = models.IntegerField(default=0, verbose_name=u'Минимальный уровень науки')
    min_math = models.IntegerField(default=0, verbose_name=u'Минимальный уровень математики')
    min_phis = models.IntegerField(default=0, verbose_name=u'Минимальный уровень физики')
    min_biol = models.IntegerField(default=0, verbose_name=u'Минимальный уровень биологии')
    min_energy = models.IntegerField(default=0, verbose_name=u'Минимальный уровень енергетики')
    min_radio = models.IntegerField(default=0, verbose_name=u'Минимальный уровень електротехники')
    min_nanotech = models.IntegerField(default=0, verbose_name=u'Минимальный уровень нанотехнологий')
    min_astronomy = models.IntegerField(default=0, verbose_name=u'Минимальный уровень астрономии')
    min_logist = models.IntegerField(default=0, verbose_name=u'Минимальный уровень логистики')

    def __unicode__(self):
        return self.shell_name


class ShellPattern(models.Model):
    class Meta:
        db_table = 'shell_pattern'

    user = models.ForeignKey(MyUser, db_index=True)
    basic_shell = models.ForeignKey(BasicShell)
    shell_name = models.CharField(max_length=50, default='New shell')
    shell_phisical_damage = models.FloatField()
    shell_speed = models.FloatField()
    shell_mass = models.FloatField()
    shell_size = models.FloatField()
    price_internal_currency = models.IntegerField(default=25)
    price_resource1 = models.IntegerField(default=0)
    price_resource2 = models.IntegerField(default=0)
    price_resource3 = models.IntegerField(default=0)
    price_resource4 = models.IntegerField(default=0)
    price_mineral1 = models.IntegerField(default=0)
    price_mineral2 = models.IntegerField(default=0)
    price_mineral3 = models.IntegerField(default=0)
    price_mineral4 = models.IntegerField(default=0)
    bought_template = models.BooleanField(default=False)


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
    price_resource1 = models.IntegerField(default=0, verbose_name=u'Цена в никеле')
    price_resource2 = models.IntegerField(default=0, verbose_name=u'Цена в железе')
    price_resource3 = models.IntegerField(default=0, verbose_name=u'Цена в меди')
    price_resource4 = models.IntegerField(default=0, verbose_name=u'Цена в алюминии')
    price_mineral1 = models.IntegerField(default=0, verbose_name=u'Цена в вариатите')
    price_mineral2 = models.IntegerField(default=0, verbose_name=u'Цена в иннэилите')
    price_mineral3 = models.IntegerField(default=0, verbose_name=u'Цена в ренниите')
    price_mineral4 = models.IntegerField(default=0, verbose_name=u'Цена в кобальте')
    min_all_scientic = models.IntegerField(default=0, verbose_name=u'Минимальный уровень науки')
    min_math = models.IntegerField(default=0, verbose_name=u'Минимальный уровень математики')
    min_phis = models.IntegerField(default=0, verbose_name=u'Минимальный уровень физики')
    min_biol = models.IntegerField(default=0, verbose_name=u'Минимальный уровень биологии')
    min_energy = models.IntegerField(default=0, verbose_name=u'Минимальный уровень енергетики')
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
    price_resource1 = models.IntegerField(default=0)
    price_resource2 = models.IntegerField(default=0)
    price_resource3 = models.IntegerField(default=0)
    price_resource4 = models.IntegerField(default=0)
    price_mineral1 = models.IntegerField(default=0)
    price_mineral2 = models.IntegerField(default=0)
    price_mineral3 = models.IntegerField(default=0)
    price_mineral4 = models.IntegerField(default=0)
    bought_template = models.BooleanField(default=False)


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
    price_resource1 = models.IntegerField(default=0, verbose_name=u'Цена в никеле')
    price_resource2 = models.IntegerField(default=0, verbose_name=u'Цена в железе')
    price_resource3 = models.IntegerField(default=0, verbose_name=u'Цена в меди')
    price_resource4 = models.IntegerField(default=0, verbose_name=u'Цена в алюминии')
    price_mineral1 = models.IntegerField(default=0, verbose_name=u'Цена в вариатите')
    price_mineral2 = models.IntegerField(default=0, verbose_name=u'Цена в иннэилите')
    price_mineral3 = models.IntegerField(default=0, verbose_name=u'Цена в ренниите')
    price_mineral4 = models.IntegerField(default=0, verbose_name=u'Цена в кобальте')

    def __unicode__(self):
        return self.fuel_name


class FuelPattern(models.Model):
    class Meta:
        db_table = 'fuel_pattern'

    user = models.IntegerField(db_index=True, default=2)
    fuel_name = models.CharField(max_length=50)
    basic_fuel = models.ForeignKey(BasicFuel)
    fuel_mass = models.IntegerField()
    fuel_size = models.IntegerField()
    fuel_efficiency = models.IntegerField()
    fuel_class = models.IntegerField()
    fuel_id = models.IntegerField(default=0)
    price_internal_currency = models.IntegerField(default=25, verbose_name=u'Цена в валюте')
    price_resource1 = models.IntegerField(default=0, verbose_name=u'Цена в никеле')
    price_resource2 = models.IntegerField(default=0, verbose_name=u'Цена в железе')
    price_resource3 = models.IntegerField(default=0, verbose_name=u'Цена в меди')
    price_resource4 = models.IntegerField(default=0, verbose_name=u'Цена в алюминии')
    price_mineral1 = models.IntegerField(default=0, verbose_name=u'Цена в вариатите')
    price_mineral2 = models.IntegerField(default=0, verbose_name=u'Цена в иннэилите')
    price_mineral3 = models.IntegerField(default=0, verbose_name=u'Цена в ренниите')
    price_mineral4 = models.IntegerField(default=0, verbose_name=u'Цена в кобальте')

    def __unicode__(self):
        return self.fuel_name


class BasicDevice(models.Model):
    class Meta:
        db_table = 'basic_device'
        verbose_name = u'Устройство'
        verbose_name_plural = u'Устройства'

    device_name = models.CharField(max_length=50, verbose_name=u'Название')
    description = models.CharField(max_length=500, verbose_name=u'Описание')
    device_health = models.IntegerField(verbose_name=u'Количество жизни')
    param1 = models.IntegerField(verbose_name=u'Параметр 1')
    param2 = models.IntegerField(verbose_name=u'Параметр 2')
    param3 = models.IntegerField(verbose_name=u'Параметр 3')
    device_mass = models.IntegerField(verbose_name=u'Масса')
    device_size = models.IntegerField(verbose_name=u'Размер')
    power_consuption = models.IntegerField(verbose_name=u'Потребление энергии')
    device_class = models.IntegerField(verbose_name=u'Класс устройства')
    price_internal_currency = models.IntegerField(default=25, verbose_name=u'Цена в валюте')
    price_resource1 = models.IntegerField(default=0, verbose_name=u'Цена в никеле')
    price_resource2 = models.IntegerField(default=0, verbose_name=u'Цена в железе')
    price_resource3 = models.IntegerField(default=0, verbose_name=u'Цена в меди')
    price_resource4 = models.IntegerField(default=0, verbose_name=u'Цена в алюминии')
    price_mineral1 = models.IntegerField(default=0, verbose_name=u'Цена в вариатите')
    price_mineral2 = models.IntegerField(default=0, verbose_name=u'Цена в иннэилите')
    price_mineral3 = models.IntegerField(default=0, verbose_name=u'Цена в ренниите')
    price_mineral4 = models.IntegerField(default=0, verbose_name=u'Цена в кобальте')
    min_all_scientic = models.IntegerField(default=0, verbose_name=u'Минимальный уровень науки')
    min_math = models.IntegerField(default=0, verbose_name=u'Минимальный уровень математики')
    min_phis = models.IntegerField(default=0, verbose_name=u'Минимальный уровень физики')
    min_biol = models.IntegerField(default=0, verbose_name=u'Минимальный уровень биологии')
    min_energy = models.IntegerField(default=0, verbose_name=u'Минимальный уровень енергетики')
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
    price_resource1 = models.IntegerField(default=0)
    price_resource2 = models.IntegerField(default=0)
    price_resource3 = models.IntegerField(default=0)
    price_resource4 = models.IntegerField(default=0)
    price_mineral1 = models.IntegerField(default=0)
    price_mineral2 = models.IntegerField(default=0)
    price_mineral3 = models.IntegerField(default=0)
    price_mineral4 = models.IntegerField(default=0)
    bought_template = models.BooleanField(default=False)


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
    price_resource1 = models.IntegerField(default=0, verbose_name=u'Цена в никеле')
    price_resource2 = models.IntegerField(default=0, verbose_name=u'Цена в железе')
    price_resource3 = models.IntegerField(default=0, verbose_name=u'Цена в меди')
    price_resource4 = models.IntegerField(default=0, verbose_name=u'Цена в алюминии')
    price_mineral1 = models.IntegerField(default=0, verbose_name=u'Цена в вариатите')
    price_mineral2 = models.IntegerField(default=0, verbose_name=u'Цена в иннэилите')
    price_mineral3 = models.IntegerField(default=0, verbose_name=u'Цена в ренниите')
    price_mineral4 = models.IntegerField(default=0, verbose_name=u'Цена в кобальте')
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
    price_internal_currency = models.IntegerField(default=25)
    price_resource1 = models.IntegerField(default=0)
    price_resource2 = models.IntegerField(default=0)
    price_resource3 = models.IntegerField(default=0)
    price_resource4 = models.IntegerField(default=0)
    price_mineral1 = models.IntegerField(default=0)
    price_mineral2 = models.IntegerField(default=0)
    price_mineral3 = models.IntegerField(default=0)
    price_mineral4 = models.IntegerField(default=0)
    cost_expert_deployment = models.IntegerField(default=10)
    assembly_workpiece = models.IntegerField(default=10)
    time_deployment = models.IntegerField()
    building_size = models.IntegerField()
    building_mass = models.IntegerField()
    power_consumption = models.IntegerField(default=0)


class ManufacturingComplex(models.Model):
    class Meta:
        db_table = 'manufacturing_complex'

    user = models.ForeignKey(MyUser, db_index=True)
    user_city = models.ForeignKey(UserCity, db_index=True)
    name = models.CharField(max_length=50, default='New complex')
    extraction_parametr = models.IntegerField(default=0)


class FactoryInstalled(models.Model):
    class Meta:
        db_table = 'factory_installed'

    user = models.ForeignKey(MyUser, db_index=True)
    user_city = models.ForeignKey(UserCity, db_index=True)
    factory_pattern = models.ForeignKey(FactoryPattern)
    complex_status = models.BooleanField(default=0)
    complex = models.ForeignKey(ManufacturingComplex, null=True, default=None)


class BuildingInstalled(models.Model):
    class Meta:
        db_table = 'building_installed'

    user = models.ForeignKey(MyUser, db_index=True)
    user_city = models.ForeignKey(UserCity, db_index=True)
    building_pattern = models.ForeignKey(BuildingPattern)


class WarehouseFactoryResource(models.Model):
    class Meta:
        db_table = 'warehouse_factory_resource'

    factory = models.ForeignKey(FactoryInstalled, db_index=True)
    resource = models.ForeignKey(BasicResource)
    amount = models.IntegerField()


class WarehouseComplex(models.Model):
    class Meta:
        db_table = 'warehouse_complex'

    complex = models.ForeignKey(ManufacturingComplex)
    resource_id = models.IntegerField()
    amount = models.IntegerField()


class WarehouseFactory(models.Model):
    class Meta:
        db_table = 'warehouse_factory'

    user = models.ForeignKey(MyUser, db_index=True)
    user_city = models.ForeignKey(UserCity, db_index=True)
    factory = models.ForeignKey(FactoryPattern, db_index=True)
    amount = models.IntegerField(default=0)


class WarehouseBuilding(models.Model):
    class Meta:
        db_table = 'warehouse_building'

    user = models.ForeignKey(MyUser, db_index=True)
    user_city = models.ForeignKey(UserCity, db_index=True)
    factory = models.ForeignKey(BuildingPattern, db_index=True)
    amount = models.IntegerField(default=0)


class WarehouseElement(models.Model):
    class Meta:
        db_table = 'warehouse_element'

    user = models.ForeignKey(MyUser, db_index=True)
    user_city = models.ForeignKey(UserCity, db_index=True)
    element_class = models.IntegerField(default=1, db_index=True)
    element_id = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)


class TurnBuilding(models.Model):
    class Meta:
        db_table = 'turn_building'

    user = models.ForeignKey(MyUser, db_index=True)
    user_city = models.ForeignKey(UserCity, db_index=True)
    factory = models.IntegerField(default=0)
    class_id = models.IntegerField(default=0)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    z = models.IntegerField(default=0)
    start_time_deployment = models.DateTimeField()
    finish_time_deployment = models.DateTimeField()


class TurnScientic(models.Model):
    class Meta:
        db_table = 'turn_scientic'

    user = models.ForeignKey(MyUser, db_index=True)
    mathematics_up = models.IntegerField(default=0)
    phisics_up = models.IntegerField(default=0)
    biologic_chimics_up = models.IntegerField(default=0)
    energetics_up = models.IntegerField(default=0)
    radionics_up = models.IntegerField(default=0)
    nanotech_up = models.IntegerField(default=0)
    astronomy_up = models.IntegerField(default=0)
    logistic_up = models.IntegerField(default=0)
    start_time_science = models.DateTimeField()
    finish_time_science = models.DateTimeField()


class TurnProduction(models.Model):
    class Meta:
        db_table = 'turn_production'

    user = models.ForeignKey(MyUser, db_index=True)
    user_city = models.ForeignKey(UserCity, db_index=True)
    factory = models.ForeignKey(FactoryInstalled)
    element_id = models.IntegerField()
    amount_element = models.IntegerField(default=1)
    start_time_production = models.DateTimeField()
    finish_time_production = models.DateTimeField()


class TurnComplexProduction(models.Model):
    class Meta:
        db_table = 'turn_complex_production'

    complex = models.ForeignKey(ManufacturingComplex)
    factory = models.ForeignKey(FactoryInstalled)
    element_id = models.IntegerField()
    start_time_production = models.DateTimeField()
    time = models.IntegerField()


class TurnAssemblyPieces(models.Model):
    class Meta:
        db_table = 'turn_assembly_pieces'

    user = models.ForeignKey(MyUser, db_index=True)
    user_city = models.ForeignKey(UserCity, db_index=True)
    pattern = models.ForeignKey(FactoryPattern)
    class_id = models.IntegerField(default=0)
    amount_assembly = models.IntegerField(default=0)
    start_time_assembly = models.DateTimeField()
    finish_time_assembly = models.DateTimeField()


class ProjectShip(models.Model):
    class Meta:
        db_table = 'project_ship'

    user = models.ForeignKey(MyUser, db_index=True)
    project_name = models.CharField(max_length=32)
    hull_id = models.IntegerField()
    system_power = models.IntegerField(default=0)
    system_fuel = models.IntegerField(default=0)
    intersystem_power = models.IntegerField(default=0)
    intersystem_fuel = models.IntegerField(default=0)
    giper_power = models.IntegerField(default=0)
    giper_energy = models.IntegerField(default=0)
    giper_accuracy = models.FloatField(default=0.9)
    null_power = models.IntegerField(default=0)
    null_energy = models.IntegerField(default=0)
    null_accuracy = models.FloatField(default=0.9)
    generator_fuel = models.IntegerField(default=0)
    generator_energy = models.IntegerField(default=0)
    maneuverability = models.FloatField(default=0)
    time_build = models.IntegerField(default=0)
    ship_mass = models.IntegerField(default=500)


class ElementShip(models.Model):
    class Meta:
        db_table = 'element_ship'

    project_ship = models.ForeignKey(ProjectShip, db_index=True)
    class_element = models.IntegerField(db_index=True)
    element_pattern_id = models.IntegerField()
    position = models.IntegerField()
    element_health = models.IntegerField()


class Ship(models.Model):
    class Meta:
        db_table = 'ship'

    user = models.ForeignKey(MyUser, db_index=True)
    project_ship = models.ForeignKey(ProjectShip, db_index=True)
    ship_name = models.CharField(max_length=32, default='New ship')
    amount_ship = models.IntegerField()
    fleet_status = models.BooleanField(default=0)
    place_id = models.IntegerField()


class WarehouseShip(models.Model):
    class Meta:
        db_table = 'warehouse_ship'

    user = models.ForeignKey(MyUser, db_index=True)
    user_city = models.ForeignKey(UserCity, db_index=True)
    ship = models.ForeignKey(Ship)
    amount = models.IntegerField(default=0)


class FleetEngine(models.Model):
    class Meta:
        db_table = 'fleet_engine'

    system_power = models.IntegerField(default=0)
    intersystem_power = models.IntegerField(default=0)
    giper_power = models.IntegerField(default=0)
    giper_accuracy = models.FloatField(default=0)
    null_power = models.IntegerField(default=0)
    null_accuracy = models.FloatField(default=0)
    maneuverability = models.FloatField(default=0)


class FleetEnergyPower(models.Model):
    class Meta:
        db_table = 'fleet_energy_power'

    use_energy = models.IntegerField(default=0)
    use_fuel_system = models.IntegerField(default=0)
    use_fuel_intersystem = models.IntegerField(default=0)
    use_energy_giper = models.IntegerField(default=0)
    use_energy_null = models.IntegerField(default=0)
    produce_energy = models.IntegerField(default=0)
    use_fuel_generator = models.IntegerField(default=0)


class Fleet(models.Model):
    class Meta:
        db_table = 'fleet'

    user = models.ForeignKey(MyUser, db_index=True)
    fleet_name = models.CharField(max_length=20)
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    system = models.IntegerField(default=0)
    planet = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    planet_status = models.BooleanField(default=1)
    fleet_hold = models.IntegerField(default=0)
    empty_hold = models.IntegerField(default=0)
    ship_empty_mass = models.IntegerField(default=0)
    fuel_tank = models.IntegerField(default=0)
    free_fuel_tank = models.IntegerField(default=0)
    fleet_engine = models.ForeignKey(FleetEngine, null=True, default=None)
    fleet_energy_power = models.ForeignKey(FleetEnergyPower, null=True, default=None)


class FleetParametrScan(models.Model):
    class Meta:
        db_table = 'fleet_parametr_scan'

    fleet = models.ForeignKey(Fleet, db_index=True)
    method_scanning = models.IntegerField(default=0)
    time_scanning = models.IntegerField(default=0)
    range_scanning = models.IntegerField(default=0)


class FleetParametrResourceExtraction(models.Model):
    class Meta:
        db_table = 'fleet_parametr_resource_extraction'

    fleet = models.ForeignKey(Fleet, db_index=True)
    extraction_per_minute = models.IntegerField(default=0)


class FleetParametrBuildRepair(models.Model):
    class Meta:
        db_table = 'fleet_parametr_build_repair'

    fleet = models.ForeignKey(Fleet, db_index=True)
    class_process = models.IntegerField()
    process_per_minute = models.IntegerField()


class Hold(models.Model):
    class Meta:
        db_table = 'fleet_hold'

    fleet = models.ForeignKey(Fleet, db_index=True)
    class_shipment = models.IntegerField()
    shipment_id = models.IntegerField()
    amount_shipment = models.IntegerField()
    mass_shipment = models.IntegerField()
    size_shipment = models.IntegerField()


class FuelTank(models.Model):
    class Meta:
        db_table = 'fuel_tank'

    fleet = models.ForeignKey(Fleet, db_index=True)
    fuel_class = models.IntegerField()
    fuel_id = models.IntegerField(default=1)
    amount_fuel = models.IntegerField()
    mass_fuel = models.IntegerField()
    size_fuel = models.IntegerField()


class DamageShip(models.Model):
    class Meta:
        db_table = 'damage_ship'

    user = models.ForeignKey(MyUser, db_index=True)
    fleet = models.ForeignKey(Fleet)
    project_ship = models.ForeignKey(ProjectShip)


class DamageElement(models.Model):
    class Meta:
        db_table = 'damage_element'

    damage_ship = models.ForeignKey(DamageShip, db_index=True)
    element_id = models.IntegerField()
    health = models.IntegerField()


class TurnShipBuild(models.Model):
    class Meta:
        db_table = 'turn_ship_build'

    user = models.ForeignKey(MyUser, db_index=True)
    user_city = models.ForeignKey(UserCity, db_index=True)
    process_id = models.IntegerField(default=0)
    project_ship = models.ForeignKey(ProjectShip)
    start_time_build = models.DateTimeField()
    finish_time_build = models.DateTimeField()


class Flightplan(models.Model):
    class Meta:
        db_table = 'flightplan'

    user = models.ForeignKey(MyUser, db_index=True)
    fleet = models.ForeignKey(Fleet, db_index=True)
    class_command = models.IntegerField()
    command_id = models.IntegerField()
    status = models.IntegerField()


class FlightplanFlight(models.Model):
    class Meta:
        db_table = 'flightplan_flight'

    user = models.ForeignKey(MyUser, db_index=True)
    fleet = models.ForeignKey(Fleet, db_index=True)
    flightplan = models.ForeignKey(Flightplan)
    command_id = models.IntegerField()
    start_x = models.IntegerField()
    start_y = models.IntegerField()
    start_z = models.IntegerField()
    finish_x = models.IntegerField()
    finish_y = models.IntegerField()
    finish_z = models.IntegerField()
    system_flight = models.BooleanField(default=True)
    flight_time = models.IntegerField(default=0)
    start_time = models.DateTimeField(default=timezone.now, blank=True)
    system = models.IntegerField(default=0)
    planet = models.IntegerField(default=0)


class FlightplanHold(models.Model):
    class Meta:
        db_table = 'flightplan_hold'

    user = models.ForeignKey(MyUser, db_index=True)
    fleet = models.ForeignKey(Fleet, db_index=True)
    flightplan = models.ForeignKey(Flightplan)
    command_id = models.IntegerField()
    class_element = models.IntegerField(default=0)
    element_id = models.IntegerField(default=0)
    amount = models.IntegerField()
    start_time = models.DateTimeField(default=timezone.now, blank=True)
    time = models.IntegerField(default=0)
    name = models.CharField(max_length=50, default='')


class FlightplanProduction(models.Model):
    class Meta:
        db_table = 'flightplan_production'

    user = models.ForeignKey(MyUser, db_index=True)
    fleet = models.ForeignKey(Fleet, db_index=True)
    flightplan = models.ForeignKey(Flightplan)
    command = models.IntegerField()
    production_per_minute = models.IntegerField()
    start_time = models.DateTimeField(default=timezone.now, blank=True)
    time_extraction = models.IntegerField(default=0)


class FlightplanRefill(models.Model):
    class Meta:
        db_table = 'flightplan_refill'

    user = models.ForeignKey(MyUser, db_index=True)
    fleet = models.ForeignKey(Fleet, db_index=True)
    flightplan = models.ForeignKey(Flightplan)
    command = models.IntegerField()
    fleet_refill_id = models.IntegerField()
    class_refill = models.IntegerField(default=0)
    class_element = models.IntegerField(default=0)
    element_id = models.IntegerField(default=0)
    amount = models.IntegerField()
    start_time = models.DateTimeField(default=timezone.now, blank=True)
    time_refill = models.IntegerField(default=0)
    name = models.CharField(max_length=50, default='')


class FlightplanBuildRepair(models.Model):
    class Meta:
        db_table = 'flightplan_build_repair'

    fleet = models.ForeignKey(Fleet, db_index=True)
    flightplan = models.ForeignKey(Flightplan)
    command_id = models.IntegerField()
    fleet_repair_id = models.IntegerField()
    start_time = models.DateTimeField(default=timezone.now, blank=True)
    time = models.IntegerField(default=0)


class FlightplanScan(models.Model):
    class Meta:
        db_table = 'flightplan_scan'

    user = models.ForeignKey(MyUser, db_index=True)
    fleet = models.ForeignKey(Fleet, db_index=True)
    flightplan = models.ForeignKey(Flightplan)
    command_id = models.IntegerField()
    range_scanning = models.IntegerField()
    start_time = models.DateTimeField(default=timezone.now, blank=True)
    time_scanning = models.IntegerField(default=0)


class FlightplanColonization(models.Model):
    class Meta:
        db_table = 'flightplan_colonization'

    fleet = models.ForeignKey(Fleet, db_index=True)
    flightplan = models.ForeignKey(Flightplan)
    command_id = models.IntegerField()
    start_time = models.DateTimeField(default=timezone.now, blank=True)
    time = models.IntegerField()


class FlightplanFight(models.Model):
    class Meta:
        db_table = 'flightplan_fight'

    user = models.ForeignKey(MyUser, db_index=True)
    fleet = models.ForeignKey(Fleet, db_index=True)
    flightplan = models.ForeignKey(Flightplan)
    command_id = models.IntegerField()
    fleet_attack_id = models.IntegerField()
    fight_id = models.IntegerField()


class AsteroidField(models.Model):
    class Meta:
        db_table = 'asteroid_field'

    x = models.IntegerField(db_index=True)
    y = models.IntegerField(db_index=True)
    z = models.IntegerField(db_index=True)
    class_asteroid_field = models.IntegerField(default=0)
    size = models.IntegerField()
    koef_res_1 = models.FloatField(default=0.15)
    koef_res_2 = models.FloatField(default=0.15)
    koef_res_3 = models.FloatField(default=0.15)
    koef_res_4 = models.FloatField(default=0.15)
    koef_min_1 = models.FloatField(default=0.05)
    koef_min_2 = models.FloatField(default=0.05)
    koef_min_3 = models.FloatField(default=0.05)
    koef_min_4 = models.FloatField(default=0.05)
    artifact = models.IntegerField()


class TradeSpace(models.Model):
    class Meta:
        db_table = 'trade_space'

    name = models.CharField(max_length=64)
    user = models.ForeignKey(MyUser, db_index=True)
    password = models.CharField(max_length=64)
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


class Chat(models.Model):
    class Meta:
        db_table = 'chat'

    user = models.CharField(max_length=32)
    user_id = models.IntegerField(db_index=True, default=1)
    text = models.CharField(max_length=64)
    time = models.DateTimeField(default=datetime.now, blank=True)


class ChatPrivate(models.Model):
    class Meta:
        db_table = 'chat_private'

    user_id = models.IntegerField(default=1)
    user = models.CharField(max_length=20)
    recipient = models.IntegerField()
    recipient_name = models.CharField(max_length=20)
    text = models.CharField(max_length=64)


class UserChatOnline(models.Model):
    class Meta:
        db_table = 'user_chat_online'

    user_id = models.IntegerField(db_index=True)
    user = models.CharField(max_length=20)
    last_time_update = models.DateTimeField()
