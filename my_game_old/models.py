# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from datetime import datetime


class MyUser(models.Model):
    class Meta:
        db_table = 'my_user'
        verbose_name = u'Пользователь'
        verbose_name_plural = u'Пользователи'

    user_id = models.IntegerField(db_index=True)
    user_name = models.CharField(db_index=True, max_length=20, unique=True, verbose_name=u'Имя игрока')
    password = models.CharField(max_length=50)
    race_id = models.IntegerField(verbose_name=u'Раса')
    alliance_id = models.IntegerField(default=0)
    union_id = models.IntegerField(default=0)
    internal_currency = models.IntegerField(default=0, verbose_name=u'Внутренняя валюта')
    foreigh_currency = models.IntegerField(default=0, verbose_name=u'Внешняя валюта')
    real_currency = models.IntegerField(default=0, verbose_name=u'Реальная валюта')
    e_mail = models.CharField(db_index=True, max_length=50, unique=True, verbose_name=u'Почта')
    referal_code = models.CharField(max_length=50)
    user_luckyness = models.IntegerField()
    last_time_check = models.DateTimeField()
    last_time_scan_scient = models.DateTimeField()
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

    galaxy = models.ForeignKey(Galaxy)
    x = models.IntegerField(db_index=True)
    y = models.IntegerField(db_index=True)
    z = models.IntegerField(db_index=True)
    system_type = models.IntegerField()
    system_size = models.FloatField()
    star_size = models.FloatField()


class Planet(models.Model):
    class Meta:
        db_table = 'planet'

    system = models.ForeignKey(System)
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

    description = models.CharField(max_length=500)
    gravity = models.CharField(max_length=20)
    atmosphere = models.CharField(max_length=20)


class Warehouse(models.Model):
    class Meta:
        db_table = 'warehouse'

    user = models.IntegerField(db_index=True)
    user_city = models.IntegerField(db_index=True, default=0)
    id_resource = models.IntegerField(default=0)
    amount = models.IntegerField(default=125000)


class UserCity(models.Model):
    class Meta:
        db_table = 'user_city'

    user = models.IntegerField(db_index=True)
    system = models.ForeignKey(System, db_index=True)
    planet = models.ForeignKey(Planet, db_index=True)
    x = models.IntegerField()
    y = models.IntegerField()
    z = models.IntegerField()
    name_city = models.CharField(db_index=True, max_length=20, default='New City')
    city_size_free = models.IntegerField()
    population = models.IntegerField(default=150)
    max_population = models.IntegerField(default=500)
    founding_date = models.DateTimeField()
    extraction_date = models.DateTimeField()
    power = models.IntegerField(default=0)
    use_energy = models.IntegerField(default=0)


class Race(models.Model):
    class Meta:
        db_table = 'race'
        verbose_name = u'Раса'
        verbose_name_plural = u'Расы'

    name = models.CharField(max_length=50, default='Race', verbose_name=u'Название')
    description = models.CharField(max_length=4096, verbose_name=u'Описание')
    engine_system = models.FloatField()
    engine_intersystem = models.FloatField()
    engine_giper = models.FloatField()
    engine_null = models.FloatField()
    generator = models.FloatField()
    armor = models.FloatField()
    shield = models.FloatField()
    weapon_attack = models.FloatField()
    weapon_defense = models.FloatField()
    exploration = models.FloatField()
    disguse = models.FloatField()
    auximilary = models.FloatField()
    image_ig = models.IntegerField()


class BasicScientic(models.Model):
    class Meta:
        db_table = 'basic_scientic'
        verbose_name = u'Базовая наука'
        verbose_name_plural = u'Базовая наука'

    scientic_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=4096)
    time_study = models.IntegerField()
    cost_internal_currency = models.IntegerField(default=25)
    cost_resource1 = models.IntegerField(default=10)
    cost_resource2 = models.IntegerField(default=20)
    cost_resource3 = models.IntegerField(default=20)
    cost_resource4 = models.IntegerField(default=10)
    cost_mineral1 = models.IntegerField(default=5)
    cost_mineral2 = models.IntegerField(default=3)
    cost_mineral3 = models.IntegerField(default=2)
    cost_mineral4 = models.IntegerField(default=5)

    def __unicode__(self):
        return self.description


class BasicFactory(models.Model):
    class Meta:
        db_table = 'basic_factory'
        verbose_name = u'Базовое производство'
        verbose_name_plural = u'Базовые производства'

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
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
    time_production = models.IntegerField()
    size = models.IntegerField()
    mass = models.IntegerField()
    power_consumption = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name


