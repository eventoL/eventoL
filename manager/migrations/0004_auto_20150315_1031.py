# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0003_auto_20150313_1827'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(verbose_name=b'URL')),
                ('text', models.CharField(max_length=200, verbose_name='Text')),
                ('sede', models.ForeignKey(verbose_name=b'Sede', to='manager.Sede')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContactType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200, verbose_name='Name')),
                ('icon_class', models.CharField(max_length=200, verbose_name='Icon Class')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='contact',
            name='type',
            field=models.ForeignKey(verbose_name='Contact Type', to='manager.ContactType'),
            preserve_default=True,
        ),
    ]
