# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_recipe_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='url',
            field=models.TextField(default=''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='recipe',
            name='url_name',
            field=models.TextField(default=''),
            preserve_default=True,
        ),
    ]
