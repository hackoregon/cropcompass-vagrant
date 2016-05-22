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
# from django.contrib import admin
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'metadata', views.MetadataViewSet)

# Wire up our API using automatic URL routing
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^data/nass_animals_sales/$', views.NassAnimalsSalesList.as_view()),
    url(r'^data/subsidy_dollars/$', views.SubsidyDollarsList.as_view()),
    url(r'^table/subsidy_dollars/$', views.SubsidyDollarsTable.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
