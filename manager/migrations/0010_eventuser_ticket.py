# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0009_auto_20160401_0001'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventuser',
            name='ticket',
            field=models.BooleanField(default=False, verbose_name='Ticket sent'),
            preserve_default=True,
        ),
    ]
