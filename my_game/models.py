from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class MyUser(models.Model):
    class Meta():
        db_table = 'my_user'

    user_id = models.IntegerField()
    user_name = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=50)
    race_id = models.IntegerField()
    alliance_id = models.IntegerField(default=0)
    union_id = models.IntegerField(default=0)
    internal_currency = models.IntegerField(default=0)
    foreigh_currency = models.IntegerField(default=0)
    real_currency = models.IntegerField(default=0)
    e_mail = models.CharField(max_length=50, unique=True)
    referal_code = models.CharField(max_length=50)
    user_luckyness = models.IntegerField()

    def __unicode__(self):
        return self.user_name


class Galaxy(models.Model):
    class Meta():
        db_table = 'galaxy'

    x = models.IntegerField()
    y = models.IntegerField()
    z = models.IntegerField()


class System(models.Model):
    class Meta():
        db_table = 'system'

    galaxy = models.ForeignKey(Galaxy)
    x = models.IntegerField()
    y = models.IntegerField()
    z = models.IntegerField()
    system_type = models.IntegerField()
    system_size = models.FloatField()
    star_size = models.FloatField()


class Planet(models.Model):
    class Meta():
        db_table = 'planet'

    system = models.ForeignKey(System)
    x = models.IntegerField()
    y = models.IntegerField()
    z = models.IntegerField()
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


class Planet_type(models.Model):
    class Meta():
        db_table = 'planet_type'

    description = models.CharField(max_length=500)
    gravity = models.CharField(max_length=20)
    atmosphere = models.CharField(max_length=20)


class Warehouse(models.Model):
    class Meta():
        db_table = 'warehouse'

    user = models.IntegerField()
    planet = models.ForeignKey(Planet)
    resource1 = models.IntegerField(default=125000)
    resource2 = models.IntegerField(default=125000)
    resource3 = models.IntegerField(default=125000)
    resource4 = models.IntegerField(default=125000)
    mineral1 = models.IntegerField(default=10000)
    mineral2 = models.IntegerField(default=10000)
    mineral3 = models.IntegerField(default=10000)
    mineral4 = models.IntegerField(default=10000)
    warehouse_hull = models.IntegerField(default=0)
    warehouse_factory_id = models.IntegerField(default=0)
    warehouse_generators_id = models.IntegerField(default=0)
    warehouse_engine_id = models.IntegerField(default=0)
    warehouse_armor_id = models.IntegerField(default=0)
    warehouse_weapons_id = models.IntegerField(default=0)
    warehouse_shell_id = models.IntegerField(default=0)
    warehouse_shield_id = models.IntegerField(default=0)
    warehouse_ship_id = models.IntegerField(default=0)


class User_city(models.Model):
    class Meta():
        db_table = 'user_city'

    user = models.IntegerField()
    system = models.ForeignKey(System)
    planet = models.ForeignKey(Planet)
    x = models.IntegerField()
    y = models.IntegerField()
    z = models.IntegerField()
    name_city = models.CharField(max_length=20, default='New Planet')
    city_size_free = models.IntegerField()
    warehouse = models.ForeignKey(Warehouse)
    population = models.IntegerField(default=150)
    max_population = models.IntegerField(default=500)
    founding_date = models.DateTimeField()
    extraction_date = models.DateTimeField()


class Race(models.Model):
    class Meta():
        db_table = 'race'

    description = models.CharField(max_length=500)
    luckyness = models.FloatField()
    engine_system = models.FloatField()
    engine_intersystem = models.FloatField()
    engine_giper = models.FloatField()
    engine_null = models.FloatField()
    generators = models.FloatField()
    armor = models.FloatField()
    shield = models.FloatField()
    weapons_attack = models.FloatField()
    weapons_defense = models.FloatField()
    exploration = models.FloatField()
    disguse = models.FloatField()
    auximilary = models.FloatField()
    image_ig = models.IntegerField()


class Basic_scientic(models.Model):
    class Meta():
        db_table = 'basic_scientic'

    scientic_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=500)
    time_study = models.IntegerField()
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


class Basic_factory(models.Model):
    class Meta():
        db_table = 'basic_factory'

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    price_resource1 = models.IntegerField(default=0)
    price_resource2 = models.IntegerField(default=0)
    price_resource3 = models.IntegerField(default=0)
    price_resource4 = models.IntegerField(default=0)
    price_mineral1 = models.IntegerField(default=0)
    price_mineral2 = models.IntegerField(default=0)
    price_mineral3 = models.IntegerField(default=0)
    price_mineral4 = models.IntegerField(default=0)
    time_deployment = models.IntegerField()
    production_class = models.IntegerField()
    production_id = models.IntegerField()
    time_production = models.IntegerField()
    amount = models.IntegerField()
    size = models.IntegerField()
    mass = models.IntegerField()

    def __unicode__(self):
        return self.name


