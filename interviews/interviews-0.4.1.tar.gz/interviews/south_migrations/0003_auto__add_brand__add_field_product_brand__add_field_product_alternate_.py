# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Brand'
        db.create_table('interviews_brand', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal('interviews', ['Brand'])

        # Adding field 'Product.brand'
        db.add_column('interviews_product', 'brand',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['interviews.Brand'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Product.alternate_titles'
        db.add_column('interviews_product', 'alternate_titles',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Brand'
        db.delete_table('interviews_brand')

        # Deleting field 'Product.brand'
        db.delete_column('interviews_product', 'brand_id')

        # Deleting field 'Product.alternate_titles'
        db.delete_column('interviews_product', 'alternate_titles')


    models = {
        'interviews.answer': {
            'Meta': {'ordering': "['order']", 'unique_together': "(('interview', 'order'),)", 'object_name': 'Answer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interview': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['interviews.Interview']"}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'question': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'related_pictures': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['interviews.Picture']", 'symmetrical': 'False', 'blank': 'True'}),
            'response': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'interviews.brand': {
            'Meta': {'object_name': 'Brand'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'interviews.interview': {
            'Meta': {'ordering': "['-published_on']", 'object_name': 'Interview'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'footnotes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'introduction': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['interviews.Person']"}),
            'published_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['sites.Site']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'interviews.interviewpicture': {
            'Meta': {'object_name': 'InterviewPicture'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interview': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['interviews.Interview']"}),
            'is_selected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'picture': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['interviews.Picture']"})
        },
        'interviews.interviewproduct': {
            'Meta': {'object_name': 'InterviewProduct'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interview': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'products'", 'to': "orm['interviews.Interview']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['interviews.Product']"})
        },
        'interviews.person': {
            'Meta': {'object_name': 'Person'},
            'birthdate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sex': ('django.db.models.fields.IntegerField', [], {})
        },
        'interviews.picture': {
            'Meta': {'object_name': 'Picture'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'interview': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['interviews.Interview']"}),
            'legend': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'interviews.product': {
            'Meta': {'object_name': 'Product'},
            'alternate_titles': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'amazon_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['interviews.Brand']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published_interviews_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'interviews.quote': {
            'Meta': {'object_name': 'Quote'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quote': ('django.db.models.fields.TextField', [], {}),
            'related_to': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['interviews.Answer']"})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['interviews']