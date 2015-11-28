# -*- coding: utf-8 -*-

from django.db import models
from account_models import MyUser
from building_models import BuildingPattern
from factory_models import FactoryPattern
from galaxy_models import Planet, System
from ship_models import Ship


class Warehouse(models.Model):
    class Meta:
        db_table = 'warehouse'

    user = models.ForeignKey(MyUser, db_index=True)
    user_city = models.ForeignKey(UserCity, db_index=True)
    res_nickel = models.IntegerField(default=0)
    res_iron = models.IntegerField(default=0)
    res_cooper = models.IntegerField(default=0)
    res_aluminum = models.IntegerField(default=0)
    res_variarit = models.IntegerField(default=0)
    res_inneilit = models.IntegerField(default=0)
    res_renniit = models.IntegerField(default=0)
    res_cobalt = models.IntegerField(default=0)
    mat_construction_material = models.IntegerField(default=0)
    mat_chemical = models.IntegerField(default=0)
    mat_high_strength_allov = models.IntegerField(default=0)
    mat_nanoelement = models.IntegerField(default=0)
    mat_microprocessor_element = models.IntegerField(default=0)
    mat_fober_optic_element = models.IntegerField(default=0)


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
    warehouse = models.ForeignKey(Warehouse, db_index=True)


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
    building = models.ForeignKey(BuildingPattern, db_index=True)
    amount = models.IntegerField(default=0)


class WarehouseElement(models.Model):
    class Meta:
        db_table = 'warehouse_element'

    user = models.ForeignKey(MyUser, db_index=True)
    user_city = models.ForeignKey(UserCity, db_index=True)
    element_class = models.IntegerField(default=1, db_index=True)
    element_id = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)


class WarehouseShip(models.Model):
    class Meta:
        db_table = 'warehouse_ship'

    user = models.ForeignKey(MyUser, db_index=True)
    user_city = models.ForeignKey(UserCity, db_index=True)
    ship = models.ForeignKey(Ship)
    amount = models.IntegerField(default=0)
