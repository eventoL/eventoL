# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_auto_20160313_1841'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organizer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('eventolUser', models.ForeignKey(verbose_name='EventoL User', blank=True, to='manager.EventoLUser', null=True)),
            ],
            options={
                'verbose_name': 'Organizer',
                'verbose_name_plural': 'Organizers',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='activity',
            name='end_date',
            field=models.DateTimeField(null=True, verbose_name='End Time', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activity',
            name='room',
            field=models.ForeignKey(verbose_name='Room', blank=True, to='manager.Room', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activity',
            name='start_date',
            field=models.DateTimeField(null=True, verbose_name='Start Time', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comment',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='talkproposal',
            name='activity',
            field=models.ForeignKey(verbose_name=b'Activity', blank=True, to='manager.Activity', null=True),
            preserve_default=True,
        ),
    ]
