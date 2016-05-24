from django.contrib import admin
from .models import *

class PostAdminAnimals(admin.ModelAdmin):
    list_display = ("commodity","year","fips","animals")
    search_fields = ["commodity","year","fips","animals"]

class PostAdminCommodity(admin.ModelAdmin):
    list_display = ("commodity","year","fips","acres")
    search_fields = ["commodity","year","fips","acres"]

class PostAdminFarms(admin.ModelAdmin):
    list_display = ("commodity","year","fips","farms")
    search_fields = ["commodity","year","fips","farms"]

class PostAdminOainAcres(admin.ModelAdmin):
    list_display = ("commodity","year","fips","harvested_acres")
    search_fields = ["commodity","year","fips","harvested_acres"]

class PostAdminRegionLookup(admin.ModelAdmin):
    list_display = ("st_code","state","co_code","region","fips")
    search_fields = ["st_code","state","co_code","region","fips"]

class PostAdminSubsidyDollars(admin.ModelAdmin):
    list_display = ("commodity","year","fips","subsidy_dollars")
    search_fields = ["commodity","year","fips","subsidy_dollars"]

class PostAdminSubsidyRecipients(admin.ModelAdmin):
    list_display = ("commodity","year","fips","subsidy_recipients")
    search_fields = ["commodity","year","fips","subsidy_recipients"]

admin.site.register(NassAnimalsInventory, PostAdminAnimals)
admin.site.register(NassAnimalsSales, PostAdminAnimals)
admin.site.register(NassCommodityArea, PostAdminCommodity)
admin.site.register(NassCommodityFarms, PostAdminFarms)
admin.site.register(OainHarvestAcres, PostAdminOainAcres)
admin.site.register(RegionLookup, PostAdminRegionLookup)
admin.site.register(SubsidyDollars, PostAdminSubsidyDollars)
admin.site.register(SubsidyRecipients, PostAdminSubsidyRecipients)
