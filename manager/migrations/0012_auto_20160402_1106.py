# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0011_contactmessage_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='contacttype',
            name='validate',
            field=models.CharField(default=1, help_text='Type of field validation', max_length=10, verbose_name='Level', choices=[(b'1', 'Validate URL'), (b'2', 'Validate Email'), (b'3', "Don't validate")]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contact',
            name='url',
            field=models.CharField(help_text='i.e. https://twitter.com/flisol', max_length=200, verbose_name=b'Direccion'),
            preserve_default=True,
        ),
    ]
