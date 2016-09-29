# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'FormDefinition.confirmation_email_show_summary'
        db.add_column(u'formed_formdefinition', 'confirmation_email_show_summary',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'FormDefinition.confirmation_email_show_summary'
        db.delete_column(u'formed_formdefinition', 'confirmation_email_show_summary')


    models = {
        u'formed.formdefinition': {
            'Meta': {'object_name': 'FormDefinition'},
            'confirmation_email_show_summary': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
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