class Basic_hull(models.Model):
    class Meta():
        db_table = 'basic_hull'

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    health = models.IntegerField()
    generators = models.IntegerField()
    engines = models.IntegerField()
    weapons = models.IntegerField()
    armor = models.IntegerField()
    shield = models.IntegerField()
    modules = models.IntegerField()
    main_weapons = models.IntegerField()
    hold_size = models.IntegerField()
    mass = models.IntegerField()
    size = models.IntegerField()
    power_consuption = models.IntegerField()
    min_all_scientic = models.IntegerField()
    min_math = models.IntegerField()
    min_nanotech = models.IntegerField()
    min_astronomy = models.IntegerField()

    def __unicode__(self):
        return self.name


class Basic_engine(models.Model):
    class Meta():
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
    min_all_scientic = models.IntegerField()
    min_phis = models.IntegerField()
    min_biol = models.IntegerField()
    min_energy = models.IntegerField()
    min_nanotech = models.IntegerField()

    def __unicode__(self):
        return self.name


class Basic_generator(models.Model):
    class Meta():
        db_table = 'basic_generator'

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    health = models.IntegerField()
    produced_energy = models.IntegerField()
    fuel_necessary = models.IntegerField()
    mass = models.IntegerField()
    size = models.IntegerField()
    min_all_scientic = models.IntegerField()
    min_energy = models.IntegerField()
    min_phis = models.IntegerField()
    min_nanotech = models.IntegerField()

    def __unicode__(self):
        return self.name


class Basic_shield(models.Model):
    class Meta():
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
    min_all_scientic = models.IntegerField()
    min_phis = models.IntegerField()
    min_energy = models.IntegerField()
    min_nanotech = models.IntegerField()

    def __unicode__(self):
        return self.name


class Basic_weapon(models.Model):
    class Meta():
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
    min_all_scientic = models.IntegerField()
    min_math = models.IntegerField()
    min_radio = models.IntegerField()
    min_nanotech = models.IntegerField()
    min_logist = models.IntegerField()

    def __unicode__(self):
        return self.name


class Basic_armor(models.Model):
    class Meta():
        db_table = 'basic_armor'

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    health = models.IntegerField()
    value_energy_resistance = models.IntegerField()
    value_phisical_resistance = models.IntegerField()
    power = models.IntegerField()
    regeneration = models.IntegerField()
    mass = models.IntegerField()
    min_all_scientic = models.IntegerField()
    min_phis = models.IntegerField()
    min_biol = models.IntegerField()
    min_logist = models.IntegerField()

    def __unicode__(self):
        return self.name


class Basic_shell(models.Model):
    class Meta():
        db_table = 'basic_shell'

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    phisical_damage = models.IntegerField()
    speed = models.IntegerField()
    mass = models.IntegerField()
    size = models.IntegerField()
    min_all_scientic = models.IntegerField()
    min_radio = models.IntegerField()
    min_astronomy = models.IntegerField()

    def __unicode__(self):
        return self.name


class Basic_module(models.Model):
    class Meta():
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
    min_all_scientic = models.IntegerField()
    min_math = models.IntegerField()
    min_biol = models.IntegerField()
    min_radio = models.IntegerField()
    min_astronomy = models.IntegerField()
    min_logist = models.IntegerField()

    def __unicode__(self):
        return self.name


class Factory_pattern(models.Model):
    class Meta():
        db_table = 'factory_pattern'

    user = models.IntegerField()
    factory = models.IntegerField()
    name = models.CharField(max_length=50, default='New factory')
    price_resource1 = models.IntegerField(default=0)
    price_resource2 = models.IntegerField(default=0)
    price_resource3 = models.IntegerField(default=0)
    price_resource4 = models.IntegerField(default=0)
    price_mineral1 = models.IntegerField(default=0)
    price_mineral2 = models.IntegerField(default=0)
    price_mineral3 = models.IntegerField(default=0)
    price_mineral4 = models.IntegerField(default=0)
    time_deployment = models.IntegerField()
    production_class = models.IntegerField()
    production_id = models.IntegerField()
    time_production = models.IntegerField()
    amount = models.IntegerField()
    size = models.IntegerField()
    mass = models.IntegerField()


class Hull_pattern(models.Model):
    class Meta():
        db_table = 'hull_pattern'

    user = models.IntegerField()
    hull = models.IntegerField()
    name = models.CharField(max_length=50, default="New hull")
    health = models.IntegerField()
    generators = models.IntegerField()
    engines = models.IntegerField()
    weapons = models.IntegerField()
    armor = models.IntegerField()
    shield = models.IntegerField()
    main_weapons = models.IntegerField()
    hold_size = models.IntegerField()
    mass = models.IntegerField()
    size = models.IntegerField()
    power_consuption = models.IntegerField()


class Engine_pattern(models.Model):
    class Meta():
        db_table = 'engine_pattern'

    user = models.IntegerField()
    engine = models.IntegerField()
    name = models.CharField(max_length=50, default='New engine')
    health = models.FloatField()
    system_power = models.FloatField()
    intersystem_power = models.FloatField()
    giper_power = models.FloatField()
    nullT_power = models.FloatField()
    mass = models.FloatField()
    size = models.FloatField()
    power_consuption = models.FloatField()


