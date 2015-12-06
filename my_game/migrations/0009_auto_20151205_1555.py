# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_game', '0008_auto_20151129_0053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicweapon',
            name='number_of_bursts',
            field=models.IntegerField(default=0, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0437\u0430\u043b\u043f\u043e\u0432'),
        ),
        migrations.AlterField(
            model_name='basicweapon',
            name='weapon_accuracy',
            field=models.IntegerField(default=0, verbose_name='\u0422\u043e\u0447\u043d\u043e\u0441\u0442\u044c'),
        ),
        migrations.AlterField(
            model_name='basicweapon',
            name='weapon_class',
            field=models.IntegerField(default=1, verbose_name='\u041a\u043b\u0430\u0441\u0441 \u043e\u0440\u0443\u0436\u0438\u044f', choices=[(b'1', b'\xd0\xad\xd0\xbd\xd0\xb5\xd1\x80\xd0\xb3\xd0\xb5\xd1\x82\xd0\xb8\xd1\x87\xd0\xb5\xd1\x81\xd0\xba\xd0\xbe\xd0\xb5'), (b'2', b'\xd0\xad\xd0\xbd\xd0\xb5\xd1\x80\xd0\xb3\xd0\xb5\xd1\x82\xd0\xb8\xd1\x87\xd0\xb5\xd1\x81\xd0\xba\xd0\xb8\xd0\xb9 \xd0\xb3\xd0\xbb\xd0\xb0\xd0\xb2\xd0\xbd\xd1\x8b\xd0\xb9 \xd0\xba\xd0\xb0\xd0\xbb\xd0\xb8\xd0\xb1\xd1\x80'), (b'3', b'\xd0\x9a\xd0\xb8\xd0\xbd\xd0\xb5\xd1\x82\xd0\xb8\xd1\x87\xd0\xb5\xd1\x81\xd0\xba\xd0\xbe\xd0\xb5'), (b'4', b'\xd0\x9a\xd0\xb8\xd0\xbd\xd0\xb5\xd1\x82\xd0\xb8\xd1\x87\xd0\xb5\xd1\x81\xd0\xba\xd0\xb8\xd0\xb9 \xd0\xb3\xd0\xbb\xd0\xb0\xd0\xb2\xd0\xbd\xd1\x8b\xd0\xb9 \xd0\xba\xd0\xb0\xd0\xbb\xd0\xb8\xd0\xb1\xd1\x80')]),
        ),
        migrations.AlterField(
            model_name='basicweapon',
            name='weapon_energy_damage',
            field=models.IntegerField(default=0, verbose_name='\u042d\u043d\u0435\u0440\u0433\u0435\u0442\u0438\u0447\u0435\u0441\u043a\u0438\u0439 \u0443\u0440\u043e\u043d'),
        ),
        migrations.AlterField(
            model_name='basicweapon',
            name='weapon_mass',
            field=models.IntegerField(default=0, verbose_name='\u041c\u0430\u0441\u0441\u0430'),
        ),
        migrations.AlterField(
            model_name='basicweapon',
            name='weapon_range',
            field=models.IntegerField(default=0, verbose_name='\u0414\u0430\u043b\u044c\u043d\u043e\u0441\u0442\u044c'),
        ),
        migrations.AlterField(
            model_name='basicweapon',
            name='weapon_regenerations',
            field=models.IntegerField(default=0, verbose_name='\u0412\u0440\u0435\u043c\u044f \u043f\u0435\u0440\u0435\u0437\u0430\u0440\u044f\u0434\u043a\u0438'),
        ),
        migrations.AlterField(
            model_name='weaponpattern',
            name='number_of_bursts',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='weaponpattern',
            name='weapon_accuracy',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='weaponpattern',
            name='weapon_energy_damage',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='weaponpattern',
            name='weapon_range',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='weaponpattern',
            name='weapon_regenerations',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterModelTable(
            name='resourcehold',
            table='resource_hold',
        ),
    ]
