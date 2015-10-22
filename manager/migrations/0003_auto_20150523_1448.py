# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import manager.models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_event_multisede'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sede',
            name='url',
            field=models.CharField(help_text='URL for the sede i.e. CABA', max_length=200, verbose_name='URL', validators=[manager.models.validate_url]),
            preserve_default=True,
        ),
    ]
