# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0007_auto_20150316_0010'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstallerFromOrganizer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=30, null=True, verbose_name='Username', blank=True)),
                ('level', models.CharField(help_text='Linux Knowledge level for an installation', max_length=200, verbose_name='Level', choices=[(b'1', 'Beginner'), (b'2', 'Medium'), (b'3', 'Advanced'), (b'4', 'Super Hacker')])),
                ('software', models.ManyToManyField(help_text='Select all the software you can install. Hold Ctrl key to select many', to='manager.Software', null=True, verbose_name='Software', blank=True)),
            ],
            options={
                'verbose_name': 'Installer',
                'verbose_name_plural': 'Installers',
            },
            bases=(models.Model,),
        ),
    ]
