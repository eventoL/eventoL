# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0011_sede_external_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='talktype',
            name='color_class',
            field=models.CharField(default=b'', max_length=50, verbose_name='Color'),
            preserve_default=True,
        ),
    ]
