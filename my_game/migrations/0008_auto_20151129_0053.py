# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_game', '0007_auto_20151129_0039'),
    ]

    operations = [
        migrations.RenameField(
            model_name='uservariables',
            old_name='time_verificetion_resource',
            new_name='time_verification_resource',
        ),
    ]
