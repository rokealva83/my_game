# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_game', '0003_remove_basicfactory_price_mat_construction_material'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basicmaterial',
            name='time_production',
        ),
    ]
