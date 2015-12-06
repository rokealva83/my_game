# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_game', '0006_auto_20151129_0000'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildinginstalled',
            name='production_class',
            field=models.IntegerField(default=14),
        ),
        migrations.AddField(
            model_name='buildinginstalled',
            name='production_id',
            field=models.IntegerField(default=1),
        ),
    ]
