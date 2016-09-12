# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField()),
                ('question', models.TextField(blank=True)),
                ('response', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'Answer',
                'verbose_name_plural': 'Answers',
            },
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Brand',
                'verbose_name_plural': 'Brands',
            },
        ),
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('is_published', models.BooleanField(default=False)),
                ('published_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('introduction', models.TextField(null=True, blank=True)),
                ('footnotes', models.TextField(null=True, blank=True)),
                ('website', models.URLField(null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
                'ordering': ['-published_on'],
                'verbose_name': 'Interview',
                'verbose_name_plural': 'Interviews',
            },
        ),
        migrations.CreateModel(
            name='InterviewPicture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_selected', models.BooleanField(default=False)),
                ('interview', models.ForeignKey(to='interviews.Interview')),
            ],
        ),
        migrations.CreateModel(
            name='InterviewProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('interview', models.ForeignKey(related_name='products', to='interviews.Interview')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('birthdate', models.DateField(null=True, blank=True)),
                ('sex', models.IntegerField(choices=[(1, 'Man'), (2, 'Woman')])),
                ('about', models.TextField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Person',
                'verbose_name_plural': 'Persons',
            },
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'pictures')),
                ('legend', models.TextField(blank=True)),
                ('interview', models.ForeignKey(to='interviews.Interview')),
            ],
            options={
                'verbose_name': 'Picture',
                'verbose_name_plural': 'Pictures',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('description', models.TextField(blank=True)),
                ('alternate_titles', models.TextField(blank=True)),
                ('amazon_url', models.URLField(null=True, blank=True)),
                ('published_interviews_count', models.IntegerField(default=0, verbose_name='Published interviews', editable=False)),
                ('brand', models.ForeignKey(blank=True, to='interviews.Brand', null=True)),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author', models.CharField(max_length=255)),
                ('quote', models.TextField()),
                ('related_to', models.ForeignKey(to='interviews.Answer')),
            ],
            options={
                'verbose_name': 'Quote',
                'verbose_name_plural': 'Quotes',
            },
        ),
        migrations.AddField(
            model_name='interviewproduct',
            name='product',
            field=models.ForeignKey(to='interviews.Product'),
        ),
        migrations.AddField(
            model_name='interviewpicture',
            name='picture',
            field=models.ForeignKey(to='interviews.Picture'),
        ),
        migrations.AddField(
            model_name='interview',
            name='person',
            field=models.ForeignKey(to='interviews.Person'),
        ),
        migrations.AddField(
            model_name='interview',
            name='site',
            field=models.ForeignKey(default=2, to='sites.Site'),
        ),
        migrations.AddField(
            model_name='answer',
            name='interview',
            field=models.ForeignKey(to='interviews.Interview'),
        ),
        migrations.AddField(
            model_name='answer',
            name='related_pictures',
            field=models.ManyToManyField(to='interviews.Picture', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together=set([('interview', 'order')]),
        ),
    ]
