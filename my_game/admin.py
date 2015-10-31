# -*- coding: utf-8 -*-

from django.contrib import admin
from my_game.models import MyUser
from my_game.models import Race
from my_game.models import BasicScientic
from my_game.models import BasicFactory
from my_game.models import BasicArmor
from my_game.models import BasicResource
from my_game.models import BasicShell
from my_game.models import BasicBuilding
from my_game.models import BasicShield
from my_game.models import BasicHull
from my_game.models import BasicWeapon
from my_game.models import BasicDevice
from my_game.models import BasicEngine
from my_game.models import BasicFuel
from my_game.models import BasicGenerator
from my_game.models import BasicModule


class MyUserAdmin(admin.ModelAdmin):
    search_fields = ['user_name', 'premium_account']
    list_display = ['user_name', 'race', 'alliance', 'union', 'e_mail', 'premium_account', 'time_left_premium']


admin.site.register(MyUser, MyUserAdmin)


class MyRaceAdmin(admin.ModelAdmin):
    list_display = ['race_name', 'description', 'engine_system', 'engine_intersystem', 'engine_giper', 'engine_null',
                    'generator', 'armor', 'shield', 'weapon_attack', 'weapon_defense', 'exploration', 'disguse',
                    'auximilary', 'image']


admin.site.register(Race, MyRaceAdmin)


class MyResourceAdmin(admin.ModelAdmin):
    list_display = ['resource_name', 'description']


admin.site.register(BasicResource, MyResourceAdmin)


class MyScienticAdmin(admin.ModelAdmin):
    list_display = ['scientic_name', 'description', 'time_study', 'price_internal_currency', 'price_resource1',
                    'price_resource2', 'price_resource3', 'price_resource4', 'price_mineral1', 'price_mineral2',
                    'price_mineral3', 'price_mineral4']


admin.site.register(BasicScientic, MyScienticAdmin)


class MyFactoryAdmin(admin.ModelAdmin):
    list_display = ['factory_name', 'description', 'production_class', 'production_id', 'time_production',
                    'factory_size', 'factory_mass', 'power_consumption', 'price_internal_currency', 'price_resource1',
                    'price_resource2', 'price_resource3', 'price_resource4', 'price_mineral1', 'price_mineral2',
                    'price_mineral3', 'price_mineral4', 'price_expert_deployment', 'assembly_workpiece',
                    'time_deployment']


admin.site.register(BasicFactory, MyFactoryAdmin)


class MyHullAdmin(admin.ModelAdmin):
    list_display = ['hull_name', 'description', 'hull_health', 'generator', 'engine', 'weapon', 'armor', 'shield',
                    'module', 'main_weapon', 'hold_size', 'fuel_tank', 'hull_mass', 'hull_size', 'power_consuption',
                    'price_internal_currency', 'price_resource1', 'price_resource2', 'price_resource3',
                    'price_resource4', 'price_mineral1', 'price_mineral2', 'price_mineral3', 'price_mineral4',
                    'min_all_scientic', 'min_math', 'min_phis', 'min_biol', 'min_energy', 'min_radio', 'min_nanotech',
                    'min_astronomy', 'min_logist']


admin.site.register(BasicHull, MyHullAdmin)


class MyEngineAdmin(admin.ModelAdmin):
    list_display = ['engine_name', 'description', 'engine_health', 'system_power', 'intersystem_power', 'giper_power',
                    'nullT_power', 'engine_mass', 'engine_size', 'power_consuption', 'price_internal_currency',
                    'price_resource1', 'price_resource2', 'price_resource3', 'price_resource4', 'price_mineral1',
                    'price_mineral2', 'price_mineral3', 'price_mineral4', 'min_all_scientic', 'min_math', 'min_phis',
                    'min_biol', 'min_energy', 'min_radio', 'min_nanotech', 'min_astronomy', 'min_logist']


admin.site.register(BasicEngine, MyEngineAdmin)


class MyGeneratorAdmin(admin.ModelAdmin):
    list_display = ['generator_name', 'description', 'generator_health', 'produced_energy', 'fuel_necessary',
                    'generator_mass', 'generator_size', 'price_internal_currency', 'price_resource1', 'price_resource2',
                    'price_resource3', 'price_resource4', 'price_mineral1', 'price_mineral2', 'price_mineral3',
                    'price_mineral4', 'min_all_scientic', 'min_math', 'min_phis', 'min_biol', 'min_energy', 'min_radio',
                    'min_nanotech', 'min_astronomy', 'min_logist']


admin.site.register(BasicGenerator, MyGeneratorAdmin)


class MyShieldAdmin(admin.ModelAdmin):
    list_display = ['shield_name', 'description', 'shield_health', 'value_energy_resistance',
                    'value_phisical_resistance', 'shield_regeneration', 'number_of_emitter', 'shield_mass',
                    'shield_size', 'power_consuption', 'price_internal_currency', 'price_resource1', 'price_resource2',
                    'price_resource3', 'price_resource4', 'price_mineral1', 'price_mineral2', 'price_mineral3',
                    'price_mineral4', 'min_all_scientic', 'min_math', 'min_phis', 'min_biol', 'min_energy', 'min_radio',
                    'min_nanotech', 'min_astronomy', 'min_logist']


