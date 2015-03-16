# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0009_remove_installerfromorganizer_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='installerfromorganizer',
            name='software',
        ),
        migrations.DeleteModel(
            name='InstallerFromOrganizer',
        ),
        migrations.AlterField(
            model_name='sede',
            name='event_information',
            field=ckeditor.fields.RichTextField(help_text='Event Information HTML', null=True, verbose_name='Event Information', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sede',
            name='footer',
            field=ckeditor.fields.RichTextField(help_text='Footer HTML', null=True, verbose_name='Footer', blank=True),
            preserve_default=True,
        ),
    ]
