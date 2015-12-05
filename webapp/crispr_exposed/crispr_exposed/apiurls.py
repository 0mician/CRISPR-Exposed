from django.conf.urls import patterns, include, url
from rest_framework import routers

import crispr.views

api = routers.DefaultRouter()
api.register(r'crispr/strains', crispr.views.StrainViewSet)
api.register(r'crispr/crispr_arrays', crispr.views.CrisprArrayViewSet)
api.register(r'crispr/crispr_entries', crispr.views.CrisprEntryViewSet)

urlpatterns = [
    url(r'^', include(api.urls)),
]
