# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_game', '0017_auto_20151206_2030'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shellpattern',
            old_name='shell_name',
            new_name='element_name',
        ),
        migrations.RenameField(
            model_name='shieldpattern',
            old_name='shield_name',
            new_name='element_name',
        ),
        migrations.RenameField(
            model_name='weaponpattern',
            old_name='weapon_name',
            new_name='element_name',
        ),
    ]
