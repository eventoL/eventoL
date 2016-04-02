# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import manager.models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=models.CharField(help_text='For example: flisol-caba', unique=True, max_length=200, verbose_name='URL', validators=[manager.models.validate_url]),
            preserve_default=True,
        ),
    ]
