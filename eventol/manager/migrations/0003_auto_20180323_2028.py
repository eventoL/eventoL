# Generated by Django 1.11.6 on 2018-03-23 20:28

import image_cropping.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("manager", "0002_auto_20180321_1228"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="cropping",
            field=image_cropping.fields.ImageRatioField(
                "image",
                "700x450",
                adapt_rotation=False,
                allow_fullsize=False,
                free_crop=True,
                help_text="The image must be 700x450 px. You can crop it here.",
                hide_image_field=False,
                size_warning=True,
                verbose_name="Cropping",
            ),
        ),
    ]
