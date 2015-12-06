# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_game', '0002_auto_20151128_1943'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basicfactory',
            name='price_mat_construction_material',
        ),
    ]
