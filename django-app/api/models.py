# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Metadata(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    table_name = models.CharField(max_length=64, blank=True, null=True)
    unit = models.CharField(max_length=64, blank=True, null=True)
    field = models.CharField(max_length=64, blank=True, null=True)
    source_name = models.CharField(max_length=256, blank=True, null=True)
    source_link = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'metadata'


# Managed version of Metadata model for testing only (auto-generated pk)
class MetadataTest(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    table_name = models.CharField(max_length=64, blank=True, null=True)
    unit = models.CharField(max_length=64, blank=True, null=True)
    field = models.CharField(max_length=64, blank=True, null=True)
    source_name = models.CharField(max_length=256, blank=True, null=True)
    source_link = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        db_table = 'metadata_test'


class NassAnimalsInventory(models.Model):
    commodity = models.CharField(max_length=64, blank=True, null=True)
    year = models.SmallIntegerField(blank=True, null=True)
    fips = models.IntegerField(blank=True, null=True)
    animals = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nass_animals_inventory'


class NassAnimalsSales(models.Model):
    commodity = models.CharField(max_length=64, blank=True, null=True)
    year = models.SmallIntegerField(blank=True, null=True)
    fips = models.IntegerField(blank=True, null=True)
    animals = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nass_animals_sales'


class NassCommodityArea(models.Model):
    commodity = models.CharField(max_length=64, blank=True, null=True)
    year = models.SmallIntegerField(blank=True, null=True)
    fips = models.IntegerField(blank=True, null=True)
    acres = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nass_commodity_area'


class NassCommodityFarms(models.Model):
    commodity = models.CharField(max_length=64, blank=True, null=True)
    year = models.SmallIntegerField(blank=True, null=True)
    fips = models.IntegerField(blank=True, null=True)
    farms = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nass_commodity_farms'


class OainHarvestAcres(models.Model):
    commodity = models.CharField(max_length=64, blank=True, null=True)
    year = models.SmallIntegerField(blank=True, null=True)
    fips = models.IntegerField(blank=True, null=True)
    harvested_acres = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oain_harvest_acres'


class RegionLookup(models.Model):
    st_code = models.IntegerField(blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    co_code = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    region = models.CharField(max_length=90, blank=True, null=True)
    fips = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'region_lookup'


# Managed version of RegionLookup model for testing only (auto-generated pk)
class RegionLookupTest(models.Model):
    st_code = models.IntegerField(blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    co_code = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    region = models.CharField(max_length=90, blank=True, null=True)
    fips = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'region_lookup_test'


class SpatialRefSys(models.Model):
    srid = models.IntegerField(primary_key=True)
    auth_name = models.CharField(max_length=256, blank=True, null=True)
    auth_srid = models.IntegerField(blank=True, null=True)
    srtext = models.CharField(max_length=2048, blank=True, null=True)
    proj4text = models.CharField(max_length=2048, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'spatial_ref_sys'


class SubsidyDollars(models.Model):
    commodity = models.CharField(max_length=64, blank=True, null=True)
    year = models.SmallIntegerField(blank=True, null=True)
    fips = models.IntegerField(blank=True, null=True)
    subsidy_dollars = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subsidy_dollars'


# Managed version of SubsidyDollars model for testing only (auto-generated pk)
class SubsidyDollarsTest(models.Model):
    commodity = models.CharField(max_length=64, blank=True, null=True)
    year = models.SmallIntegerField(blank=True, null=True)
    fips = models.IntegerField(blank=True, null=True)
    subsidy_dollars = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'subsidy_dollars_test'


class SubsidyRecipients(models.Model):
    commodity = models.CharField(max_length=64, blank=True, null=True)
    year = models.SmallIntegerField(blank=True, null=True)
    fips = models.IntegerField(blank=True, null=True)
    subsidy_recipients = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subsidy_recipients'
