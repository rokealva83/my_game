# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_game', '0014_auto_20151206_1726'),
    ]

    operations = [
        migrations.AddField(
            model_name='shellpattern',
            name='shell_class',
            field=models.IntegerField(default=1, verbose_name='\u041a\u043b\u0430\u0441\u0441 \u0431\u043e\u0435\u043f\u0440\u0438\u043f\u0430\u0441\u0430'),
        ),
    ]
