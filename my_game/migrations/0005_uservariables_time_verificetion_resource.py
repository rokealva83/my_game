# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_game', '0004_remove_basicmaterial_time_production'),
    ]

    operations = [
        migrations.AddField(
            model_name='uservariables',
            name='time_verificetion_resource',
            field=models.IntegerField(default=0, verbose_name='\u0412\u0440\u0435\u043c\u044f \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0438 \u0434\u043e\u0431\u044b\u0447\u0438 \u0440\u0435\u0441\u0443\u0440\u0441\u043e\u0432'),
        ),
    ]
