# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_game', '0010_remove_fleet_fuel_tank'),
    ]

    operations = [
        migrations.CreateModel(
            name='FleetFuelRefill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fuel_refill', models.IntegerField(default=0)),
                ('fleet', models.ForeignKey(to='my_game.Fleet')),
            ],
            options={
                'db_table': 'fleet_fuel_refill',
            },
        ),
        migrations.CreateModel(
            name='FleetOverload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('overload', models.IntegerField(default=0)),
                ('fleet', models.ForeignKey(to='my_game.Fleet')),
            ],
            options={
                'db_table': 'fleet_overload',
            },
        ),
        migrations.RemoveField(
            model_name='uservariables',
            name='time_refill_youself',
        ),
        migrations.RemoveField(
            model_name='uservariables',
            name='time_refill_youself_all_goods',
        ),
        migrations.AlterField(
            model_name='basicengine',
            name='fuel',
            field=models.ManyToManyField(to='my_game.BasicFuel', verbose_name='\u0422\u043e\u043f\u043b\u0438\u0432\u043e', blank=True),
        ),
    ]