class BasicHull(models.Model):
    class Meta:
        db_table = 'basic_hull'

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    health = models.IntegerField()
    generator = models.IntegerField()
    engine = models.IntegerField()
    weapon = models.IntegerField()
    armor = models.IntegerField()
    shield = models.IntegerField()
    module = models.IntegerField()
    main_weapon = models.IntegerField()
    hold_size = models.IntegerField()
    fuel_tank = models.IntegerField(default=0)
    mass = models.IntegerField()
    size = models.IntegerField()
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
    min_all_scientic = models.IntegerField(default=0)
    min_math = models.IntegerField(default=0)
    min_phis = models.IntegerField(default=0)
    min_biol = models.IntegerField(default=0)
    min_energy = models.IntegerField(default=0)
    min_radio = models.IntegerField(default=0)
    min_nanotech = models.IntegerField(default=0)
    min_astronomy = models.IntegerField(default=0)
    min_logist = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name


class BasicEngine(models.Model):
    class Meta:
        db_table = 'basic_engine'

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    health = models.IntegerField()
    system_power = models.IntegerField()
    intersystem_power = models.IntegerField()
    giper_power = models.IntegerField()
    nullT_power = models.IntegerField()
    mass = models.IntegerField()
    size = models.IntegerField()
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
    min_all_scientic = models.IntegerField(default=0)
    min_math = models.IntegerField(default=0)
    min_phis = models.IntegerField(default=0)
    min_biol = models.IntegerField(default=0)
    min_energy = models.IntegerField(default=0)
    min_radio = models.IntegerField(default=0)
    min_nanotech = models.IntegerField(default=0)
    min_astronomy = models.IntegerField(default=0)
    min_logist = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name


class BasicGenerator(models.Model):
    class Meta:
        db_table = 'basic_generator'

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    health = models.IntegerField()
    produced_energy = models.IntegerField()
    fuel_necessary = models.IntegerField()
    mass = models.IntegerField()
    size = models.IntegerField()
    price_internal_currency = models.IntegerField(default=25)
    price_resource1 = models.IntegerField(default=0)
    price_resource2 = models.IntegerField(default=0)
    price_resource3 = models.IntegerField(default=0)
    price_resource4 = models.IntegerField(default=0)
    price_mineral1 = models.IntegerField(default=0)
    price_mineral2 = models.IntegerField(default=0)
    price_mineral3 = models.IntegerField(default=0)
    price_mineral4 = models.IntegerField(default=0)
    min_all_scientic = models.IntegerField(default=0)
    min_math = models.IntegerField(default=0)
    min_phis = models.IntegerField(default=0)
    min_biol = models.IntegerField(default=0)
    min_energy = models.IntegerField(default=0)
    min_radio = models.IntegerField(default=0)
    min_nanotech = models.IntegerField(default=0)
    min_astronomy = models.IntegerField(default=0)
    min_logist = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name


class BasicShield(models.Model):
    class Meta:
        db_table = 'basic_shield'

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    health = models.IntegerField()
    value_energy_resistance = models.IntegerField()
    value_phisical_resistance = models.IntegerField()
    regeneration = models.IntegerField()
    number_of_emitter = models.IntegerField()
    mass = models.IntegerField()
    size = models.IntegerField()
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
    min_all_scientic = models.IntegerField(default=0)
    min_math = models.IntegerField(default=0)
    min_phis = models.IntegerField(default=0)
    min_biol = models.IntegerField(default=0)
    min_energy = models.IntegerField(default=0)
    min_radio = models.IntegerField(default=0)
    min_nanotech = models.IntegerField(default=0)
    min_astronomy = models.IntegerField(default=0)
    min_logist = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name


class BasicWeapon(models.Model):
    class Meta:
        db_table = 'basic_weapon'

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    health = models.IntegerField()
    energy_damage = models.IntegerField()
    regenerations = models.IntegerField()
    number_of_bursts = models.IntegerField()
    range = models.IntegerField()
    accuracy = models.IntegerField()
    mass = models.IntegerField()
    size = models.IntegerField()
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
    min_all_scientic = models.IntegerField(default=0)
    min_math = models.IntegerField(default=0)
    min_phis = models.IntegerField(default=0)
    min_biol = models.IntegerField(default=0)
    min_energy = models.IntegerField(default=0)
    min_radio = models.IntegerField(default=0)
    min_nanotech = models.IntegerField(default=0)
    min_astronomy = models.IntegerField(default=0)
    min_logist = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name


