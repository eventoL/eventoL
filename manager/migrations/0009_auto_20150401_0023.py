# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0008_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talk',
            name='end_date',
            field=models.DateTimeField(verbose_name='End Time'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='talk',
            name='start_date',
            field=models.DateTimeField(verbose_name='Start Time'),
            preserve_default=True,
        ),
    ]
