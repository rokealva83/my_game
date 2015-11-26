# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_game', '0002_auto_20151031_2227'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectship',
            name='hull_id',
        ),
        migrations.AddField(
            model_name='projectship',
            name='hull_pattern',
            field=models.ForeignKey(default=None, to='my_game.HullPattern'),
        ),
        migrations.AddField(
            model_name='turnshipbuild',
            name='amount',
            field=models.IntegerField(default=0),
        ),
    ]
