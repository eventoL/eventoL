# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0006_auto_20150315_1228'),
    ]

    operations = [
        migrations.AddField(
            model_name='sede',
            name='event_information',
            field=ckeditor.fields.RichTextField(default=b'', help_text='Event Information HTML', verbose_name='Event Information'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sede',
            name='footer',
            field=ckeditor.fields.RichTextField(default=b'', help_text='Footer HTML', verbose_name='Footer'),
            preserve_default=True,
        ),
    ]