class Generator_pattern(models.Model):
    class Meta():
        db_table = 'generator_pattern'

    user = models.IntegerField()
    generator = models.IntegerField()
    name = models.CharField(max_length=50, default='New generator')
    health = models.FloatField()
    produced_energy = models.FloatField()
    fuel_necessary = models.FloatField()
    mass = models.FloatField()
    size = models.FloatField()


class Shield_pattern(models.Model):
    class Meta():
        db_table = 'shield_pattern'

    user = models.IntegerField()
    shield = models.IntegerField()
    name = models.CharField(max_length=50, default='new shield')
    health = models.FloatField()
    value_energy_resistance = models.FloatField()
    value_phisical_resistance = models.FloatField()
    regeneration = models.FloatField()
    number_of_emitter = models.FloatField()
    mass = models.FloatField()
    size = models.FloatField()
    power_consuption = models.FloatField()


class Weapon_pattern(models.Model):
    class Meta():
        db_table = 'weapon_pattern'

    user = models.IntegerField()
    weapon = models.IntegerField()
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


class Armor_pattern(models.Model):
    class Meta():
        db_table = 'armor_pattern'

    user = models.IntegerField()
    armor = models.IntegerField()
    name = models.CharField(max_length=50, default='New armor')
    health = models.FloatField()
    value_energy_resistance = models.FloatField()
    value_phisical_resistance = models.FloatField()
    power = models.FloatField()
    regeneration = models.FloatField()
    mass = models.FloatField()


class Shell_pattern(models.Model):
    class Meta():
        db_table = 'shell_pattern'

    user = models.IntegerField()
    shell = models.IntegerField()
    name = models.CharField(max_length=50, default='New shell')
    phisical_damage = models.FloatField()
    speed = models.FloatField()
    mass = models.FloatField()
    size = models.FloatField()


class Module_pattern(models.Model):
    class Meta():
        db_table = 'module_pattern'

    user = models.IntegerField()
    module = models.IntegerField()
    name = models.CharField(max_length=50, default='New module')
    health = models.IntegerField()
    param1 = models.IntegerField()
    param2 = models.IntegerField()
    param3 = models.IntegerField()
    mass = models.IntegerField()
    size = models.IntegerField()
    power_consuption = models.IntegerField()
    module_class = models.IntegerField()


class Warehouse_factory(models.Model):
    class Meta():
        db_table = 'warehouse_factory'

    factory_id = models.IntegerField()
    production_class = models.IntegerField()
    production_id = models.IntegerField()
    time_production = models.IntegerField()
    amount = models.IntegerField()
    size = models.IntegerField()
    mass = models.IntegerField()


class Warehouse_hull(models.Model):
    class Meta():
        db_table = 'warehouse_hull'

    hull_id = models.IntegerField()
    amount = models.IntegerField()


class Warehouse_generator(models.Model):
    class Meta():
        db_table = 'warehouse_generator'

    generator_id = models.IntegerField()
    amount = models.IntegerField()


class Warehouse_engine(models.Model):
    class Meta():
        db_table = 'warehouse_engine'

    engine_id = models.IntegerField()
    amount = models.IntegerField()


class Warehouse_armor(models.Model):
    class Meta():
        db_table = 'warehouse_armor'

    armor_id = models.IntegerField()
    amount = models.IntegerField()


class Warehouse_weapon(models.Model):
    class Meta():
        db_table = 'warehouse_weapon'

    weapon_id = models.IntegerField()
    amount = models.IntegerField()


class Warehouse_shell(models.Model):
    class Meta():
        db_table = 'warehouse_shell'

    shell_id = models.IntegerField()
    amount = models.IntegerField()


class Warehouse_shield(models.Model):
    class Meta():
        db_table = 'warehouse_shield'

    shield_id = models.IntegerField()
    amount = models.IntegerField()


class Warehouse_module(models.Model):
    class Meta():
        db_table = 'warehouse_module'

    module_id = models.IntegerField()
    amount = models.IntegerField()


class Warehouse_ship(models.Model):
    class Meta():
        db_table = 'warehouse_ship'

    ship_id = models.IntegerField()
    amount = models.IntegerField()


class User_scientic(models.Model):
    class Meta():
        db_table = 'user_scientic'

    user = models.IntegerField()
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


class Turn_building(models.Model):
    class Meta():
        db_table = 'turn_building'

    user = models.IntegerField()
    user_city = models.IntegerField(default=0)
    x = models.IntegerField()
    y = models.IntegerField()
    z = models.IntegerField()
    start_time_deploiment = models.DateTimeField()
    finish_time_deploiment = models.DateTimeField()


class Turn_scientic(models.Model):
    class Meta():
        db_table = 'turn_scientic'

    user = models.IntegerField()
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
