# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_game', '0013_basicweapon_shell_class'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicweapon',
            name='shell_class',
            field=models.IntegerField(default=0, verbose_name='\u041a\u043b\u0430\u0441\u0441 \u0431\u043e\u0435\u043f\u0440\u0438\u043f\u0430\u0441\u0430', choices=[(0, b'\xd0\xad\xd0\xbd\xd0\xb5\xd1\x80\xd0\xb3\xd0\xb8\xd1\x8f'), (1, b'\xd0\xa1\xd0\xbd\xd0\xb0\xd1\x80\xd1\x8f\xd0\xb4\xd1\x8b'), (2, b'\xd0\xa0\xd0\xb0\xd0\xba\xd0\xb5\xd1\x82\xd1\x8b'), (3, b'\xd0\xa2\xd0\xbe\xd1\x80\xd0\xbf\xd0\xb5\xd0\xb4\xd1\x8b')]),
        ),
        migrations.AlterField(
            model_name='enginepattern',
            name='basic_engine',
            field=models.ForeignKey(to='my_game.BasicEngine'),
        ),
    ]
