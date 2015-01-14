










class warehouse_factory(models.Model):
    class Meta():
        db_table = 'warehouse_factory'

    factory_id = models.IntegerField()
    production_class = models.IntegerField()
    production_id = models.IntegerField()
    time_production = models.IntegerField()
    amount = models.IntegerField()
    size = models.IntegerField()
    mass = models.IntegerField()


class warehouse_hull(models.Model):
    class Meta():
        db_table = 'warehouse_hull'

    hull_id = models.IntegerField()
    amount = models.IntegerField()


class warehouse_generator(models.Model):
    class Meta():
        db_table = 'warehouse_generators'

    generator_id = models.IntegerField()
    amount = models.IntegerField()


class warehouse_engine(models.Model):
    class Meta():
        db_table = 'warehouse_engine'

    engine_id = models.IntegerField()
    amount = models.IntegerField()


class warehouse_armor(models.Model):
    class Meta():
        db_table = 'warehouse_armor'

    armor_id = models.IntegerField()
    amount = models.IntegerField()


class warehouse_weapon(models.Model):
    class Meta():
        db_table = 'warehouse_weapon'

    weapon_id = models.IntegerField()
    amount = models.IntegerField()


class warehouse_shell(models.Model):
    class Meta():
        db_table = 'warehouse_shell'

    shell_id = models.IntegerField()
    amount = models.IntegerField()


class warehouse_shield(models.Model):
    class Meta():
        db_table = 'warehouse_shield'

    shield_id = models.IntegerField()
    amount = models.IntegerField()


class warehouse_module(models.Model):
    class Meta():
        db_table = 'warehouse_module'

    module_id = models.IntegerField()
    amount = models.IntegerField()


class warehouse_ship(models.Model):
    class Meta():
        db_table = 'warehouse_ship'

    ship_id = models.IntegerField()
    amount = models.IntegerField()


class turn_building(models.Model):
    class Meta():
        db_table = 'turn_building'

    user = models.ForeignKey(User)
    user_city = models.IntegerField(default=0)
    x = models.IntegerField()
    y = models.IntegerField()
    z = models.IntegerField()
    start_time_deploiment = models.DateTimeField()
    finish_time_deploiment = models.DateTimeField()


class turn_scientic(models.Model):
    class Meta():
        db_table = 'turn_scientic'

    user = models.ForeignKey(User)
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










