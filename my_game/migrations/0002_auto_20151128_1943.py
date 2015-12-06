# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_game', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fuelpattern',
            name='user',
            field=models.ForeignKey(default=2, to='my_game.MyUser'),
        ),
        migrations.AlterField(
            model_name='uservariables',
            name='registr_aluminum',
            field=models.IntegerField(default=0, verbose_name='\u0410\u043b\u044e\u043c\u0438\u043d\u0438\u0439 \u043f\u0440\u0438 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u0438'),
        ),
        migrations.AlterField(
            model_name='uservariables',
            name='registr_chemical',
            field=models.IntegerField(default=0, verbose_name='\u0425\u0438\u043c\u0438\u0447\u0435\u0441\u043a\u0438\u0435 \u0440\u0435\u0430\u043a\u0442\u0438\u0432\u044b \u043f\u0440\u0438 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u0438'),
        ),
        migrations.AlterField(
            model_name='uservariables',
            name='registr_cobalt',
            field=models.IntegerField(default=0, verbose_name='\u041a\u043e\u0431\u0430\u043b\u044c\u0442 \u043f\u0440\u0438 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u0438'),
        ),
        migrations.AlterField(
            model_name='uservariables',
            name='registr_construction_material',
            field=models.IntegerField(default=0, verbose_name='\u0421\u0442\u0440\u043e\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0435 \u043c\u0430\u0442\u0435\u0440\u0438\u0430\u043b\u044b \u043f\u0440\u0438 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u0438'),
        ),
        migrations.AlterField(
            model_name='uservariables',
            name='registr_cooper',
            field=models.IntegerField(default=0, verbose_name='\u041c\u0435\u0434\u044c \u043f\u0440\u0438 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u0438'),
        ),
        migrations.AlterField(
            model_name='uservariables',
            name='registr_fober_optic_element',
            field=models.IntegerField(default=0, verbose_name='\u041e\u043f\u0442\u043e\u0432\u043e\u043b\u043e\u043a\u043e\u043d\u043d\u044b\u0435 \u0435\u043b\u0435\u043c\u0435\u043d\u0442\u044b \u043f\u0440\u0438 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u0438'),
        ),
        migrations.AlterField(
            model_name='uservariables',
            name='registr_high_strength_allov',
            field=models.IntegerField(default=0, verbose_name='\u0412\u044b\u0441\u043e\u043a\u043e\u043f\u0440\u043e\u0447\u043d\u044b\u0435 \u0441\u043f\u043b\u0430\u0432\u044b \u043f\u0440\u0438 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u0438'),
        ),
        migrations.AlterField(
            model_name='uservariables',
            name='registr_inneilit',
            field=models.IntegerField(default=0, verbose_name='\u0418\u043d\u043d\u044d\u0438\u043b\u0438\u0442 \u043f\u0440\u0438 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u0438'),
        ),
        migrations.AlterField(
            model_name='uservariables',
            name='registr_iron',
            field=models.IntegerField(default=0, verbose_name='\u0416\u0435\u043b\u0435\u0437\u043e \u043f\u0440\u0438 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u0438'),
        ),
        migrations.AlterField(
            model_name='uservariables',
            name='registr_microprocessor_element',
            field=models.IntegerField(default=0, verbose_name='\u041c\u0438\u043a\u0440\u043e\u043f\u0440\u043e\u0446\u0435\u0441\u0441\u043e\u0440\u043d\u044b\u0435 \u0435\u043b\u0435\u043c\u0435\u043d\u0442\u044b \u043f\u0440\u0438 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u0438'),
        ),
        migrations.AlterField(
            model_name='uservariables',
            name='registr_nanoelement',
            field=models.IntegerField(default=0, verbose_name='\u041d\u0430\u043d\u043e\u0435\u043b\u0435\u043c\u0435\u043d\u0442\u044b \u043f\u0440\u0438 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u0438'),
        ),
        migrations.AlterField(
            model_name='uservariables',
            name='registr_nickel',
            field=models.IntegerField(default=0, verbose_name='\u041d\u0438\u043a\u0435\u043b\u044c \u043f\u0440\u0438 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u0438'),
        ),
        migrations.AlterField(
            model_name='uservariables',
            name='registr_renniit',
            field=models.IntegerField(default=0, verbose_name='\u0420\u0435\u043d\u043d\u0438\u0438\u0442 \u043f\u0440\u0438 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u0438'),
        ),
        migrations.AlterField(
            model_name='uservariables',
            name='registr_veriarit',
            field=models.IntegerField(default=0, verbose_name='\u0412\u0430\u0440\u0438\u0430\u0442\u0438\u0442 \u043f\u0440\u0438 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u0438'),
        ),
    ]
