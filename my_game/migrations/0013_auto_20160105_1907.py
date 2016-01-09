# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_game', '0012_auto_20160105_1906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flightplanoverload',
            name='resource',
            field=models.BooleanField(default=False),
        ),
    ]
