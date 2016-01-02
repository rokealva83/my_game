# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_game', '0003_auto_20151227_1331'),
    ]

    operations = [
        migrations.AddField(
            model_name='basicgenerator',
            name='fuel',
            field=models.ManyToManyField(to='my_game.BasicFuel', verbose_name='\u0422\u043e\u043f\u043b\u0438\u0432\u043e'),
        ),
    ]
