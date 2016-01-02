# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_game', '0006_basicfuel_min_all_scientic'),
    ]

    operations = [
        migrations.CreateModel(
            name='FleetParametrAcceleration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('acceleration', models.FloatField()),
                ('braking', models.FloatField()),
                ('reverse', models.FloatField()),
                ('fleet', models.ForeignKey(to='my_game.Fleet')),
            ],
            options={
                'db_table': 'fleet_parametr_acceleration',
            },
        ),
        migrations.AlterField(
            model_name='basicmodule',
            name='param1',
            field=models.IntegerField(help_text='\u0414\u043e\u0431\u044b\u0447\u0430 \u0432 \u043c\u0438\u043d\u0443\u0442\u0443, \u0420\u0430\u0441\u0442\u043e\u044f\u043d\u0438\u0435 \u0441\u043a\u0430\u043d\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f, \u041f\u0440\u043e\u0446\u0435\u043d\u0442 \u0443\u0441\u043a\u043e\u0440\u0435\u043d\u0438\u044f, \u0420\u0435\u043c\u043e\u043d\u0442/\u0441\u0442\u0440\u043e\u0438\u0442\u0435\u043b\u044c\u0441\u0442\u0432\u043e \u043c \u043c\u0438\u043d\u0443\u0442\u0443', verbose_name='\u041f\u0430\u0440\u0430\u043c\u0435\u0442\u0440 1'),
        ),
        migrations.AlterField(
            model_name='basicmodule',
            name='param2',
            field=models.IntegerField(help_text='\u0412\u0440\u0435\u043c\u044f \u0441\u043a\u0430\u043d\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f, \u041f\u0440\u043e\u0446\u0435\u043d\u0442 \u043f\u0440\u0438 \u0442\u043e\u0440\u043c\u043e\u0436\u0435\u043d\u0438\u0438', verbose_name='\u041f\u0430\u0440\u0430\u043c\u0435\u0442\u0440 2'),
        ),
        migrations.AlterField(
            model_name='basicmodule',
            name='param3',
            field=models.IntegerField(help_text='\u041c\u0435\u0442\u043e\u0434 \u0441\u043a\u0430\u043d\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f, \u041f\u0440\u043e\u0446\u0435\u043d\u0442 \u043f\u0440\u0438 \u0440\u0435\u0432\u0435\u0440\u0441\u0435, \u041c\u0435\u0442\u043e\u0434 \u0441\u0442\u0440\u043e\u0438\u0442\u0435\u043b\u044c\u0441\u0442\u0432\u0430(1)/\u0440\u0435\u043c\u043e\u043d\u0442\u0430(2), \u041c\u0435\u0442\u043e\u0434 \u0437\u0430\u043f\u0440\u0430\u0432\u043a\u0438(1)/\u043f\u0435\u0440\u0435\u0433\u0440\u0443\u0437\u043a\u0438(2)', verbose_name='\u041f\u0430\u0440\u0430\u043c\u0435\u0442\u0440 3'),
        ),
    ]
