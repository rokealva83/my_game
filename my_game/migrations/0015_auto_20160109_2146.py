# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_game', '0014_auto_20160109_2144'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flightplanoverload',
            name='fleet',
        ),
        migrations.RemoveField(
            model_name='flightplanoverload',
            name='flightplan',
        ),
        migrations.DeleteModel(
            name='FlightplanOverload',
        ),
    ]
