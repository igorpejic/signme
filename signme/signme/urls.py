from django.conf.urls import include, url
from django.contrib import admin
from restful import views
from rest_framework.authtoken import views

urlpatterns = [
    url(r'^rest', include('restful.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('authemail.urls')),
]
