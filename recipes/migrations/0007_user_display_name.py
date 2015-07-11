# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_user_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='display_name',
            field=models.TextField(default=''),
            preserve_default=True,
        ),
    ]
