# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FormDefinition'
        db.create_table(u'formed_formdefinition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('definition', self.gf('jsonfield.fields.JSONField')()),
            ('enable_summary', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('send_confirmation_email', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('confirmation_email_subject', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('confirmation_email_text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('notification_email_subject', self.gf('django.db.models.fields.CharField')(default=u"Submission of the form '{form_name}'", max_length=254)),
            ('finish_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('finish_text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'formed', ['FormDefinition'])

        # Adding M2M table for field sites on 'FormDefinition'
        m2m_table_name = db.shorten_name(u'formed_formdefinition_sites')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('formdefinition', models.ForeignKey(orm[u'formed.formdefinition'], null=False)),
            ('site', models.ForeignKey(orm[u'sites.site'], null=False))
        ))
        db.create_unique(m2m_table_name, ['formdefinition_id', 'site_id'])

        # Adding model 'FormSubmissionNotification'
        db.create_table(u'formed_formsubmissionnotification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('copy', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('form_definition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['formed.FormDefinition'])),
        ))
        db.send_create_signal(u'formed', ['FormSubmissionNotification'])

        # Adding unique constraint on 'FormSubmissionNotification', fields ['form_definition', 'email']
        db.create_unique(u'formed_formsubmissionnotification', ['form_definition_id', 'email'])

        # Adding model 'FormSubmission'
        db.create_table(u'formed_formsubmission', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('form_definition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['formed.FormDefinition'])),
            ('submission', self.gf('jsonfield.fields.JSONField')()),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'], null=True, blank=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(default=u'en-us', max_length=10)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'formed', ['FormSubmission'])


    def backwards(self, orm):
        # Removing unique constraint on 'FormSubmissionNotification', fields ['form_definition', 'email']
        db.delete_unique(u'formed_formsubmissionnotification', ['form_definition_id', 'email'])

        # Deleting model 'FormDefinition'
        db.delete_table(u'formed_formdefinition')

        # Removing M2M table for field sites on 'FormDefinition'
        db.delete_table(db.shorten_name(u'formed_formdefinition_sites'))

        # Deleting model 'FormSubmissionNotification'
        db.delete_table(u'formed_formsubmissionnotification')

        # Deleting model 'FormSubmission'
        db.delete_table(u'formed_formsubmission')


    models = {
        u'formed.formdefinition': {
            'Meta': {'object_name': 'FormDefinition'},
            'confirmation_email_subject': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'confirmation_email_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'definition': ('jsonfield.fields.JSONField', [], {}),
            'enable_summary': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'finish_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'finish_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notification_email_subject': ('django.db.models.fields.CharField', [], {'default': 'u"Submission of the form \'{form_name}\'"', 'max_length': '254'}),
            'send_confirmation_email': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['sites.Site']", 'symmetrical': 'False', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'})
        },
        u'formed.formsubmission': {
            'Meta': {'object_name': 'FormSubmission'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'form_definition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['formed.FormDefinition']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "u'en-us'", 'max_length': '10'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']", 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'submission': ('jsonfield.fields.JSONField', [], {})
        },
        u'formed.formsubmissionnotification': {
            'Meta': {'unique_together': "((u'form_definition', u'email'),)", 'object_name': 'FormSubmissionNotification'},
            'copy': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'form_definition': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['formed.FormDefinition']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['formed']
