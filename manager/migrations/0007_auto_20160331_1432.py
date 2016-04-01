# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0006_remove_nonregisteredattendee_assisted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hardware',
            name='serial',
        ),
        migrations.RemoveField(
            model_name='software',
            name='version',
        ),
        migrations.AlterField(
            model_name='hardware',
            name='manufacturer',
            field=models.CharField(max_length=200, null=True, verbose_name='Manufacturer', blank=True),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='HardwareManufacturer',
        ),
        migrations.AlterField(
            model_name='installation',
            name='attendee',
            field=models.ForeignKey(verbose_name='Attendee', to='manager.EventUser', help_text='The owner of the installed hardware'),
            preserve_default=True,
        ),
    ]
