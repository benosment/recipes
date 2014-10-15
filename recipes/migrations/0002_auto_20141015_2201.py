# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='directions',
            field=models.TextField(default=''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.TextField(default=''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='recipe',
            name='servings',
            field=models.TextField(default=''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='recipe',
            name='title',
            field=models.TextField(default=''),
            preserve_default=True,
        ),
    ]
