# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leonardo_store_faq', '0002_question_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productquestion',
            name='order',
            field=models.IntegerField(null=True, verbose_name='Order', blank=True),
        ),
        migrations.AlterField(
            model_name='productquestion',
            name='product',
            field=models.ForeignKey(related_name='questions', verbose_name='Product', to='catalogue.Product'),
        ),
        migrations.AlterField(
            model_name='productquestion',
            name='question',
            field=models.ForeignKey(related_name='product_questions', verbose_name='Question', to='leonardo_store_faq.Question'),
        ),
        migrations.AlterField(
            model_name='question',
            name='answer',
            field=models.TextField(verbose_name='Answer'),
        ),
        migrations.AlterField(
            model_name='question',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.TextField(verbose_name='Question text'),
        ),
    ]
