# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0005_auto_20160329_0554'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nonregisteredattendee',
            name='assisted',
        ),
    ]
