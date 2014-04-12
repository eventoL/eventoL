# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Building'
        db.create_table(u'manager_building', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, db_index=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'manager', ['Building'])

        # Adding model 'Sede'
        db.create_table(u'manager_sede', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cities.Country'])),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cities.Region'])),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cities.City'])),
            ('district', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cities.District'], null=True, blank=True)),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['manager.Building'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'manager', ['Sede'])

        # Adding model 'Attendant'
        db.create_table(u'manager_attendant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=200)),
            ('sede', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['manager.Sede'])),
            ('assisted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'manager', ['Attendant'])

        # Adding model 'Organizer'
        db.create_table(u'manager_organizer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, null=True, blank=True)),
            ('sede', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['manager.Sede'])),
            ('is_coordinator', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('assignation', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('additional_info', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('assisted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'manager', ['Organizer'])

        # Adding model 'HardwareManufacturer'
        db.create_table(u'manager_hardwaremanufacturer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'manager', ['HardwareManufacturer'])

        # Adding model 'Hardware'
        db.create_table(u'manager_hardware', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('manufacturer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['manager.HardwareManufacturer'], null=True, blank=True)),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('serial', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'manager', ['Hardware'])

        # Adding model 'Software'
        db.create_table(u'manager_software', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'manager', ['Software'])

        # Adding model 'Installer'
        db.create_table(u'manager_installer', (
            (u'organizer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['manager.Organizer'], unique=True, primary_key=True)),
            ('level', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'manager', ['Installer'])

        # Adding M2M table for field software on 'Installer'
        db.create_table(u'manager_installer_software', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('installer', models.ForeignKey(orm[u'manager.installer'], null=False)),
            ('software', models.ForeignKey(orm[u'manager.software'], null=False))
        ))
        db.create_unique(u'manager_installer_software', ['installer_id', 'software_id'])

        # Adding model 'Installation'
        db.create_table(u'manager_installation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('attendant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['manager.Attendant'])),
            ('hardware', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['manager.Hardware'], null=True, blank=True)),
            ('software', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['manager.Software'], null=True, blank=True)),
            ('installer', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='installed_by', null=True, to=orm['manager.Installer'])),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'manager', ['Installation'])

        # Adding model 'TalkType'
        db.create_table(u'manager_talktype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'manager', ['TalkType'])

        # Adding model 'TalkProposal'
        db.create_table(u'manager_talkproposal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=600)),
            ('speakers_email', self.gf('django.db.models.fields.CharField')(max_length=600)),
            ('labels', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('abstract', self.gf('django.db.models.fields.TextField')()),
            ('long_description', self.gf('django.db.models.fields.TextField')()),
            ('sede', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['manager.Sede'])),
            ('presentation', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['manager.TalkType'])),
            ('home_image', self.gf(u'django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('cropping', self.gf(u'django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'manager', ['TalkProposal'])

        # Adding model 'Room'
        db.create_table(u'manager_room', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sede', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['manager.Sede'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('for_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['manager.TalkType'])),
        ))
        db.send_create_signal(u'manager', ['Room'])

        # Adding model 'TalkTime'
        db.create_table(u'manager_talktime', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('sede', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['manager.Sede'])),
            ('talk_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['manager.TalkType'])),
        ))
        db.send_create_signal(u'manager', ['TalkTime'])

        # Adding model 'Talk'
        db.create_table(u'manager_talk', (
            (u'talkproposal_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['manager.TalkProposal'], unique=True, primary_key=True)),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['manager.Room'])),
            ('hour', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['manager.TalkTime'])),
        ))
        db.send_create_signal(u'manager', ['Talk'])

        # Adding M2M table for field speakers on 'Talk'
        db.create_table(u'manager_talk_speakers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('talk', models.ForeignKey(orm[u'manager.talk'], null=False)),
            ('organizer', models.ForeignKey(orm[u'manager.organizer'], null=False))
        ))
        db.create_unique(u'manager_talk_speakers', ['talk_id', 'organizer_id'])

        # Adding model 'EventInfo'
        db.create_table(u'manager_eventinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sede', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['manager.Sede'])),
            ('html', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'manager', ['EventInfo'])


    def backwards(self, orm):
        # Deleting model 'Building'
        db.delete_table(u'manager_building')

        # Deleting model 'Sede'
        db.delete_table(u'manager_sede')

        # Deleting model 'Attendant'
        db.delete_table(u'manager_attendant')

        # Deleting model 'Organizer'
        db.delete_table(u'manager_organizer')

        # Deleting model 'HardwareManufacturer'
        db.delete_table(u'manager_hardwaremanufacturer')

        # Deleting model 'Hardware'
        db.delete_table(u'manager_hardware')

        # Deleting model 'Software'
        db.delete_table(u'manager_software')

        # Deleting model 'Installer'
        db.delete_table(u'manager_installer')

        # Removing M2M table for field software on 'Installer'
        db.delete_table('manager_installer_software')

        # Deleting model 'Installation'
        db.delete_table(u'manager_installation')

        # Deleting model 'TalkType'
        db.delete_table(u'manager_talktype')

        # Deleting model 'TalkProposal'
        db.delete_table(u'manager_talkproposal')

        # Deleting model 'Room'
        db.delete_table(u'manager_room')

        # Deleting model 'TalkTime'
        db.delete_table(u'manager_talktime')

        # Deleting model 'Talk'
        db.delete_table(u'manager_talk')

        # Removing M2M table for field speakers on 'Talk'
        db.delete_table('manager_talk_speakers')

        # Deleting model 'EventInfo'
        db.delete_table(u'manager_eventinfo')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'cities.city': {
            'Meta': {'object_name': 'City'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'name_std': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'population': ('django.db.models.fields.IntegerField', [], {}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities.Region']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'subregion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities.Subregion']", 'null': 'True', 'blank': 'True'})
        },
        u'cities.country': {
            'Meta': {'ordering': "['name']", 'object_name': 'Country'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'db_index': 'True'}),
            'continent': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'population': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'tld': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        u'cities.district': {
            'Meta': {'object_name': 'District'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities.City']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'name_std': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'population': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'cities.region': {
            'Meta': {'object_name': 'Region'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'name_std': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'cities.subregion': {
            'Meta': {'object_name': 'Subregion'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'name_std': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities.Region']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'manager.attendant': {
            'Meta': {'object_name': 'Attendant'},
            'assisted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'sede': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['manager.Sede']"}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'manager.building': {
            'Meta': {'object_name': 'Building'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'manager.eventinfo': {
            'Meta': {'object_name': 'EventInfo'},
            'html': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sede': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['manager.Sede']"})
        },
        u'manager.hardware': {
            'Meta': {'object_name': 'Hardware'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['manager.HardwareManufacturer']", 'null': 'True', 'blank': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'serial': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'manager.hardwaremanufacturer': {
            'Meta': {'object_name': 'HardwareManufacturer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'manager.installation': {
            'Meta': {'object_name': 'Installation'},
            'attendant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['manager.Attendant']"}),
            'hardware': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['manager.Hardware']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'installer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'installed_by'", 'null': 'True', 'to': u"orm['manager.Installer']"}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'software': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['manager.Software']", 'null': 'True', 'blank': 'True'})
        },
        u'manager.installer': {
            'Meta': {'object_name': 'Installer', '_ormbases': [u'manager.Organizer']},
            'level': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'organizer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['manager.Organizer']", 'unique': 'True', 'primary_key': 'True'}),
            'software': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['manager.Software']", 'null': 'True', 'blank': 'True'})
        },
        u'manager.organizer': {
            'Meta': {'object_name': 'Organizer'},
            'additional_info': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'assignation': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'assisted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_coordinator': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'sede': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['manager.Sede']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'manager.room': {
            'Meta': {'object_name': 'Room'},
            'for_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['manager.TalkType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'sede': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['manager.Sede']"})
        },
        u'manager.sede': {
            'Meta': {'object_name': 'Sede'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities.City']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities.Country']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities.District']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['manager.Building']"}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cities.Region']"})
        },
        u'manager.software': {
            'Meta': {'object_name': 'Software'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'manager.talk': {
            'Meta': {'object_name': 'Talk', '_ormbases': [u'manager.TalkProposal']},
            'hour': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['manager.TalkTime']"}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['manager.Room']"}),
            'speakers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'speakers'", 'symmetrical': 'False', 'to': u"orm['manager.Organizer']"}),
            u'talkproposal_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['manager.TalkProposal']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'manager.talkproposal': {
            'Meta': {'object_name': 'TalkProposal'},
            'abstract': ('django.db.models.fields.TextField', [], {}),
            'cropping': (u'django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'home_image': (u'django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'labels': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'long_description': ('django.db.models.fields.TextField', [], {}),
            'presentation': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'sede': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['manager.Sede']"}),
            'speakers_email': ('django.db.models.fields.CharField', [], {'max_length': '600'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '600'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['manager.TalkType']"})
        },
        u'manager.talktime': {
            'Meta': {'object_name': 'TalkTime'},
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sede': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['manager.Sede']"}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'talk_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['manager.TalkType']"})
        },
        u'manager.talktype': {
            'Meta': {'object_name': 'TalkType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['manager']