# -*- coding: utf-8 -*-

from django.db import models
from account_models import MyUser
from city_models import UserCity

class ManufacturingComplex(models.Model):
    class Meta:
        db_table = 'manufacturing_complex'

    user = models.ForeignKey(MyUser, db_index=True)
    user_city = models.ForeignKey(UserCity, db_index=True)
    name = models.CharField(max_length=50, default='New complex')
    warehouse_complex = models.ForeignKey(WarehouseComplex)
    extraction_parametr = models.IntegerField(default=0)


class WarehouseComplex(models.Model):
    class Meta:
        db_table = 'warehouse_complex'

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
