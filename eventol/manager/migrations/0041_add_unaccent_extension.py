# Generated by Django 1.11.26 on 2019-12-02 04:32

from django.db import connection
from django.db import migrations
from django.db.utils import ProgrammingError


def forwards_func(apps, schema_editor):
    if "sqlite" not in connection.vendor:
        cursor = connection.cursor()
        try:
            cursor.execute("CREATE EXTENSION unaccent;")
        except ProgrammingError:
            pass


def reverse_func(apps, schema_editor):
    if "sqlite" not in connection.vendor:
        cursor = connection.cursor()
        try:
            cursor.execute("DROP EXTENSION unaccent;")
        except ProgrammingError:
            pass


class Migration(migrations.Migration):
    dependencies = [
        ("manager", "0040_auto_20191024_1536"),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
