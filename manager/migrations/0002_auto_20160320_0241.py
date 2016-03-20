# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='instalationattendee',
            options={'verbose_name': 'Installation Attendee', 'verbose_name_plural': 'Installation Attendees'},
        ),
        migrations.AlterField(
            model_name='collaborator',
            name='assignation',
            field=models.CharField(help_text='Anything you can help with (i.e. Talks, Coffee...)', max_length=200, null=True, verbose_name='Assignation', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='collaborator',
            name='time_availability',
            field=models.CharField(help_text='Time gap in which you can help during the event. i.e. "All the event", "Morning", "Afternoon", ...', max_length=200, null=True, verbose_name='Time Availability', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='eventuser',
            name='event',
            field=models.ForeignKey(verbose_name=b'Event', to='manager.Event'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='eventuser',
            name='user',
            field=models.ForeignKey(verbose_name='User', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='instalationattendee',
            name='installarion_additional_info',
            field=models.TextField(help_text='i.e. Wath kind of PC are you bringing?', null=True, verbose_name='Additional Info', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='installer',
            name='level',
            field=models.CharField(help_text='Knowledge level for an installation', max_length=200, verbose_name='Level', choices=[(b'1', 'Beginner'), (b'2', 'Medium'), (b'3', 'Advanced'), (b'4', 'Super Hacker')]),
            preserve_default=True,
        ),
    ]
