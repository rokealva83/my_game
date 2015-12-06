# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_game', '0016_auto_20151206_2015'),
    ]

    operations = [
        migrations.RenameField(
            model_name='armorpattern',
            old_name='armor_name',
            new_name='element_name',
        ),
        migrations.RenameField(
            model_name='devicepattern',
            old_name='device_name',
            new_name='element_name',
        ),
        migrations.RenameField(
            model_name='enginepattern',
            old_name='engine_name',
            new_name='element_name',
        ),
        migrations.RenameField(
            model_name='fuelpattern',
            old_name='fuel_name',
            new_name='element_name',
        ),
        migrations.RenameField(
            model_name='generatorpattern',
            old_name='generator_name',
            new_name='element_name',
        ),
        migrations.RenameField(
            model_name='modulepattern',
            old_name='module_name',
            new_name='element_name',
        ),
    ]
