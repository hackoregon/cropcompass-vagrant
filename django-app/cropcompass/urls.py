"""cropcompass URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from api import views
from django.contrib import admin

# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^$', views.EndpointIndexView.as_view(), name='endpoint_index'),
    url(r'^list/$', views.EndpointIndexView.as_view(), name='endpoint_index'),
    url(r'^metadata/$', views.MetadataView.as_view(), name='metadata'),
    url(r'^table/county_stats/$', views.CountyStatisticsList.as_view(), name='county_stats'),
    url(r'^data/nass_animals_sales/$', views.NassAnimalsSalesList.as_view(), name='nass_animals_sales'),
    url(r'^data/subsidy_dollars/$', views.SubsidyDollarsList.as_view(), name='subsidy_dollars_data'),
    url(r'^data/subsidy_recipients/$', views.SubsidyRecipientsList.as_view(), name='subsidy_recipients_data'),
    url(r'^data/commodity_area/$', views.NassCommodityAreaList.as_view(), name='nass_commodity_area_list'),
    url(r'^data/commodity_farms/$', views.NassCommodityFarmsList.as_view(), name='nass_commodity_farms_list'),
    url(r'^data/oain_harvest_acres/$', views.OainHarvestAcresList.as_view(), name='oain_harvest_acres_list'),
    url(r'^table/subsidy_dollars/$', views.SubsidyDollarsTable.as_view(), name='subsidy_dollars_table'),
    url(r'^table/subsidy_dollars_timeline/$', views.SubsidyDollarsTimeline.as_view(), name='subsidy_dollars_timeline'),
    url(r'^table/commodity_area/$', views.CommodityAreaTable.as_view(), name='nass_commodity_area_table'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^table/subsidy_dollars_top5fips/$', views.SubsidyDollarsTopFiveCounties.as_view(), name='subsidy_dollars_top_counties'),
    url(r'^table/subsidy_dollars_top5crops/$', views.SubsidyDollarsTopFiveCommodities.as_view(), name='subsidy_dollars_top_commodities'),
    url(r'^data/crop_diversity/$', views.CropDiversityList.as_view(), name='crop_diversity_data'),
]
