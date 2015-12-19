# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def create_resource(my_game, schema_editor):
    BasicResource = my_game.get_model("my_game", "BasicResource")
    res = BasicResource(
        resource_name='Никель',
        description='Никель'
    )
    res.save()


class Migration(migrations.Migration):
    dependencies = [
        ('my_game', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_resource)
    ]
