# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_game', '0002_auto_20151219_2146'),
    ]

    operations = [
        migrations.AddField(
            model_name='basicengine',
            name='fuel',
            field=models.ManyToManyField(to='my_game.BasicFuel', verbose_name='\u0422\u043e\u043f\u043b\u0438\u0432\u043e'),
        ),
        migrations.AlterField(
            model_name='basicfuel',
            name='fuel_class',
            field=models.IntegerField(verbose_name='\u041a\u043b\u0430\u0441\u0441 \u0442\u043e\u043f\u043b\u0438\u0432\u0430', choices=[(1, b'\xd0\x93\xd0\xb5\xd0\xbd\xd0\xb5\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80\xd0\xbd\xd0\xbe\xd0\xb5 \xd1\x82\xd0\xbe\xd0\xbf\xd0\xbb\xd0\xb8\xd0\xb2\xd0\xbe'), (2, b'\xd0\x94\xd0\xb2\xd0\xb8\xd0\xb3\xd0\xb0\xd1\x82\xd0\xb5\xd0\xbb\xd1\x8c\xd0\xbd\xd0\xbe\xd0\xb5 \xd1\x82\xd0\xbe\xd0\xbf\xd0\xbb\xd0\xb8\xd0\xb2\xd0\xbe')]),
        ),
        migrations.AlterField(
            model_name='basicmodule',
            name='param1',
            field=models.IntegerField(help_text='\u0414\u043e\u0431\u044b\u0447\u0430 \u0432 \u043c\u0438\u043d\u0443\u0442\u0443, \u0420\u0430\u0441\u0442\u043e\u044f\u043d\u0438\u0435 \u0441\u043a\u0430\u043d\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f, \u041f\u0440\u043e\u0446\u0435\u043d\u0442 \u0443\u0441\u043a\u043e\u0440\u0435\u043d\u0438\u044f', verbose_name='\u041f\u0430\u0440\u0430\u043c\u0435\u0442\u0440 1'),
        ),
        migrations.AlterField(
            model_name='basicmodule',
            name='param2',
            field=models.IntegerField(help_text='\u0420\u0435\u043c\u043e\u043d\u0442/\u0421\u0442\u0440\u043e\u0438\u0442\u0435\u043b\u044c\u0441\u0442\u0432\u043e \u0432 \u043c\u0438\u043d\u0443\u0442\u0443, \u0412\u0440\u0435\u043c\u044f \u0441\u043a\u0430\u043d\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f, \u041f\u0440\u043e\u0446\u0435\u043d\u0442 \u043f\u0440\u0438 \u0442\u043e\u0440\u043c\u043e\u0436\u0435\u043d\u0438\u0438', verbose_name='\u041f\u0430\u0440\u0430\u043c\u0435\u0442\u0440 2'),
        ),
        migrations.AlterField(
            model_name='basicmodule',
            name='param3',
            field=models.IntegerField(help_text='\u041c\u0435\u0442\u043e\u0434 \u0440\u0435\u043c\u043e\u043d\u0442\u0430/\u0441\u0442\u0440\u043e\u0438\u0442\u0435\u043b\u044c\u0441\u0442\u0432\u0430, \u041c\u0435\u0442\u043e\u0434 \u0441\u043a\u0430\u043d\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f, \u041f\u0440\u043e\u0446\u0435\u043d\u0442 \u043f\u0440\u0438 \u0440\u0435\u0432\u0435\u0440\u0441\u0435', verbose_name='\u041f\u0430\u0440\u0430\u043c\u0435\u0442\u0440 3'),
        ),
    ]
