# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_game', '0004_basicgenerator_fuel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fuelpattern',
            name='fuel_id',
        ),
    ]
