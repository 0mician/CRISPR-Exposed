from django.conf.urls import include, url
from django.contrib import admin

import crispr_exposed.apiurls

urlpatterns = [
    url(r'^$', include('crispr.urls')),
    url(r'^rest-api/', include('crispr_exposed.apiurls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^crispr/', include('crispr.urls')),
]
