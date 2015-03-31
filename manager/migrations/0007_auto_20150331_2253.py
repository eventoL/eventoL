# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0006_sede_schedule_confirm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sede',
            name='schedule_confirm',
            field=models.BooleanField(default=False, verbose_name='Schedule Confirm'),
            preserve_default=True,
        ),
    ]
