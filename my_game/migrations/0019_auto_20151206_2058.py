# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_game', '0018_auto_20151206_2031'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hullpattern',
            old_name='hull_name',
            new_name='element_name',
        ),
    ]