class BasicArmor(models.Model):
    class Meta:
        db_table = 'basic_armor'

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    health = models.IntegerField()
    value_energy_resistance = models.IntegerField()
    value_phisical_resistance = models.IntegerField()
    power = models.IntegerField()
    regeneration = models.IntegerField()
    mass = models.IntegerField()
    price_internal_currency = models.IntegerField(default=25)
    price_resource1 = models.IntegerField(default=0)
    price_resource2 = models.IntegerField(default=0)
    price_resource3 = models.IntegerField(default=0)
    price_resource4 = models.IntegerField(default=0)
    price_mineral1 = models.IntegerField(default=0)
    price_mineral2 = models.IntegerField(default=0)
    price_mineral3 = models.IntegerField(default=0)
    price_mineral4 = models.IntegerField(default=0)
    min_all_scientic = models.IntegerField(default=0)
    min_math = models.IntegerField(default=0)
    min_phis = models.IntegerField(default=0)
    min_biol = models.IntegerField(default=0)
    min_energy = models.IntegerField(default=0)
    min_radio = models.IntegerField(default=0)
    min_nanotech = models.IntegerField(default=0)
    min_astronomy = models.IntegerField(default=0)
    min_logist = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name


class BasicShell(models.Model):
    class Meta:
        db_table = 'basic_shell'

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    phisical_damage = models.IntegerField()
    speed = models.IntegerField()
    mass = models.IntegerField()
    size = models.IntegerField()
    price_internal_currency = models.IntegerField(default=25)
    price_resource1 = models.IntegerField(default=0)
    price_resource2 = models.IntegerField(default=0)
    price_resource3 = models.IntegerField(default=0)
    price_resource4 = models.IntegerField(default=0)
    price_mineral1 = models.IntegerField(default=0)
    price_mineral2 = models.IntegerField(default=0)
    price_mineral3 = models.IntegerField(default=0)
    price_mineral4 = models.IntegerField(default=0)
    min_all_scientic = models.IntegerField(default=0)
    min_math = models.IntegerField(default=0)
    min_phis = models.IntegerField(default=0)
    min_biol = models.IntegerField(default=0)
    min_energy = models.IntegerField(default=0)
    min_radio = models.IntegerField(default=0)
    min_nanotech = models.IntegerField(default=0)
    min_astronomy = models.IntegerField(default=0)
    min_logist = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name


class BasicModule(models.Model):
    class Meta:
        db_table = 'basic_module'

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    health = models.IntegerField()
    param1 = models.IntegerField()
    param2 = models.IntegerField()
    param3 = models.IntegerField()
    mass = models.IntegerField()
    size = models.IntegerField()
    power_consuption = models.IntegerField()
    module_class = models.IntegerField()
    price_internal_currency = models.IntegerField(default=25)
    price_resource1 = models.IntegerField(default=0)
    price_resource2 = models.IntegerField(default=0)
    price_resource3 = models.IntegerField(default=0)
    price_resource4 = models.IntegerField(default=0)
    price_mineral1 = models.IntegerField(default=0)
    price_mineral2 = models.IntegerField(default=0)
    price_mineral3 = models.IntegerField(default=0)
    price_mineral4 = models.IntegerField(default=0)
    min_all_scientic = models.IntegerField(default=0)
    min_math = models.IntegerField(default=0)
    min_phis = models.IntegerField(default=0)
    min_biol = models.IntegerField(default=0)
    min_energy = models.IntegerField(default=0)
    min_radio = models.IntegerField(default=0)
    min_nanotech = models.IntegerField(default=0)
    min_astronomy = models.IntegerField(default=0)
    min_logist = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name


class BasicFuel(models.Model):
    class Meta:
        db_table = 'basic_fuel'

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    mass = models.IntegerField()
    size = models.IntegerField()
    efficiency = models.IntegerField()
    fuel_class = models.IntegerField()
    fuel_id = models.IntegerField(default=0)
    price_internal_currency = models.IntegerField(default=25)
    price_resource1 = models.IntegerField(default=0)
    price_resource2 = models.IntegerField(default=0)
    price_resource3 = models.IntegerField(default=0)
    price_resource4 = models.IntegerField(default=0)
    price_mineral1 = models.IntegerField(default=0)
    price_mineral2 = models.IntegerField(default=0)
    price_mineral3 = models.IntegerField(default=0)
    price_mineral4 = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name


class BasicDevice(models.Model):
    class Meta:
        db_table = 'basic_device'

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    health = models.IntegerField()
    param1 = models.IntegerField()
    param2 = models.IntegerField()
    param3 = models.IntegerField()
    mass = models.IntegerField()
    size = models.IntegerField()
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
    min_all_scientic = models.IntegerField(default=0)
    min_math = models.IntegerField(default=0)
    min_phis = models.IntegerField(default=0)
    min_biol = models.IntegerField(default=0)
    min_energy = models.IntegerField(default=0)
    min_radio = models.IntegerField(default=0)
    min_nanotech = models.IntegerField(default=0)
    min_astronomy = models.IntegerField(default=0)
    min_logist = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name


