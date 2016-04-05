# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_auto_20160320_0309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='event',
            field=models.ForeignKey(related_name='contacts', verbose_name=b'Event', blank=True, to='manager.Event'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='text',
            field=models.CharField(help_text='i.e. @Flisol', max_length=200, verbose_name='Text'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contact',
            name='url',
            field=models.URLField(help_text='i.e. https://twitter.com/flisol', verbose_name=b'URL'),
            preserve_default=True,
        ),
    ]
