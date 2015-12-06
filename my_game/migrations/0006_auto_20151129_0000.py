# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_game', '0005_uservariables_time_verificetion_resource'),
    ]

    operations = [
        migrations.AddField(
            model_name='factoryinstalled',
            name='production_class',
            field=models.IntegerField(default=11),
        ),
        migrations.AddField(
            model_name='factoryinstalled',
            name='production_id',
            field=models.IntegerField(default=0),
        ),
    ]
