# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='user',
            field=models.ForeignKey(default=None, to='recipes.User'),
            preserve_default=True,
        ),
    ]
