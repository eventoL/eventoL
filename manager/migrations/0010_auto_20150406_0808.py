# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0009_auto_20150401_0023'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sede',
            options={'ordering': ['name']},
        ),
    ]