class FactoryPattern(models.Model):
    class Meta:
        db_table = 'factory_pattern'

    user = models.IntegerField(db_index=True)
    basic_id = models.IntegerField()
    name = models.CharField(max_length=50, default='New factory')
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
    size = models.IntegerField()
    mass = models.IntegerField()
    power_consumption = models.IntegerField(default=0)
    bought_template = models.BooleanField(default=False)


class HullPattern(models.Model):
    class Meta:
        db_table = 'hull_pattern'

    user = models.IntegerField(db_index=True)
    basic_id = models.IntegerField()
    name = models.CharField(max_length=50, default="New hull")
    health = models.IntegerField()
    generator = models.IntegerField()
    engine = models.IntegerField()
    weapon = models.IntegerField()
    armor = models.IntegerField()
    shield = models.IntegerField()
    module = models.IntegerField(default=3)
    main_weapon = models.IntegerField()
    hold_size = models.IntegerField()
    fuel_tank = models.IntegerField(default=100)
    mass = models.IntegerField()
    size = models.IntegerField()
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


class EnginePattern(models.Model):
    class Meta:
        db_table = 'engine_pattern'

    user = models.IntegerField(db_index=True)
    basic_id = models.IntegerField()
    name = models.CharField(max_length=50, default='New engine')
    health = models.FloatField()
    system_power = models.FloatField()
    intersystem_power = models.FloatField()
    giper_power = models.FloatField()
    nullT_power = models.FloatField()
    mass = models.FloatField()
    size = models.FloatField()
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


class GeneratorPattern(models.Model):
    class Meta:
        db_table = 'generator_pattern'

    user = models.IntegerField(db_index=True)
    basic_id = models.IntegerField()
    name = models.CharField(max_length=50, default='New generator')
    health = models.FloatField()
    produced_energy = models.FloatField()
    fuel_necessary = models.FloatField()
    mass = models.FloatField()
    size = models.FloatField()
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


class ShieldPattern(models.Model):
    class Meta:
        db_table = 'shield_pattern'

    user = models.IntegerField(db_index=True)
    basic_id = models.IntegerField()
    name = models.CharField(max_length=50, default='New shield')
    health = models.FloatField()
    value_energy_resistance = models.FloatField()
    value_phisical_resistance = models.FloatField()
    regeneration = models.FloatField()
    number_of_emitter = models.FloatField()
    mass = models.FloatField()
    size = models.FloatField()
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


class WeaponPattern(models.Model):
    class Meta:
        db_table = 'weapon_pattern'

    user = models.IntegerField(db_index=True)
    basic_id = models.IntegerField()
    name = models.CharField(max_length=50, default='New weapon')
    health = models.IntegerField()
    energy_damage = models.IntegerField()
    regenerations = models.IntegerField()
    number_of_bursts = models.IntegerField()
    range = models.IntegerField()
    accuracy = models.IntegerField()
    mass = models.IntegerField()
    size = models.IntegerField()
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


class ArmorPattern(models.Model):
    class Meta:
        db_table = 'armor_pattern'

    user = models.IntegerField(db_index=True)
    basic_id = models.IntegerField()
    name = models.CharField(max_length=50, default='New armor')
    health = models.FloatField()
    value_energy_resistance = models.FloatField()
    value_phisical_resistance = models.FloatField()
    power = models.FloatField()
    regeneration = models.FloatField()
    mass = models.FloatField()
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


class ShellPattern(models.Model):
    class Meta:
        db_table = 'shell_pattern'

    user = models.IntegerField(db_index=True)
    basic_id = models.IntegerField()
    name = models.CharField(max_length=50, default='New shell')
    phisical_damage = models.FloatField()
    speed = models.FloatField()
    mass = models.FloatField()
    size = models.FloatField()
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


class ModulePattern(models.Model):
    class Meta:
        db_table = 'module_pattern'

    user = models.IntegerField(db_index=True)
    basic_id = models.IntegerField()
    name = models.CharField(max_length=50, default='New module')
    health = models.IntegerField()
    param1 = models.IntegerField()
    param2 = models.IntegerField()
    param3 = models.IntegerField()
    mass = models.IntegerField()
    size = models.IntegerField()
    power_consuption = models.IntegerField()
    module_class = models.IntegerField()
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


