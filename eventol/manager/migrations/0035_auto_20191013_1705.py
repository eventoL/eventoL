# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-10-13 17:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0034_auto_20191013_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='limit_proposal_date',
            field=models.DateField(blank=True, help_text='Limit date to submit talk proposals', null=True, verbose_name='Limit Proposals Date'),
        ),
    ]