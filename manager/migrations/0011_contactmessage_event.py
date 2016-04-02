# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0010_eventuser_ticket'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactmessage',
            name='event',
            field=models.ForeignKey(verbose_name=b'Event', blank=True, to='manager.Event', null=True),
            preserve_default=True,
        ),
    ]
