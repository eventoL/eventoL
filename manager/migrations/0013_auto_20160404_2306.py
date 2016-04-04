# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0012_auto_20160402_1106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='schedule_confirm',
            field=models.BooleanField(default=False, verbose_name='Confirm Schedule'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='installationattendee',
            name='installation_additional_info',
            field=models.TextField(help_text='i.e. Wath kind of PC are you bringing?', null=True, verbose_name='Installation Additional Info', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='talkproposal',
            name='level',
            field=models.CharField(help_text="Talk's Technical level", max_length=100, verbose_name='Level', choices=[(b'1', 'Beginner'), (b'2', 'Medium'), (b'3', 'Advanced')]),
            preserve_default=True,
        ),
    ]