class FuelPattern(models.Model):
    class Meta:
        db_table = 'fuel_pattern'

    user = models.IntegerField(db_index=True, default=2)
    name = models.CharField(max_length=50)
    basic_id = models.IntegerField(default=0)
    mass = models.IntegerField()
    size = models.IntegerField()
    efficiency = models.IntegerField()
    fuel_class = models.IntegerField()
    fuel_id = models.IntegerField(default=0)
    price_internal_currency = models.IntegerField(default=25)
    price_resource1 = models.IntegerField(default=0)
    price_resource2 = models.IntegerField(default=0)
    price_resource3 = models.IntegerField(default=0)
    price_resource4 = models.IntegerField(default=0)
    price_mineral1 = models.IntegerField(default=0)
    price_mineral2 = models.IntegerField(default=0)
    price_mineral3 = models.IntegerField(default=0)
    price_mineral4 = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name


class DevicePattern(models.Model):
    class Meta:
        db_table = 'device_pattern'

    user = models.IntegerField(db_index=True)
    basic_id = models.IntegerField()
    name = models.CharField(max_length=50, default='New device')
    health = models.IntegerField()
    param1 = models.IntegerField()
    param2 = models.IntegerField()
    param3 = models.IntegerField()
    mass = models.IntegerField()
    size = models.IntegerField()
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


class FactoryInstalled(models.Model):
    class Meta:
        db_table = 'factory_installed'

    user = models.IntegerField(db_index=True)
    user_city = models.IntegerField(db_index=True)
    factory_pattern_id = models.IntegerField()
    name = models.CharField(max_length=50)
    time_deployment = models.IntegerField()
    production_class = models.IntegerField(db_index=True)
    production_id = models.IntegerField(db_index=True)
    time_production = models.IntegerField()
    size = models.IntegerField()
    mass = models.IntegerField()
    power_consumption = models.IntegerField(default=0)
    complex_status = models.IntegerField(default=0)
    complex_id = models.IntegerField(default=0)


class ManufacturingComplex(models.Model):
    class Meta:
        db_table = 'manufacturing_complex'

    user = models.IntegerField(db_index=True)
    user_city = models.IntegerField(db_index=True)
    name = models.CharField(max_length=50, default='New complex')
    extraction_parametr = models.IntegerField(default=0)


class WarehouseFactoryResource(models.Model):
    class Meta:
        db_table = 'warehouse_factory_resource'

    id_factory = models.IntegerField(db_index=True)
    id_resource = models.IntegerField()
    amount = models.IntegerField()


class WarehouseComplex(models.Model):
    class Meta:
        db_table = 'warehouse_complex'

    id_complex = models.IntegerField(db_index=True)
    id_resource = models.IntegerField()
    amount = models.IntegerField()


class WarehouseFactory(models.Model):
    class Meta:
        db_table = 'warehouse_factory'

    user = models.IntegerField(default=5, db_index=True)
    user_city = models.IntegerField(default=1, db_index=True)
    factory_id = models.IntegerField(default=0, db_index=True)
    production_class = models.IntegerField(default=0)
    production_id = models.IntegerField(default=0)
    time_production = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
    size = models.IntegerField(default=0)
    mass = models.IntegerField(default=0)
    power_consumption = models.IntegerField(default=0)


class WarehouseElement(models.Model):
    class Meta:
        db_table = 'warehouse_element'

    user = models.IntegerField(default=5, db_index=True)
    user_city = models.IntegerField(default=1, db_index=True)
    element_class = models.IntegerField(default=1, db_index=True)
    element_id = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)


class WarehouseShip(models.Model):
    class Meta:
        db_table = 'warehouse_ship'

    user = models.IntegerField(default=5, db_index=True)
    user_city = models.IntegerField(default=1, db_index=True)
    ship_id = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)


class UserScientic(models.Model):
    class Meta:
        db_table = 'user_scientic'

    user = models.IntegerField(db_index=True)
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


class TurnBuilding(models.Model):
    class Meta:
        db_table = 'turn_building'

    user = models.IntegerField(db_index=True)
    user_city = models.IntegerField(default=0, db_index=True)
    factory_id = models.IntegerField(default=0)
    class_id = models.IntegerField(default=0)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    z = models.IntegerField(default=0)
    start_time_deployment = models.DateTimeField()
    finish_time_deployment = models.DateTimeField()


class TurnScientic(models.Model):
    class Meta:
        db_table = 'turn_scientic'

    user = models.IntegerField(db_index=True)
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

    user = models.IntegerField(db_index=True)
    user_city = models.IntegerField(db_index=True)
    factory_id = models.IntegerField()
    element_id = models.IntegerField()
    amount_element = models.IntegerField(default=1)
    start_time_production = models.DateTimeField()
    finish_time_production = models.DateTimeField()


class TurnComplexProduction(models.Model):
    class Meta:
        db_table = 'turn_complex_production'

    complex_id = models.IntegerField(db_index=True)
    factory_id = models.IntegerField()
    element_id = models.IntegerField()
    start_time_production = models.DateTimeField()
    time = models.IntegerField()


