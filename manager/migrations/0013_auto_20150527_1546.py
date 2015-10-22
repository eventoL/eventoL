# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0012_auto_20150526_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='proposal',
            field=models.ForeignKey(verbose_name='TalkProposal', to='manager.TalkProposal'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
