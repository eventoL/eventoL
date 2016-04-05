# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0008_auto_20160331_2345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='event',
            field=models.ForeignKey(verbose_name=b'Event', blank=True, to='manager.Event', null=True),
            preserve_default=True,
        ),
    ]
