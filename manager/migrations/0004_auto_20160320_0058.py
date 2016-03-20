# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import manager.models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0003_auto_20160316_0045'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Address',
        ),
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateField(help_text='When will your event be?', verbose_name='Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='external_url',
            field=models.URLField(default=None, blank=True, help_text='http://www.my-awesome-event.com', null=True, verbose_name='External URL'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='limit_proposal_date',
            field=models.DateField(help_text='Limit date to submit talk proposals', verbose_name='Limit Proposals Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Event Name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=models.CharField(help_text='For example: flisol-caba', max_length=200, verbose_name='URL', validators=[manager.models.validate_url]),
            preserve_default=True,
        ),
    ]
