# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Person.about'
        db.add_column(u'interviews_person', 'about',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Person.about'
        db.delete_column(u'interviews_person', 'about')


    models = {
        u'interviews.answer': {
            'Meta': {'ordering': "['order']", 'unique_together': "(('interview', 'order'),)", 'object_name': 'Answer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interview': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['interviews.Interview']"}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'question': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'related_pictures': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['interviews.Picture']", 'symmetrical': 'False', 'blank': 'True'}),
            'response': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'interviews.brand': {
            'Meta': {'ordering': "['title']", 'object_name': 'Brand'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'interviews.interview': {
            'Meta': {'ordering': "['-published_on']", 'object_name': 'Interview'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'footnotes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'introduction': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['interviews.Person']"}),
            'published_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'interviews.interviewpicture': {
            'Meta': {'object_name': 'InterviewPicture'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interview': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['interviews.Interview']"}),
            'is_selected': ('django.db.models.fields.BooleanField', [], {}),
            'picture': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['interviews.Picture']"})
        },
        u'interviews.interviewproduct': {
            'Meta': {'object_name': 'InterviewProduct'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interview': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'products'", 'to': u"orm['interviews.Interview']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['interviews.Product']"})
        },
        u'interviews.person': {
            'Meta': {'object_name': 'Person'},
            'about': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'birthdate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sex': ('django.db.models.fields.IntegerField', [], {})
        },
        u'interviews.picture': {
            'Meta': {'object_name': 'Picture'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'interview': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['interviews.Interview']"}),
            'legend': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'interviews.product': {
            'Meta': {'ordering': "['title']", 'object_name': 'Product'},
            'alternate_titles': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'amazon_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['interviews.Brand']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published_interviews_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'interviews.quote': {
            'Meta': {'object_name': 'Quote'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quote': ('django.db.models.fields.TextField', [], {}),
            'related_to': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['interviews.Answer']"})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['interviews']