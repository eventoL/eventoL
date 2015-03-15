# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0004_auto_20150315_1031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='sede',
            field=models.ForeignKey(related_name='contacts', verbose_name=b'Sede', to='manager.Sede'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='talkproposal',
            name='sede',
            field=models.ForeignKey(related_name='talk_proposals', verbose_name=b'Sede', to='manager.Sede', help_text='Sede you are proposing the talk to'),
            preserve_default=True,
        ),
    ]