class TurnAssemblyPieces(models.Model):
    class Meta:
        db_table = 'turn_assembly_pieces'

    user = models.IntegerField(db_index=True)
    user_city = models.IntegerField(db_index=True)
    pattern_id = models.IntegerField()
    class_id = models.IntegerField(default=0)
    amount_assembly = models.IntegerField(default=0)
    start_time_assembly = models.DateTimeField()
    finish_time_assembly = models.DateTimeField()


class ProjectShip(models.Model):
    class Meta:
        db_table = 'project_ship'

    user = models.IntegerField(db_index=True)
    name = models.CharField(max_length=20)
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
    mass = models.IntegerField(default=500)


class ElementShip(models.Model):
    class Meta:
        db_table = 'element_ship'

    id_project_ship = models.IntegerField(db_index=True)
    class_element = models.IntegerField(db_index=True)
    id_element_pattern = models.IntegerField()
    position = models.IntegerField()
    health = models.IntegerField()


class Ship(models.Model):
    class Meta:
        db_table = 'ship'

    user = models.IntegerField(db_index=True)
    id_project_ship = models.IntegerField(db_index=True)
    name = models.CharField(max_length=20, default='New ship')
    amount_ship = models.IntegerField()
    fleet_status = models.BooleanField(default=0)
    place_id = models.IntegerField()


class DamageShip(models.Model):
    class Meta:
        db_table = 'damage_ship'

    user = models.IntegerField(db_index=True)
    id_fleet = models.IntegerField()
    id_project = models.IntegerField()


class DamageElement(models.Model):
    class Meta:
        db_table = 'damage_element'

    id_damage_ship = models.IntegerField(db_index=True)
    id_element = models.IntegerField()
    health = models.IntegerField()


class Fleet(models.Model):
    class Meta:
        db_table = 'fleet'

    user = models.IntegerField(db_index=True)
    name = models.CharField(max_length=20)
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    system = models.IntegerField(default=0)
    planet = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    planet_status = models.BooleanField(default=1)
    hold = models.IntegerField(default=0)
    empty_hold = models.IntegerField(default=0)
    ship_empty_mass = models.IntegerField(default=0)
    fuel_tank = models.IntegerField(default=0)
    free_fuel_tank = models.IntegerField(default=0)


class FleetEngine(models.Model):
    class Meta:
        db_table = 'fleet_engine'

    fleet_id = models.IntegerField(db_index=True)
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

    fleet_id = models.IntegerField(db_index=True)
    use_energy = models.IntegerField(default=0)
    use_fuel_system = models.IntegerField(default=0)
    use_fuel_intersystem = models.IntegerField(default=0)
    use_energy_giper = models.IntegerField(default=0)
    use_energy_null = models.IntegerField(default=0)
    produce_energy = models.IntegerField(default=0)
    use_fuel_generator = models.IntegerField(default=0)


class FleetParametrScan(models.Model):
    class Meta:
        db_table = 'fleet_parametr_scan'

    fleet_id = models.IntegerField(db_index=True)
    method_scanning = models.IntegerField(default=0)
    time_scanning = models.IntegerField(default=0)
    range_scanning = models.IntegerField(default=0)


class FleetParametrResourceExtraction(models.Model):
    class Meta:
        db_table = 'fleet_parametr_resource_extraction'

    fleet_id = models.IntegerField()
    extraction_per_minute = models.IntegerField(default=0)


class FleetParametrBuildRepair(models.Model):
    class Meta:
        db_table = 'fleet_parametr_build_repair'

    fleet_id = models.IntegerField()
    class_process = models.IntegerField()
    process_per_minute = models.IntegerField()


class Hold(models.Model):
    class Meta:
        db_table = 'hold'

    fleet_id = models.IntegerField(db_index=True)
    class_shipment = models.IntegerField()
    id_shipment = models.IntegerField()
    amount_shipment = models.IntegerField()
    mass_shipment = models.IntegerField()
    size_shipment = models.IntegerField()


class FuelTank(models.Model):
    class Meta:
        db_table = 'fuel_tank'

    fleet_id = models.IntegerField(db_index=True)
    fuel_class = models.IntegerField()
    fuel_id = models.IntegerField(default=1)
    amount_fuel = models.IntegerField()
    mass_fuel = models.IntegerField()
    size_fuel = models.IntegerField()


class TurnShipBuild(models.Model):
    class Meta:
        db_table = 'turn_ship_build'

    user = models.IntegerField(db_index=True)
    user_city = models.IntegerField()
    process_id = models.IntegerField(default=0)
    ship_pattern = models.IntegerField()
    amount = models.IntegerField()
    start_time_build = models.DateTimeField()
    finish_time_build = models.DateTimeField()


