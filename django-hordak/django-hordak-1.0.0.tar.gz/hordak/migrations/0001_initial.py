# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-13 11:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_smalluuid.models
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', django_smalluuid.models.SmallUUIDField(default=django_smalluuid.models.UUIDDefault(), editable=False, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=3)),
                ('_type', models.CharField(blank=True, choices=[('AS', 'Asset'), ('LI', 'Liability'), ('IN', 'Income'), ('EX', 'Expense'), ('EQ', 'Equity')], max_length=2)),
                ('has_statements', models.BooleanField(default=False, help_text='Does this account have statements to reconcile against. This is typically the case for bank accounts.')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='hordak.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Leg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', django_smalluuid.models.SmallUUIDField(default=django_smalluuid.models.UUIDDefault(), editable=False, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, help_text='Record debits as positive, credits as negative', max_digits=13)),
                ('description', models.TextField(blank=True, default='')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='legs', to='hordak.Account')),
            ],
        ),
        migrations.CreateModel(
            name='StatementImport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', django_smalluuid.models.SmallUUIDField(default=django_smalluuid.models.UUIDDefault(), editable=False, unique=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('bank_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imports', to='hordak.Account')),
            ],
        ),
        migrations.CreateModel(
            name='StatementLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', django_smalluuid.models.SmallUUIDField(default=django_smalluuid.models.UUIDDefault(), editable=False, unique=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('date', models.DateField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=13)),
                ('description', models.TextField(blank=True, default='')),
                ('statement_import', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='hordak.StatementImport')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', django_smalluuid.models.SmallUUIDField(default=django_smalluuid.models.UUIDDefault(), editable=False, unique=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, help_text='The creation date of this transaction object')),
                ('date', models.DateField(default=django.utils.timezone.now, help_text='The date on which this transaction occurred')),
                ('description', models.TextField(blank=True, default='')),
            ],
        ),
        migrations.AddField(
            model_name='statementline',
            name='transaction',
            field=models.ForeignKey(blank=True, default=None, help_text='Reconcile this statement line to this transaction', null=True, on_delete=django.db.models.deletion.CASCADE, to='hordak.Transaction'),
        ),
        migrations.AddField(
            model_name='leg',
            name='transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='legs', to='hordak.Transaction'),
        ),
        migrations.AlterUniqueTogether(
            name='account',
            unique_together=set([('parent', 'code')]),
        ),
    ]
