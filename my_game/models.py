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
    last_time_check = models.DateTimeField()
    last_time_scan_scient = models.DateTimeField()

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
    user_city = models.IntegerField(default=0)
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
    population = models.IntegerField(default=150)
    max_population = models.IntegerField(default=500)
    founding_date = models.DateTimeField()
    extraction_date = models.DateTimeField()
    power = models.IntegerField(default=0)
    use_energy = models.IntegerField(default=0)


class Race(models.Model):
    class Meta():
        db_table = 'race'

    description = models.CharField(max_length=500)
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


class Basic_scientic(models.Model):
    class Meta():
        db_table = 'basic_scientic'

    scientic_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=500)
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


class Basic_factory(models.Model):
    class Meta():
        db_table = 'basic_factory'

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


class Basic_hull(models.Model):
    class Meta():
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


class Basic_shell(models.Model):
    class Meta():
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


class Factory_pattern(models.Model):
    class Meta():
        db_table = 'factory_pattern'

    user = models.IntegerField()
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


class Hull_pattern(models.Model):
    class Meta():
        db_table = 'hull_pattern'

    user = models.IntegerField()
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


class Engine_pattern(models.Model):
    class Meta():
        db_table = 'engine_pattern'

    user = models.IntegerField()
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


class Generator_pattern(models.Model):
    class Meta():
        db_table = 'generator_pattern'

    user = models.IntegerField()
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


class Shield_pattern(models.Model):
    class Meta():
        db_table = 'shield_pattern'

    user = models.IntegerField()
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


class Weapon_pattern(models.Model):
    class Meta():
        db_table = 'weapon_pattern'

    user = models.IntegerField()
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


class Armor_pattern(models.Model):
    class Meta():
        db_table = 'armor_pattern'

    user = models.IntegerField()
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


class Shell_pattern(models.Model):
    class Meta():
        db_table = 'shell_pattern'

    user = models.IntegerField()
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


class Module_pattern(models.Model):
    class Meta():
        db_table = 'module_pattern'

    user = models.IntegerField()
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


class Factory_installed(models.Model):
    class Meta():
        db_table = 'factory_installed'

    user = models.IntegerField()
    user_city = models.IntegerField()
    factory_pattern_id = models.IntegerField()
    name = models.CharField(max_length=50)
    time_deployment = models.IntegerField()
    production_class = models.IntegerField()
    production_id = models.IntegerField()
    time_production = models.IntegerField()
    size = models.IntegerField()
    mass = models.IntegerField()
    power_consumption = models.IntegerField(default=0)


class Warehouse_factory(models.Model):
    class Meta():
        db_table = 'warehouse_factory'

    user = models.IntegerField(default=5)
    user_city = models.IntegerField(default=1)
    factory_id = models.IntegerField(default=0)
    production_class = models.IntegerField(default=0)
    production_id = models.IntegerField(default=0)
    time_production = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
    size = models.IntegerField(default=0)
    mass = models.IntegerField(default=0)
    power_consumption = models.IntegerField(default=0)


class Warehouse_element(models.Model):
    class Meta():
        db_table = 'warehouse_element'

    user = models.IntegerField(default=5)
    user_city = models.IntegerField(default=1)
    element_class = models.IntegerField(default=1)
    element_id = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)


class Warehouse_ship(models.Model):
    class Meta():
        db_table = 'warehouse_ship'

    user = models.IntegerField(default=5)
    user_city = models.IntegerField(default=1)
    ship_id = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)


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
    factory_id = models.IntegerField(default=0)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    z = models.IntegerField(default=0)
    start_time_deployment = models.DateTimeField()
    finish_time_deployment = models.DateTimeField()


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


class Turn_production(models.Model):
    class Meta():
        db_table = 'turn_production'

    user = models.IntegerField()
    user_city = models.IntegerField()
    factory_id = models.IntegerField()
    element_id = models.IntegerField()
    amount_element = models.IntegerField(default=1)
    start_time_production = models.DateTimeField()
    finish_time_production = models.DateTimeField()


class Turn_assembly_pieces(models.Model):
    class Meta():
        db_table = 'turn_assembly_pieces'

    user = models.IntegerField()
    user_city = models.IntegerField()
    pattern_id = models.IntegerField()
    amount_assembly = models.IntegerField(default=0)
    start_time_assembly = models.DateTimeField()
    finish_time_assembly = models.DateTimeField()


class Project_ship(models.Model):
    class Meta():
        db_table = 'project_ship'

    user = models.IntegerField()
    name = models.CharField(max_length=20)
    hull_id = models.IntegerField()
    system_power = models.IntegerField(default=0)
    intersystem_power = models.IntegerField(default=0)
    giper_power = models.IntegerField(default=0)
    giper_accuracy = models.FloatField(default=0.9)
    null_power = models.IntegerField(default=0)
    null_accuracy = models.FloatField(default=0.9)
    maneuverability = models.FloatField(default=0)
    time_build = models.IntegerField(default=0)


class Element_ship(models.Model):
    class Meta():
        db_table = 'element_ship'

    id_project_ship = models.IntegerField()
    class_element = models.IntegerField()
    id_element_pattern = models.IntegerField()
    position = models.IntegerField()
    health = models.IntegerField()


class Ship(models.Model):
    class Meta():
        db_table = 'ship'

    user = models.IntegerField()
    id_project_ship = models.IntegerField()
    amount_ship = models.IntegerField()
    fleet_status = models.BooleanField(default=0)
    place_id = models.IntegerField()


class Fleet(models.Model):
    class Meta():
        db_table = 'fleet'

    user = models.IntegerField()
    name = models.CharField(max_length=20)
    x = models.IntegerField()
    y = models.IntegerField()
    z = models.IntegerField()
    status = models.IntegerField()
    system_power = models.IntegerField()
    intersystem_power = models.IntegerField()
    giper_power = models.IntegerField()
    giper_accuracy = models.FloatField(default=0.9)
    null_power = models.IntegerField()
    null_accuracy = models.FloatField(default=0.9)
    use_power_engine_system = models.IntegerField()
    use_power_engine_intersystem = models.IntegerField()
    use_power_engine_giper = models.IntegerField()
    use_power_engine_null = models.IntegerField()
    use_power_hull = models.IntegerField()
    use_power_shield = models.IntegerField()
    use_power_weapon = models.IntegerField()
    use_power_module = models.IntegerField()
    maneuverability = models.FloatField()


class Turn_ship_build(models.Model):
    class Meta():
        db_table = 'turn_ship_build'

    user = models.IntegerField()
    user_city = models.IntegerField()
    ship_pattern = models.IntegerField()
    amount = models.IntegerField()
    start_time_build = models.DateTimeField()
    finish_time_build = models.DateTimeField()


class Global_variables(models.Model):
    class Meta():
        db_table = 'global_variables'

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
