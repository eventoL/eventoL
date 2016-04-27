# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0013_auto_20160404_2306'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstallationMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', ckeditor.fields.RichTextField(help_text='Email message HTML Body', null=True, verbose_name='Message Body', blank=True)),
                ('contact_email', models.EmailField(max_length=75, verbose_name='Contatc Email')),
                ('event', models.ForeignKey(verbose_name=b'Event', to='manager.Event')),
            ],
            options={
                'verbose_name': 'Post-install Email',
                'verbose_name_plural': 'Post-install Emails',
            },
            bases=(models.Model,),
        ),
    ]
