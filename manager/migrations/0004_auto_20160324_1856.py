# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0003_auto_20160323_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='event',
            field=models.ForeignKey(related_name='contacts', verbose_name=b'Event', blank=True, to='manager.Event', null=True),
            preserve_default=True,
        ),
    ]
