# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_game', '0013_auto_20160105_1907'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='flightplanoverload',
            table='flightplan_overload',
        ),
    ]