class UserVariables(models.Model):
    class Meta:
        db_table = 'user_variables'

    registr_internal_currency = models.IntegerField()
    registr_resource1 = models.IntegerField()
    registr_resource2 = models.IntegerField()
    registr_resource3 = models.IntegerField()
    registr_resource4 = models.IntegerField()
    registr_mineral1 = models.IntegerField()
    registr_mineral2 = models.IntegerField()
    registr_mineral3 = models.IntegerField()
    registr_mineral4 = models.IntegerField()
    basic_time_build_ship = models.IntegerField()
    koef_ship_element_time = models.FloatField()
    minimum_scan_time = models.IntegerField()
    max_turn_assembly_pieces_basic = models.IntegerField()
    max_turn_assembly_pieces_premium = models.IntegerField()
    max_turn_building_basic = models.IntegerField()
    max_turn_building_premium = models.IntegerField()
    max_turn_production_basic = models.IntegerField()
    max_turn_production_premium = models.IntegerField()
    max_turn_scientic_basic = models.IntegerField()
    max_turn_scientic_premium = models.IntegerField()
    max_turn_ship_build_basic = models.IntegerField()
    max_turn_ship_build_premium = models.IntegerField()
    time_check_new_technology = models.IntegerField()
    min_scientic_level = models.IntegerField()
    tax_per_person = models.FloatField()
    koef_price_increace_modern_element = models.FloatField()


class Flightplan(models.Model):
    class Meta:
        db_table = 'flightplan'

    user = models.IntegerField(db_index=True)
    id_fleet = models.IntegerField(db_index=True)
    class_command = models.IntegerField()
    id_command = models.IntegerField()
    status = models.IntegerField()


class FlightplanFlight(models.Model):
    class Meta:
        db_table = 'flightplan_flight'

    user = models.IntegerField(db_index=True)
    id_fleet = models.IntegerField(db_index=True)
    id_fleetplan = models.IntegerField(default=0)
    id_command = models.IntegerField()
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

    user = models.IntegerField(db_index=True)
    id_fleet = models.IntegerField(db_index=True)
    id_fleetplan = models.IntegerField(default=0)
    id_command = models.IntegerField()
    class_element = models.IntegerField(default=0)
    id_element = models.IntegerField(default=0)
    amount = models.IntegerField()
    start_time = models.DateTimeField(default=timezone.now, blank=True)
    time = models.IntegerField(default=0)
    name = models.CharField(max_length=50, default='')


class FlightplanProduction(models.Model):
    class Meta:
        db_table = 'flightplan_production'

    user = models.IntegerField(db_index=True)
    id_fleet = models.IntegerField(db_index=True)
    id_fleetplan = models.IntegerField(default=0)
    id_command = models.IntegerField()
    production_per_minute = models.IntegerField()
    start_time = models.DateTimeField(default=timezone.now, blank=True)
    time_extraction = models.IntegerField(default=0)


class FlightplanRefill(models.Model):
    class Meta:
        db_table = 'flightplan_refill'

    user = models.IntegerField(db_index=True)
    id_fleet = models.IntegerField(db_index=True)
    id_fleetplan = models.IntegerField(default=0)
    id_command = models.IntegerField()
    id_fleet_refill = models.IntegerField()
    class_refill = models.IntegerField(default=0)
    class_element = models.IntegerField(default=0)
    id_element = models.IntegerField(default=0)
    amount = models.IntegerField()
    start_time = models.DateTimeField(default=timezone.now, blank=True)
    time_refill = models.IntegerField(default=0)
    name = models.CharField(max_length=50, default='')


class FlightplanBuildRepair(models.Model):
    class Meta:
        db_table = 'flightplan_build_repair'

    id_fleet = models.IntegerField(db_index=True)
    id_fleetplan = models.IntegerField(default=0)
    id_command = models.IntegerField()
    fleet_repair = models.IntegerField()
    start_time = models.DateTimeField(default=timezone.now, blank=True)
    time = models.IntegerField(default=0)


class FlightplanScan(models.Model):
    class Meta:
        db_table = 'flightplan_scan'

    user = models.IntegerField(db_index=True)
    id_fleet = models.IntegerField(db_index=True)
    id_command = models.IntegerField()
    id_fleetplan = models.IntegerField(default=0)
    range_scanning = models.IntegerField()
    start_time = models.DateTimeField(default=timezone.now, blank=True)
    time_scanning = models.IntegerField(default=0)


