# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_game', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='basicarmor',
            options={'verbose_name': '\u0411\u0440\u043e\u043d\u044c', 'verbose_name_plural': '\u0411\u0440\u043e\u043d\u044c'},
        ),
        migrations.AlterModelOptions(
            name='basicbuilding',
            options={'verbose_name': '\u0421\u0442\u0440\u043e\u0435\u043d\u0438\u0435', 'verbose_name_plural': '\u0421\u0442\u0440\u043e\u0435\u043d\u0438\u044f'},
        ),
        migrations.AlterModelOptions(
            name='basicdevice',
            options={'verbose_name': '\u0423\u0441\u0442\u0440\u043e\u0439\u0441\u0442\u0432\u043e', 'verbose_name_plural': '\u0423\u0441\u0442\u0440\u043e\u0439\u0441\u0442\u0432\u0430'},
        ),
        migrations.AlterModelOptions(
            name='basicengine',
            options={'verbose_name': '\u0414\u0432\u0438\u0433\u0430\u0442\u0435\u043b\u044c', 'verbose_name_plural': '\u0414\u0432\u0438\u0433\u0430\u0442\u0435\u043b\u0438'},
        ),
        migrations.AlterModelOptions(
            name='basicfactory',
            options={'verbose_name': '\u0424\u0430\u0431\u0440\u0438\u043a\u0430', 'verbose_name_plural': '\u0424\u0430\u0431\u0440\u0438\u043a\u0438'},
        ),
        migrations.AlterModelOptions(
            name='basicfuel',
            options={'verbose_name': '\u0422\u043e\u043f\u043b\u0438\u0432\u043e', 'verbose_name_plural': '\u0422\u043e\u043f\u043b\u0438\u0432\u043e'},
        ),
        migrations.AlterModelOptions(
            name='basicgenerator',
            options={'verbose_name': '\u0413\u0435\u043d\u0435\u0440\u0430\u0442\u043e\u0440', 'verbose_name_plural': '\u0413\u0435\u043d\u0435\u0440\u0430\u0442\u043e\u0440\u044b'},
        ),
        migrations.AlterModelOptions(
            name='basichull',
            options={'verbose_name': '\u041a\u043e\u0440\u043f\u0443\u0441', 'verbose_name_plural': '\u041a\u043e\u0440\u043f\u0443\u0441\u0430'},
        ),
        migrations.AlterModelOptions(
            name='basicmodule',
            options={'verbose_name': '\u041c\u043e\u0434\u0443\u043b\u044c', 'verbose_name_plural': '\u041c\u043e\u0434\u0443\u043b\u0438'},
        ),
        migrations.AlterModelOptions(
            name='basicresource',
            options={'verbose_name': '\u0420\u0435\u0441\u0443\u0440\u0441', 'verbose_name_plural': '\u0420\u0435\u0441\u0443\u0440\u0441\u044b'},
        ),
        migrations.AlterModelOptions(
            name='basicscientic',
            options={'verbose_name': '\u041d\u0430\u0443\u043a\u0430', 'verbose_name_plural': '\u041d\u0430\u0443\u043a\u0438'},
        ),
        migrations.AlterModelOptions(
            name='basicshell',
            options={'verbose_name': '\u0411\u043e\u0435\u043f\u0440\u0438\u043f\u0430\u0441', 'verbose_name_plural': '\u0411\u043e\u0435\u043f\u0440\u0438\u043f\u0430\u0441\u044b'},
        ),
        migrations.AlterModelOptions(
            name='basicshield',
            options={'verbose_name': '\u0429\u0438\u0442', 'verbose_name_plural': '\u0429\u0438\u0442\u044b'},
        ),
        migrations.AlterModelOptions(
            name='basicweapon',
            options={'verbose_name': '\u041e\u0440\u0443\u0436\u0438\u0435', 'verbose_name_plural': '\u041e\u0440\u0443\u0436\u0438\u0435'},
        ),
        migrations.RemoveField(
            model_name='basicfactory',
            name='price_mineral1',
        ),
        migrations.RemoveField(
            model_name='basicfactory',
            name='price_mineral2',
        ),
        migrations.RemoveField(
            model_name='basicfactory',
            name='price_mineral3',
        ),
        migrations.RemoveField(
            model_name='basicfactory',
            name='price_mineral4',
        ),
        migrations.RemoveField(
            model_name='factorypattern',
            name='price_mineral1',
        ),
        migrations.RemoveField(
            model_name='factorypattern',
            name='price_mineral2',
        ),
        migrations.RemoveField(
            model_name='factorypattern',
            name='price_mineral3',
        ),
        migrations.RemoveField(
            model_name='factorypattern',
            name='price_mineral4',
        ),
        migrations.AlterField(
            model_name='basicarmor',
            name='min_energy',
            field=models.IntegerField(default=0, verbose_name='\u041c\u0438\u043d\u0438\u043c\u0430\u043b\u044c\u043d\u044b\u0439 \u0443\u0440\u043e\u0432\u0435\u043d\u044c \u0445\u0438\u043c\u0438\u0438'),
        ),
        migrations.AlterField(
            model_name='basicdevice',
            name='min_energy',
            field=models.IntegerField(default=0, verbose_name='\u041c\u0438\u043d\u0438\u043c\u0430\u043b\u044c\u043d\u044b\u0439 \u0443\u0440\u043e\u0432\u0435\u043d\u044c \u0445\u0438\u043c\u0438\u0438'),
        ),
        migrations.AlterField(
            model_name='basicengine',
            name='min_energy',
            field=models.IntegerField(default=0, verbose_name='\u041c\u0438\u043d\u0438\u043c\u0430\u043b\u044c\u043d\u044b\u0439 \u0443\u0440\u043e\u0432\u0435\u043d\u044c \u0445\u0438\u043c\u0438\u0438'),
        ),
        migrations.AlterField(
            model_name='basicgenerator',
            name='min_energy',
            field=models.IntegerField(default=0, verbose_name='\u041c\u0438\u043d\u0438\u043c\u0430\u043b\u044c\u043d\u044b\u0439 \u0443\u0440\u043e\u0432\u0435\u043d\u044c \u0445\u0438\u043c\u0438\u0438'),
        ),
        migrations.AlterField(
            model_name='basichull',
            name='min_energy',
            field=models.IntegerField(default=0, verbose_name='\u041c\u0438\u043d\u0438\u043c\u0430\u043b\u044c\u043d\u044b\u0439 \u0443\u0440\u043e\u0432\u0435\u043d\u044c \u0445\u0438\u043c\u0438\u0438'),
        ),
        migrations.AlterField(
            model_name='basicmodule',
            name='min_energy',
            field=models.IntegerField(default=0, verbose_name='\u041c\u0438\u043d\u0438\u043c\u0430\u043b\u044c\u043d\u044b\u0439 \u0443\u0440\u043e\u0432\u0435\u043d\u044c \u0445\u0438\u043c\u0438\u0438'),
        ),
        migrations.AlterField(
            model_name='basicshell',
            name='min_energy',
            field=models.IntegerField(default=0, verbose_name='\u041c\u0438\u043d\u0438\u043c\u0430\u043b\u044c\u043d\u044b\u0439 \u0443\u0440\u043e\u0432\u0435\u043d\u044c \u0445\u0438\u043c\u0438\u0438'),
        ),
        migrations.AlterField(
            model_name='basicshield',
            name='min_energy',
            field=models.IntegerField(default=0, verbose_name='\u041c\u0438\u043d\u0438\u043c\u0430\u043b\u044c\u043d\u044b\u0439 \u0443\u0440\u043e\u0432\u0435\u043d\u044c \u0445\u0438\u043c\u0438\u0438'),
        ),
        migrations.AlterField(
            model_name='basicweapon',
            name='min_energy',
            field=models.IntegerField(default=0, verbose_name='\u041c\u0438\u043d\u0438\u043c\u0430\u043b\u044c\u043d\u044b\u0439 \u0443\u0440\u043e\u0432\u0435\u043d\u044c \u0445\u0438\u043c\u0438\u0438'),
        ),
        migrations.AlterField(
            model_name='usercity',
            name='user',
            field=models.ForeignKey(verbose_name='\u0413\u043e\u0440\u043e\u0434', to='my_game.MyUser'),
        ),
        migrations.AlterField(
            model_name='uservariables',
            name='registr_mineral1',
            field=models.IntegerField(verbose_name='\u0412\u0430\u0440\u0438\u0430\u0440\u0438\u0442 \u043f\u0440\u0438 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438'),
        ),
        migrations.AlterField(
            model_name='uservariables',
            name='registr_mineral2',
            field=models.IntegerField(verbose_name='\u0418\u043d\u043d\u044d\u043b\u0438\u0442 \u043f\u0440\u0438 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438'),
        ),
        migrations.AlterField(
            model_name='uservariables',
            name='registr_mineral3',
            field=models.IntegerField(verbose_name='\u0420\u0435\u043d\u043d\u0438\u0438\u0442 \u043f\u0440\u0438 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438'),
        ),
        migrations.AlterField(
            model_name='uservariables',
            name='registr_mineral4',
            field=models.IntegerField(verbose_name='\u041a\u043e\u0431\u0430\u043b\u044c\u0442 \u043f\u0440\u0438 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438'),
        ),
        migrations.AlterField(
            model_name='uservariables',
            name='registr_resource1',
            field=models.IntegerField(verbose_name='\u041d\u0438\u043a\u0435\u043b\u044c \u043f\u0440\u0438 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438'),
        ),
        migrations.AlterField(
            model_name='uservariables',
            name='registr_resource2',
            field=models.IntegerField(verbose_name='\u0416\u0435\u043b\u0435\u0437\u043e \u043f\u0440\u0438 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438'),
        ),
        migrations.AlterField(
            model_name='uservariables',
            name='registr_resource3',
            field=models.IntegerField(verbose_name='\u041c\u0435\u0434\u044c \u043f\u0440\u0438 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438'),
        ),
        migrations.AlterField(
            model_name='uservariables',
            name='registr_resource4',
            field=models.IntegerField(verbose_name='\u0410\u043b\u044e\u043c\u0438\u043d\u0438\u0439 \u043f\u0440\u0438 \u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438'),
        ),
    ]
