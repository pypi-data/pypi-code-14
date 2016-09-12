# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Person'
        db.create_table('interviews_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('birthdate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('sex', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('interviews', ['Person'])

        # Adding model 'Interview'
        db.create_table('interviews_interview', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['interviews.Person'])),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['sites.Site'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('is_published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('published_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('introduction', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('footnotes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('interviews', ['Interview'])

        # Adding model 'Picture'
        db.create_table('interviews_picture', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('interview', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['interviews.Interview'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('legend', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('interviews', ['Picture'])

        # Adding model 'Answer'
        db.create_table('interviews_answer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('interview', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['interviews.Interview'])),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('question', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('response', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('interviews', ['Answer'])

        # Adding unique constraint on 'Answer', fields ['interview', 'order']
        db.create_unique('interviews_answer', ['interview_id', 'order'])

        # Adding M2M table for field related_pictures on 'Answer'
        db.create_table('interviews_answer_related_pictures', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('answer', models.ForeignKey(orm['interviews.answer'], null=False)),
            ('picture', models.ForeignKey(orm['interviews.picture'], null=False))
        ))
        db.create_unique('interviews_answer_related_pictures', ['answer_id', 'picture_id'])

        # Adding model 'Quote'
        db.create_table('interviews_quote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('related_to', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['interviews.Answer'])),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('quote', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('interviews', ['Quote'])

        # Adding model 'InterviewPicture'
        db.create_table('interviews_interviewpicture', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('interview', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['interviews.Interview'])),
            ('picture', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['interviews.Picture'])),
            ('is_selected', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('interviews', ['InterviewPicture'])

        # Adding model 'Product'
        db.create_table('interviews_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('amazon_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('interviews', ['Product'])

        # Adding model 'InterviewProduct'
        db.create_table('interviews_interviewproduct', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('interview', self.gf('django.db.models.fields.related.ForeignKey')(related_name='products', to=orm['interviews.Interview'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['interviews.Product'])),
        ))
        db.send_create_signal('interviews', ['InterviewProduct'])


    def backwards(self, orm):
        # Removing unique constraint on 'Answer', fields ['interview', 'order']
        db.delete_unique('interviews_answer', ['interview_id', 'order'])

        # Deleting model 'Person'
        db.delete_table('interviews_person')

        # Deleting model 'Interview'
        db.delete_table('interviews_interview')

        # Deleting model 'Picture'
        db.delete_table('interviews_picture')

        # Deleting model 'Answer'
        db.delete_table('interviews_answer')

        # Removing M2M table for field related_pictures on 'Answer'
        db.delete_table('interviews_answer_related_pictures')

        # Deleting model 'Quote'
        db.delete_table('interviews_quote')

        # Deleting model 'InterviewPicture'
        db.delete_table('interviews_interviewpicture')

        # Deleting model 'Product'
        db.delete_table('interviews_product')

        # Deleting model 'InterviewProduct'
        db.delete_table('interviews_interviewproduct')


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
            'amazon_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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