class FlightplanColonization(models.Model):
    class Meta:
        db_table = 'flightplan_colonization'

    id_fleet = models.IntegerField(db_index=True)
    id_command = models.IntegerField()
    id_fleetplan = models.IntegerField()
    start_time = models.DateTimeField(default=timezone.now, blank=True)
    time = models.IntegerField()


class FlightplanFight(models.Model):
    class Meta:
        db_table = 'flightplan_fight'

    user = models.IntegerField(db_index=True)
    id_fleet = models.IntegerField()
    id_fleetplan = models.IntegerField(default=0)
    id_command = models.IntegerField()
    id_fleet_attack = models.IntegerField()
    id_fight = models.IntegerField()


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


class TradeElement(models.Model):
    class Meta:
        db_table = 'trade_element'

    name = models.CharField(max_length=50)
    user = models.IntegerField(db_index=True)
    buyer = models.IntegerField(default=0)
    trade_space = models.IntegerField(default=0)
    class_element = models.IntegerField()
    id_element = models.IntegerField()
    amount = models.IntegerField()
    min_amount = models.IntegerField()
    cost = models.IntegerField(default=0)
    cost_element = models.IntegerField()
    diplomacy = models.IntegerField(default=0)
    x = models.IntegerField()
    y = models.IntegerField()
    z = models.IntegerField()
    user_city = models.IntegerField(default=1)
    planet = models.IntegerField(default=1)
    mass_element = models.IntegerField(default=0)
    size_element = models.IntegerField(default=0)


class TradeSpace(models.Model):
    class Meta:
        db_table = 'trade_space'

    name = models.CharField(max_length=50)
    user = models.IntegerField(db_index=True)
    password = models.CharField(max_length=50)
    tax = models.IntegerField()


class Mail(models.Model):
    class Meta:
        db_table = 'mail'

    user = models.IntegerField(db_index=True)
    recipient = models.IntegerField()
    time = models.DateTimeField(default=timezone.now, blank=True)
    status = models.IntegerField()
    category = models.IntegerField()
    login_recipient = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    message = models.CharField(max_length=8192)


class BasicBuilding(models.Model):
    class Meta:
        db_table = 'basic_building'

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
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
    size = models.IntegerField()
    mass = models.IntegerField()
    power_consumption = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name


class BuildingPattern(models.Model):
    class Meta:
        db_table = 'building_pattern'

    user = models.IntegerField(db_index=True)
    name = models.CharField(max_length=50)
    basic_id = models.IntegerField(default=1)
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
    size = models.IntegerField()
    mass = models.IntegerField()
    power_consumption = models.IntegerField(default=0)


class BuildingInstalled(models.Model):
    class Meta:
        db_table = 'building_installed'

    user = models.IntegerField(db_index=True)
    user_city = models.IntegerField()
    building_pattern_id = models.IntegerField()
    name = models.CharField(max_length=50)
    time_deployment = models.IntegerField()
    production_class = models.IntegerField()
    production_id = models.IntegerField()
    time_production = models.IntegerField()
    warehouse = models.IntegerField()
    max_warehouse = models.IntegerField(default=500)
    size = models.IntegerField()
    mass = models.IntegerField()
    power_consumption = models.IntegerField(default=0)


class BasicResource(models.Model):
    class Meta:
        db_table = 'basic_resource'

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)


class DeliveryQueue(models.Model):
    class Meta:
        db_table = 'delivery_queue'

    user = models.IntegerField(db_index=True)
    user_city = models.IntegerField()
    name = models.CharField(max_length=50, default='new')
    class_element = models.IntegerField()
    id_element = models.IntegerField()
    amount = models.IntegerField()
    method = models.IntegerField()
    status = models.IntegerField()
    x = models.IntegerField()
    y = models.IntegerField()
    z = models.IntegerField()
    mass_element = models.IntegerField(default=0)
    size_element = models.IntegerField(default=0)


class TradeReleport(models.Model):
    class Meta:
        db_table = 'trade_teleport'

    user = models.IntegerField(db_index=True)
    user_city = models.IntegerField()
    name = models.CharField(max_length=50, default='new')
    class_element = models.IntegerField()
    id_element = models.IntegerField()
    amount = models.IntegerField()
    start_teleport = models.DateTimeField()
    finish_teleport = models.DateTimeField()


class TradeFlight(models.Model):
    class Meta:
        db_table = 'trade_flight'

    user = models.IntegerField(db_index=True)
    user_city = models.IntegerField(db_index=True)
    id_fleet = models.IntegerField(db_index=True)
    id_flight = models.IntegerField()
    name = models.CharField(max_length=50)
    class_element = models.IntegerField()
    id_element = models.IntegerField()
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

    user = models.CharField(max_length=20)
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
