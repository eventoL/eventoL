# Generated by Django 4.2 on 2024-06-22 17:40

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("manager", "0049_alter_attendee_customfields"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attendee",
            name="customFields",
            field=models.JSONField(default=dict),
        ),
    ]
