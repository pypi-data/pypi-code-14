# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0012_product_product_backend_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(null=True, blank=True)),
                ('product', models.ForeignKey(related_name='questions', to='catalogue.Product')),
            ],
            options={
                'verbose_name': 'Product question',
                'verbose_name_plural': 'Product questions',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_text', models.TextField()),
                ('answer', models.TextField()),
            ],
            options={
                'verbose_name': 'question',
                'verbose_name_plural': 'questions',
            },
        ),
        migrations.AddField(
            model_name='productquestion',
            name='question',
            field=models.ForeignKey(related_name='product_questions', to='leonardo_store_faq.Question'),
        ),
    ]
