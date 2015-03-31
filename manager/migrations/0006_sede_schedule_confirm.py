# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0005_remove_comment_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='sede',
            name='schedule_confirm',
            field=models.BooleanField(default=False, verbose_name='Schedule Comfirm'),
            preserve_default=True,
        ),
    ]
