# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2020-01-15 20:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0043_auto_20200115_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='speaker_bio',
            field=models.TextField(help_text='Tell us about you (we will use it as your "bio" in our website)', null=True, verbose_name='Speaker Bio'),
        ),
    ]
