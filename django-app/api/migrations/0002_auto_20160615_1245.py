# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-15 12:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CropDiversity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('county_name', models.CharField(blank=True, max_length=64, null=True)),
                ('diversity_score', models.CharField(blank=True, max_length=64, null=True)),
            ],
            options={
                'db_table': 'crop_diversity',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ExportsByCountryRaw',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commodity', models.CharField(blank=True, max_length=64, null=True)),
                ('country', models.CharField(blank=True, max_length=64, null=True)),
                ('time', models.CharField(blank=True, max_length=64, null=True)),
                ('value', models.CharField(blank=True, max_length=64, null=True)),
            ],
            options={
                'db_table': 'exports_by_country_raw',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ExportsHistoricalCleanedAnnualTotals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commodity', models.CharField(blank=True, max_length=64, null=True)),
                ('time', models.CharField(blank=True, max_length=64, null=True)),
                ('value', models.CharField(blank=True, max_length=64, null=True)),
            ],
            options={
                'db_table': 'exports_historical_cleaned_annual_totals',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ExportsHistoricalCleanedMonthlyTotals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commodity', models.CharField(blank=True, max_length=64, null=True)),
                ('time', models.CharField(blank=True, max_length=64, null=True)),
                ('value', models.CharField(blank=True, max_length=64, null=True)),
            ],
            options={
                'db_table': 'exports_historical_cleaned_monthly_totals',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ExportsHistoricalRaw',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commodity', models.CharField(blank=True, max_length=64, null=True)),
                ('time', models.CharField(blank=True, max_length=64, null=True)),
                ('value', models.CharField(blank=True, max_length=64, null=True)),
            ],
            options={
                'db_table': 'exports_historical_raw',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ImportsByCountryRaw',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commodity', models.CharField(blank=True, max_length=64, null=True)),
                ('country', models.CharField(blank=True, max_length=64, null=True)),
                ('time', models.CharField(blank=True, max_length=64, null=True)),
                ('value', models.CharField(blank=True, max_length=64, null=True)),
            ],
            options={
                'db_table': 'imports_by_country_raw',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ImportsHistoricalCleanedAnnualTotals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commodity', models.CharField(blank=True, max_length=64, null=True)),
                ('time', models.CharField(blank=True, max_length=64, null=True)),
                ('value', models.CharField(blank=True, max_length=64, null=True)),
            ],
            options={
                'db_table': 'imports_historical_cleaned_annual_totals',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ImportsHistoricalCleanedMonthlyTotals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commodity', models.CharField(blank=True, max_length=64, null=True)),
                ('time', models.CharField(blank=True, max_length=64, null=True)),
                ('value', models.CharField(blank=True, max_length=64, null=True)),
            ],
            options={
                'db_table': 'imports_historical_cleaned_monthly_totals',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ImportsHistoricalRaw',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commodity', models.CharField(blank=True, max_length=64, null=True)),
                ('time', models.CharField(blank=True, max_length=64, null=True)),
                ('value', models.CharField(blank=True, max_length=64, null=True)),
            ],
            options={
                'db_table': 'imports_historical_raw',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='MetadataTest',
        ),
        migrations.DeleteModel(
            name='RegionLookupTest',
        ),
        migrations.DeleteModel(
            name='SubsidyDollarsTest',
        ),
    ]
