# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0003_talkproposal_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='sede',
            name='limit_proposal_date',
            field=models.DateField(default=datetime.datetime(2015, 3, 29, 0, 32, 15, 588920), help_text='Date Limit of Talk Proposal', verbose_name='Limit Proposal Date'),
            preserve_default=False,
        ),
    ]
