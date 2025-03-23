# Generated by Django 4.2 on 2025-03-22 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0050_alter_attendee_customfields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='activities_proposal_form_text',
            field=models.TextField(blank=True, help_text='A message to show in the activities proposal form', null=True, verbose_name='Activity proposal form text'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_information',
            field=models.TextField(blank=True, help_text='Event Info HTML', null=True, verbose_name='Event Info'),
        ),
        migrations.AlterField(
            model_name='installationmessage',
            name='message',
            field=models.TextField(blank=True, help_text='Email message HTML Body', null=True, verbose_name='Message Body'),
        ),
    ]
