# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0008_installerfromorganizer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='installerfromorganizer',
            name='username',
        ),
    ]
