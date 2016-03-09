# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import manager.models
from django.conf import settings
import django.core.validators
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50, null=True, verbose_name='Title', blank=True)),
                ('long_description', models.TextField(verbose_name='Long Description')),
                ('confirmed', models.BooleanField(default=False, verbose_name='Confirmed')),
                ('abstract', models.TextField(help_text='Short idea of the talk (Two or three sentences)', verbose_name='Abstract')),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Activity',
                'verbose_name_plural': 'Activities',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Adress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('adress', models.CharField(max_length=200, verbose_name='Adress')),
                ('latitude', models.FloatField(verbose_name='Latitude', validators=[django.core.validators.MinValueValidator(-90), django.core.validators.MaxValueValidator(90)])),
                ('longitude', models.FloatField(verbose_name='Longitude', validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)])),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Attendee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('additional_info', models.CharField(help_text='Any additional info you consider relevant', max_length=200, null=True, verbose_name='Additional Info', blank=True)),
            ],
            options={
                'verbose_name': 'Attendee',
                'verbose_name_plural': 'Attendees',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Collaborator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('assignation', models.CharField(help_text='Assignations given to the user (i.e. Talks, Coffee...)', max_length=200, null=True, verbose_name='Assignation', blank=True)),
                ('time_availability', models.CharField(help_text='Time gap in which you can help during the event. i.e. "All the event", "Morning", "Afternoon"...', max_length=200, null=True, verbose_name='Time Availability', blank=True)),
                ('phone', models.CharField(max_length=200, null=True, verbose_name='Phone', blank=True)),
                ('address', models.CharField(max_length=200, null=True, verbose_name='Address', blank=True)),
                ('additional_info', models.CharField(help_text='Any additional info you consider relevant', max_length=200, null=True, verbose_name='Additional Info', blank=True)),
            ],
            options={
                'verbose_name': 'Collaborator',
                'verbose_name_plural': 'Collaborators',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField()),
                ('body', models.TextField()),
                ('activity', models.ForeignKey(verbose_name=b'Activity', to='manager.Activity')),
                ('user', models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(verbose_name=b'URL')),
                ('text', models.CharField(max_length=200, verbose_name='Text')),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('email', models.EmailField(max_length=75, verbose_name='Email')),
                ('message', models.TextField(verbose_name='Message')),
            ],
            options={
                'verbose_name': 'Contact Message',
                'verbose_name_plural': 'Contact Messages',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContactType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200, verbose_name='Name')),
                ('icon_class', models.CharField(max_length=200, verbose_name='Icon Class')),
            ],
            options={
                'verbose_name': 'Contact Type',
                'verbose_name_plural': 'Contact Types',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('date', models.DateField(help_text='Date of the event', verbose_name='Date')),
                ('limit_proposal_date', models.DateField(help_text='Date Limit of Talk Proposal', verbose_name='Limit Proposal Date')),
                ('url', models.CharField(help_text='URL for the event i.e. CABA', max_length=200, verbose_name='URL', validators=[manager.models.validate_url])),
                ('external_url', models.URLField(default=None, blank=True, help_text="If you want to use other page for your event rather than eventoL's one, you can put the absolute url here", null=True, verbose_name='External URL')),
                ('email', models.EmailField(max_length=75, verbose_name='Email')),
                ('event_information', ckeditor.fields.RichTextField(help_text='Event Information HTML', null=True, verbose_name='Event Information', blank=True)),
                ('schedule_confirm', models.BooleanField(default=False, verbose_name='Schedule Confirm')),
                ('adress', models.ForeignKey(verbose_name='Adress', to='manager.Adress')),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventoLUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('assisted', models.BooleanField(default=False, verbose_name='Assisted')),
                ('event', models.ForeignKey(verbose_name=b'Event', to='manager.Event', help_text='Event you are going to collaborate')),
                ('user', models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'EventoL User',
                'verbose_name_plural': 'EventoL User',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hardware',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=200, verbose_name='Type', choices=[(b'MOB', 'Mobile'), (b'NOTE', 'Notebook'), (b'NET', 'Netbook'), (b'TAB', 'Tablet'), (b'DES', 'Desktop'), (b'OTH', 'Other')])),
                ('model', models.CharField(max_length=200, null=True, verbose_name='Model', blank=True)),
                ('serial', models.CharField(max_length=200, null=True, verbose_name='Serial', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HardwareManufacturer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, null=True, verbose_name='Name', blank=True)),
            ],
            options={
                'verbose_name': 'Hardware Manufacturer',
                'verbose_name_plural': 'Hardware Manufacturers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=200, verbose_name='Type')),
                ('url', models.URLField(verbose_name=b'URL')),
                ('cropping', models.CharField(max_length=200, verbose_name='Text')),
            ],
            options={
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InstalationAttendee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('installarion_additional_info', models.TextField(help_text='i.e. Wath kind of PC are you bringing', null=True, verbose_name='Additional Info', blank=True)),
                ('eventolUser', models.ForeignKey(verbose_name='EventoL User', to='manager.EventoLUser')),
            ],
            options={
                'verbose_name': 'Instalation Attendee',
                'verbose_name_plural': 'Instalation Attendees',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Installation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(help_text='Any information or trouble you found and consider relevant to document', null=True, verbose_name='Notes', blank=True)),
                ('attendee', models.ForeignKey(verbose_name='Attendee', to='manager.InstalationAttendee', help_text='The owner of the installed hardware')),
                ('hardware', models.ForeignKey(verbose_name='Hardware', blank=True, to='manager.Hardware', null=True)),
            ],
            options={
                'verbose_name': 'Installation',
                'verbose_name_plural': 'Installations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Installer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.CharField(help_text='Linux Knowledge level for an installation', max_length=200, verbose_name='Level', choices=[(b'1', 'Beginner'), (b'2', 'Medium'), (b'3', 'Advanced'), (b'4', 'Super Hacker')])),
                ('eventolUser', models.ForeignKey(verbose_name='EventoL User', to='manager.EventoLUser')),
            ],
            options={
                'verbose_name': 'Installer',
                'verbose_name_plural': 'Installers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='i.e. Classroom 256', max_length=200, verbose_name='Name')),
                ('event', models.ForeignKey(verbose_name=b'Event', to='manager.Event')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Room',
                'verbose_name_plural': 'Rooms',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Software',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('version', models.CharField(max_length=200, verbose_name='Version')),
                ('type', models.CharField(max_length=200, verbose_name='Type', choices=[(b'OS', 'Operative System'), (b'AP', 'Application'), (b'SU', 'Support and Problem Fixing'), (b'OT', 'Other')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Speaker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('eventolUser', models.ForeignKey(verbose_name='EventoL User', to='manager.EventoLUser')),
            ],
            options={
                'verbose_name': 'Speaker',
                'verbose_name_plural': 'Speakers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Talk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateTimeField(verbose_name='Start Time')),
                ('end_date', models.DateTimeField(verbose_name='End Time')),
                ('room', models.ForeignKey(verbose_name='Room', to='manager.Room')),
            ],
            options={
                'verbose_name': 'Talk',
                'verbose_name_plural': 'Talks',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TalkProposal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('speakers_names', models.CharField(help_text="Comma separated speaker's names", max_length=600, verbose_name='Speakers Names')),
                ('speakers_email', models.CharField(help_text="Comma separated speaker's emails", max_length=600, verbose_name='Speakers Emails')),
                ('labels', models.CharField(help_text='Comma separated tags. i.e. Linux, Free Software, Debian', max_length=200, verbose_name='Labels')),
                ('presentation', models.FileField(help_text='Any material you are going to use for the talk (optional, but recommended)', upload_to=b'talks', null=True, verbose_name='Presentation', blank=True)),
                ('level', models.CharField(help_text="The talk's Technical level", max_length=100, verbose_name='Level', choices=[(b'1', 'Beginner'), (b'2', 'Medium'), (b'3', 'Advanced')])),
                ('activity', models.ForeignKey(verbose_name=b'Activity', to='manager.Activity')),
                ('image', models.ForeignKey(verbose_name=b'Image', blank=True, to='manager.Image', null=True)),
            ],
            options={
                'verbose_name': 'Talk Proposal',
                'verbose_name_plural': 'Talk Proposals',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TalkType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Talk Type',
                'verbose_name_plural': 'Talk Types',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='talkproposal',
            name='type',
            field=models.ForeignKey(verbose_name='Type', to='manager.TalkType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='talk',
            name='talk_proposal',
            field=models.OneToOneField(null=True, blank=True, to='manager.TalkProposal', verbose_name='TalkProposal'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='room',
            name='for_type',
            field=models.ForeignKey(verbose_name='For talk type', to='manager.TalkType', help_text='The type of talk the room is going to be used for.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='installation',
            name='installer',
            field=models.ForeignKey(related_name='installed_by', verbose_name='Installer', blank=True, to='manager.Installer', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='installation',
            name='software',
            field=models.ForeignKey(verbose_name='Software', blank=True, to='manager.Software', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hardware',
            name='manufacturer',
            field=models.ForeignKey(verbose_name='Manufacturer', blank=True, to='manager.HardwareManufacturer', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='image',
            field=models.ForeignKey(verbose_name=b'Image', blank=True, to='manager.Image', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contact',
            name='event',
            field=models.ForeignKey(related_name='contacts', verbose_name=b'Event', to='manager.Event'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contact',
            name='type',
            field=models.ForeignKey(verbose_name='Contact Type', to='manager.ContactType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='collaborator',
            name='eventolUser',
            field=models.ForeignKey(verbose_name='EventoL User', to='manager.EventoLUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attendee',
            name='eventolUser',
            field=models.ForeignKey(verbose_name='EventoL User', blank=True, to='manager.EventoLUser', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='event',
            field=models.ForeignKey(verbose_name=b'Event', to='manager.Event'),
            preserve_default=True,
        ),
    ]
