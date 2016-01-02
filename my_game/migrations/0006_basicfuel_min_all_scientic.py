# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_game', '0005_remove_fuelpattern_fuel_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='basicfuel',
            name='min_all_scientic',
            field=models.IntegerField(default=0, verbose_name='\u041c\u0438\u043d\u0438\u043c\u0430\u043b\u044c\u043d\u044b\u0439 \u0443\u0440\u043e\u0432\u0435\u043d\u044c \u043d\u0430\u0443\u043a\u0438'),
        ),
    ]
