# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import manager.models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0011_sede_external_url'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['name'], 'verbose_name': 'Room', 'verbose_name_plural': 'Rooms'},
        ),
        migrations.AlterField(
            model_name='sede',
            name='url',
            field=models.CharField(max_length=200, validators=[manager.models.validate_url], help_text='URL for the sede i.e. CABA', unique=True, verbose_name='URL', db_index=True),
            preserve_default=True,
        ),
    ]
