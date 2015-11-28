# -*- coding: utf-8 -*-

from django.db import models


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

    system = models.ForeignKey(System, db_index=True)
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


class PlanetType(models.Model):
    class Meta:
        db_table = 'planet_type'

    description = models.CharField(max_length=500, verbose_name=u'')
    gravity = models.CharField(max_length=20, verbose_name=u'')
    atmosphere = models.CharField(max_length=20, verbose_name=u'')


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
