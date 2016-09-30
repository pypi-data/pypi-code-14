# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='BibblioIDMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bibblio_id', models.UUIDField(default=uuid.uuid4, verbose_name='Bibblio ID', db_index=True)),
                ('catalog_id', models.UUIDField(default=uuid.uuid4, verbose_name='Catalog ID')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(related_name='bibblio_id_maps', to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Bibblio ID Map',
                'verbose_name_plural': 'Bibblio ID Maps',
            },
        ),
        migrations.CreateModel(
            name='ContentMetadata',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('relevance', models.FloatField(default=0.0, verbose_name='relevance')),
                ('count', models.PositiveIntegerField(default=0, verbose_name='count')),
                ('additional_data', jsonfield.fields.JSONField(default=b'{}', verbose_name='additional data')),
                ('ignore', models.BooleanField(default=False, help_text='When true, this content is never tagged with this metadata.', verbose_name='ignore')),
                ('bibblio_id', models.ForeignKey(to='bibblio.BibblioIDMap')),
                ('content_type', models.ForeignKey(related_name='+', to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Content Metadata',
                'verbose_name_plural': 'Content Metadata',
            },
        ),
        migrations.CreateModel(
            name='Metadata',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=255, verbose_name='text')),
                ('type', models.CharField(default=b'Keyword', max_length=255, verbose_name='type', db_index=True)),
                ('linked_data', jsonfield.fields.JSONField(default=b'{}', verbose_name='linked data')),
                ('ignore', models.BooleanField(default=False, help_text='When true, content is never tagged with this metadata, and remove from previously tagged content.', verbose_name='ignore')),
            ],
            options={
                'verbose_name': 'Metadata',
                'verbose_name_plural': 'Metadata',
            },
        ),
        migrations.CreateModel(
            name='QueuedContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('status', models.CharField(default=b'index', max_length=50, verbose_name='status', choices=[(b'index', 'To Index'), (b'get_results', 'Awaiting Results'), (b'error', 'An Error Occurred'), (b'done', 'Finished')])),
                ('status_info', models.TextField(default=b'', verbose_name='status information', blank=True)),
                ('bibblio_id', models.ForeignKey(blank=True, to='bibblio.BibblioIDMap', null=True)),
                ('content_type', models.ForeignKey(related_name='+', to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'QueuedContent',
                'verbose_name_plural': 'QueuedContent',
            },
        ),
        migrations.AlterUniqueTogether(
            name='metadata',
            unique_together=set([('text', 'type')]),
        ),
        migrations.AlterIndexTogether(
            name='metadata',
            index_together=set([('text', 'type')]),
        ),
        migrations.AddField(
            model_name='contentmetadata',
            name='metadata',
            field=models.ForeignKey(to='bibblio.Metadata'),
        ),
        migrations.AlterUniqueTogether(
            name='bibblioidmap',
            unique_together=set([('bibblio_id', 'content_type', 'object_id')]),
        ),
    ]
