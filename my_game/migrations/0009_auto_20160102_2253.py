# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_game', '0008_auto_20160101_1916'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fueltank',
            name='fuel_id',
        ),
        migrations.AddField(
            model_name='fueltank',
            name='fuel_pattern',
            field=models.ForeignKey(default=None, to='my_game.FuelPattern'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='basicfactory',
            name='assembly_workpiece',
            field=models.IntegerField(default=0, verbose_name='\u0412\u0440\u0435\u043c\u044f \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f \u0437\u0430\u0433\u043e\u0442\u043e\u0432\u043a\u0438'),
        ),
        migrations.AlterField(
            model_name='basicfactory',
            name='description',
            field=models.CharField(default=b'\xd0\x97\xd0\xb0\xd0\xb2\xd0\xbe\xd0\xb4 \xd0\xbf\xd0\xbe \xd0\xbf\xd1\x80\xd0\xbe\xd0\xb8\xd0\xb7\xd0\xb2\xd0\xbe\xd0\xb4\xd1\x81\xd1\x82\xd0\xb2\xd1\x83 ', max_length=500, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435'),
        ),
        migrations.AlterField(
            model_name='basicfactory',
            name='factory_mass',
            field=models.IntegerField(default=0, verbose_name='\u0412\u0435\u0441'),
        ),
        migrations.AlterField(
            model_name='basicfactory',
            name='factory_name',
            field=models.CharField(default=b'\xd0\x97\xd0\xb0\xd0\xb2\xd0\xbe\xd0\xb4 ""', max_length=50, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AlterField(
            model_name='basicfactory',
            name='factory_size',
            field=models.IntegerField(default=0, verbose_name='\u0420\u0430\u0437\u043c\u0435\u0440'),
        ),
        migrations.AlterField(
            model_name='basicfactory',
            name='price_expert_deployment',
            field=models.IntegerField(default=0, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0441\u043e\u0442\u0440\u0443\u0434\u043d\u0438\u043a\u043e\u0432'),
        ),
        migrations.AlterField(
            model_name='basicfactory',
            name='price_internal_currency',
            field=models.IntegerField(default=0, verbose_name='\u0426\u0435\u043d\u0430 \u0432 \u0432\u0430\u043b\u044e\u0442\u0435'),
        ),
        migrations.AlterField(
            model_name='basicfactory',
            name='time_deployment',
            field=models.IntegerField(default=0, verbose_name='\u0412\u0440\u0435\u043c\u044f \u0440\u0430\u0437\u0432\u0435\u0440\u0442\u044b\u0432\u0430\u043d\u0438\u044f'),
        ),
        migrations.AlterField(
            model_name='basicfactory',
            name='time_production',
            field=models.IntegerField(default=0, verbose_name='\u0412\u0440\u0435\u043c\u044f \u043f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0441\u0442\u0432\u0430'),
        ),
        migrations.AlterField(
            model_name='basichull',
            name='armor',
            field=models.IntegerField(default=0, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0431\u0440\u043e\u043d\u0438'),
        ),
        migrations.AlterField(
            model_name='basichull',
            name='engine',
            field=models.IntegerField(default=0, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0434\u0432\u0438\u0433\u0430\u0442\u0435\u043b\u0435\u0439'),
        ),
        migrations.AlterField(
            model_name='basichull',
            name='generator',
            field=models.IntegerField(default=0, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0433\u0435\u0440\u0435\u0440\u0430\u0442\u043e\u0440\u043e\u0432'),
        ),
        migrations.AlterField(
            model_name='basichull',
            name='hold_size',
            field=models.IntegerField(default=0, verbose_name='\u0420\u0430\u0437\u043c\u0435\u0440 \u0442\u0440\u044e\u043c\u0430'),
        ),
        migrations.AlterField(
            model_name='basichull',
            name='hull_health',
            field=models.IntegerField(default=0, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0437\u0434\u043e\u0440\u043e\u0432\u044c\u044f'),
        ),
        migrations.AlterField(
            model_name='basichull',
            name='hull_mass',
            field=models.IntegerField(default=0, verbose_name='\u041c\u0430\u0441\u0441\u0430'),
        ),
        migrations.AlterField(
            model_name='basichull',
            name='hull_size',
            field=models.IntegerField(default=0, verbose_name='\u0420\u0430\u0437\u043c\u0435\u0440'),
        ),
        migrations.AlterField(
            model_name='basichull',
            name='main_weapon',
            field=models.IntegerField(default=0, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0433\u043b\u0430\u0432\u043d\u043e\u0433\u043e \u043a\u0430\u043b\u0438\u0431\u0440\u0430'),
        ),
        migrations.AlterField(
            model_name='basichull',
            name='module',
            field=models.IntegerField(default=0, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u043c\u043e\u0434\u0443\u043b\u0435\u0439'),
        ),
        migrations.AlterField(
            model_name='basichull',
            name='power_consuption',
            field=models.IntegerField(default=0, verbose_name='\u041f\u043e\u0442\u0440\u0435\u0431\u043b\u0435\u043d\u0438\u0435 \u044d\u043d\u0435\u0440\u0433\u0438\u0438'),
        ),
        migrations.AlterField(
            model_name='basichull',
            name='price_internal_currency',
            field=models.IntegerField(default=0, verbose_name='\u0426\u0435\u043d\u0430 \u0432 \u0432\u0430\u043b\u044e\u0442\u0435'),
        ),
        migrations.AlterField(
            model_name='basichull',
            name='shield',
            field=models.IntegerField(default=0, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0449\u0438\u0442\u043e\u0432'),
        ),
        migrations.AlterField(
            model_name='basichull',
            name='weapon',
            field=models.IntegerField(default=0, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u043e\u0440\u0443\u0436\u0438\u044f'),
        ),
        migrations.AlterField(
            model_name='fleetengine',
            name='maneuverability',
            field=models.FloatField(default=0, verbose_name='\u041c\u0430\u043d\u0435\u0432\u0440\u0438\u043d\u043e\u0441\u0442\u044c'),
        ),
    ]
