# Generated by Django 1.11.6 on 2018-04-11 02:05

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("manager", "0006_event_registration_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="activity",
            name="type",
            field=models.CharField(
                blank=True,
                choices=[("1", "Talk"), ("2", "Workshop"), ("3", "Lightning talk")],
                max_length=200,
                null=True,
                verbose_name="Type",
            ),
        ),
    ]
