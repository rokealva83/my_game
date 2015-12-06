# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_game', '0015_shellpattern_shell_class'),
    ]

    operations = [
        migrations.RenameField(
            model_name='armorpattern',
            old_name='basic_armor',
            new_name='basic_pattern',
        ),
        migrations.RenameField(
            model_name='devicepattern',
            old_name='basic_device',
            new_name='basic_pattern',
        ),
        migrations.RenameField(
            model_name='enginepattern',
            old_name='basic_engine',
            new_name='basic_pattern',
        ),
        migrations.RenameField(
            model_name='fuelpattern',
            old_name='basic_fuel',
            new_name='basic_pattern',
        ),
        migrations.RenameField(
            model_name='generatorpattern',
            old_name='basic_generator',
            new_name='basic_pattern',
        ),
        migrations.RenameField(
            model_name='hullpattern',
            old_name='basic_hull',
            new_name='basic_pattern',
        ),
        migrations.RenameField(
            model_name='modulepattern',
            old_name='basic_module',
            new_name='basic_pattern',
        ),
        migrations.RenameField(
            model_name='shellpattern',
            old_name='basic_shell',
            new_name='basic_pattern',
        ),
        migrations.RenameField(
            model_name='shieldpattern',
            old_name='basic_shield',
            new_name='basic_pattern',
        ),
        migrations.RenameField(
            model_name='weaponpattern',
            old_name='basic_weapon',
            new_name='basic_pattern',
        ),
    ]