admin.site.register(BasicShield, MyShieldAdmin)


class MyWeaponAdmin(admin.ModelAdmin):
    list_display = ['weapon_name', 'description', 'weapon_health', 'weapon_energy_damage', 'weapon_regenerations',
                    'number_of_bursts', 'weapon_range', 'weapon_accuracy', 'weapon_mass', 'weapon_size', 'weapon_class',
                    'power_consuption', 'price_internal_currency', 'price_resource1', 'price_resource2',
                    'price_resource3', 'price_resource4', 'price_mineral1', 'price_mineral2', 'price_mineral3',
                    'price_mineral4', 'min_all_scientic', 'min_math', 'min_phis', 'min_biol', 'min_energy', 'min_radio',
                    'min_nanotech', 'min_astronomy', 'min_logist']


admin.site.register(BasicWeapon, MyWeaponAdmin)


class MyArmorAdmin(admin.ModelAdmin):
    list_display = ['armor_name', 'description', 'armor_health', 'value_energy_resistance', 'value_phisical_resistance',
                    'armor_power', 'armor_regeneration', 'armor_mass', 'price_internal_currency', 'price_resource1',
                    'price_resource2', 'price_resource3', 'price_resource4', 'price_mineral1', 'price_mineral2',
                    'price_mineral3', 'price_mineral4', 'min_all_scientic', 'min_math', 'min_phis', 'min_biol',
                    'min_energy', 'min_radio', 'min_nanotech', 'min_astronomy', 'min_logist']


admin.site.register(BasicArmor, MyArmorAdmin)


class MyShellAdmin(admin.ModelAdmin):
    list_display = ['shell_name', 'description', 'shell_phisical_damage', 'shell_speed', 'shell_mass', 'shell_size',
                    'price_internal_currency', 'price_resource1', 'price_resource2', 'price_resource3',
                    'price_resource4', 'price_mineral1', 'price_mineral2', 'price_mineral3', 'price_mineral4',
                    'min_all_scientic', 'min_math', 'min_phis', 'min_biol', 'min_energy', 'min_radio', 'min_nanotech',
                    'min_astronomy', 'min_logist']


admin.site.register(BasicShell, MyShellAdmin)


class MyModuleAdmin(admin.ModelAdmin):
    list_display = ['module_name', 'description', 'module_health', 'param1', 'param2', 'param3', 'module_mass',
                    'module_size', 'module_class', 'power_consuption', 'price_internal_currency', 'price_resource1',
                    'price_resource2', 'price_resource3', 'price_resource4', 'price_mineral1', 'price_mineral2',
                    'price_mineral3', 'price_mineral4', 'min_all_scientic', 'min_math', 'min_phis', 'min_biol',
                    'min_energy', 'min_radio', 'min_nanotech', 'min_astronomy', 'min_logist']


admin.site.register(BasicModule, MyModuleAdmin)


class MyFuelAdmin(admin.ModelAdmin):
    list_display = ['fuel_name', 'description', 'fuel_mass', 'fuel_size', 'fuel_efficiency', 'fuel_class', 'fuel_id',
                    'price_internal_currency', 'price_resource1', 'price_resource2', 'price_resource3',
                    'price_resource4', 'price_mineral1', 'price_mineral2', 'price_mineral3', 'price_mineral4']


admin.site.register(BasicFuel, MyFuelAdmin)


class MyDeviceAdmin(admin.ModelAdmin):
    list_display = ['device_name', 'description', 'device_health', 'param1', 'param2', 'param3', 'device_mass',
                    'device_size', 'device_class', 'power_consuption', 'price_internal_currency', 'price_resource1',
                    'price_resource2', 'price_resource3', 'price_resource4', 'price_mineral1', 'price_mineral2',
                    'price_mineral3', 'price_mineral4', 'min_all_scientic', 'min_math', 'min_phis', 'min_biol',
                    'min_energy', 'min_radio', 'min_nanotech', 'min_astronomy', 'min_logist']


admin.site.register(BasicDevice, MyDeviceAdmin)


class MyBuildingAdmin(admin.ModelAdmin):
    list_display = ['building_name', 'description', 'production_class', 'production_id', 'time_production', 'warehouse',
                    'max_warehouse', 'power_consumption', 'price_internal_currency', 'price_resource1',
                    'price_resource2', 'price_resource3', 'price_resource4', 'price_mineral1', 'price_mineral2',
                    'price_mineral3', 'price_mineral4', 'price_expert_deployment', 'assembly_workpiece',
                    'time_deployment', 'building_size', 'building_mass']


admin.site.register(BasicBuilding, MyBuildingAdmin)
