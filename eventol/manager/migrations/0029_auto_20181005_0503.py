# Generated by Django 1.11.6 on 2018-10-05 05:03

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("manager", "0028_reviewer"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="css_custom",
            field=models.FileField(
                blank=True,
                help_text="Custom css file for event page",
                null=True,
                upload_to="custom_css",
                verbose_name="Custom css",
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="template",
            field=models.FileField(
                blank=True,
                help_text="Custom template html for event index page",
                null=True,
                upload_to="templates",
                verbose_name="Template",
            ),
        ),
    ]
