# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0007_auto_20160331_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='installation',
            name='installer',
            field=models.ForeignKey(related_name='installed_by', verbose_name='Installer', blank=True, to='manager.EventUser', null=True),
            preserve_default=True,
        ),
    ]
