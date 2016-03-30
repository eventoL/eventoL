# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0004_auto_20160324_1856'),
    ]

    operations = [
        migrations.CreateModel(
            name='NonRegisteredAttendee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=30, verbose_name='First Name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='Last Name', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='E-mail Address', blank=True)),
                ('assisted', models.BooleanField(default=True, verbose_name='Assisted')),
                ('is_installing', models.BooleanField(default=False, help_text='Will you bring a PC for installation?', verbose_name='Is Installing')),
                ('installation_additional_info', models.TextField(help_text='i.e. Wath kind of PC are you bringing?', null=True, verbose_name='Additional Info', blank=True)),
            ],
            options={
                'verbose_name': 'Non Registered  Attendee',
                'verbose_name_plural': 'Non Registered Attendees',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='eventuser',
            name='nonregisteredattendee',
            field=models.ForeignKey(verbose_name='Non Registered Attendee', blank=True, to='manager.NonRegisteredAttendee', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='eventuser',
            unique_together=set([('event', 'user')]),
        ),
    ]
