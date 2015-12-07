# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_game', '0010_auto_20151206_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='basicshell',
            name='shell_class',
            field=models.IntegerField(default=1, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', choices=[(1, b'\xd0\xa1\xd0\xbd\xd0\xb0\xd1\x80\xd1\x8f\xd0\xb4\xd1\x8b'), (2, b'\xd0\xa0\xd0\xb0\xd0\xba\xd0\xb5\xd1\x82\xd1\x8b'), (3, b'\xd0\xa2\xd0\xbe\xd1\x80\xd0\xbf\xd0\xb5\xd0\xb4\xd1\x8b')]),
        ),
    ]