# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='talkproposal',
            name='level',
            field=models.CharField(default=b'Beginner', help_text="The talk's Technical level", max_length=100, verbose_name='Level', choices=[(b'1', 'Beginner'), (b'2', 'Medium'), (b'3', 'Advanced')]),
            preserve_default=True,
        ),
    ]
