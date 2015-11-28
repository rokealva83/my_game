# -*- coding: utf-8 -*-

from django.db import models
from my_game.models import MyUser


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

class ResourceHold(models.Model):
    res_nickel = models.IntegerField(default=0)
    res_iron = models.IntegerField(default=0)
    res_cooper = models.IntegerField(default=0)
    res_aluminum = models.IntegerField(default=0)
    res_veriarit = models.IntegerField(default=0)
    res_inneilit = models.IntegerField(default=0)
    res_renniit = models.IntegerField(default=0)
    res_cobalt = models.IntegerField(default=0)
    mat_construction_material = models.IntegerField(default=0)
    mat_chemical = models.IntegerField(default=0)
    mat_high_strength_allov = models.IntegerField(default=0)
    mat_nanoelement = models.IntegerField(default=0)
    mat_microprocessor_element = models.IntegerField(default=0)
    mat_fober_optic_element = models.IntegerField(default=0)


class Fleet(models.Model):
    class Meta:
        db_table = 'fleet'

    user = models.ForeignKey(MyUser, db_index=True)
    fleet_name = models.CharField(max_length=20)
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    system_id = models.IntegerField(default=0)
    planet_id = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    planet_status = models.BooleanField(default=1)
    fleet_hold = models.IntegerField(default=0)
    resource_hold = models.ForeignKey(ResourceHold)
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
