# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_game', '0009_auto_20160102_2253'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fleet',
            name='fuel_tank',
        ),
    ]
