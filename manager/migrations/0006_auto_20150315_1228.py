# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0005_auto_20150315_1103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sede',
            name='url',
            field=models.CharField(help_text='URL for the sede i.e. CABA', unique=True, max_length=200, verbose_name='URL', db_index=True),
            preserve_default=True,
        ),
    ]
