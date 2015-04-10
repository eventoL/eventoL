# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0010_auto_20150406_0808'),
    ]

    operations = [
        migrations.AddField(
            model_name='sede',
            name='external_url',
            field=models.URLField(default=None, blank=True, help_text="If you want to use other page for your sede rather than eventoL's one, you can put the absolute url here", null=True, verbose_name='External URL'),
            preserve_default=True,
        ),
    ]
