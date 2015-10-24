# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0010_auto_20150811_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='title',
            field=models.TextField(unique=True, default=''),
        ),
    ]
