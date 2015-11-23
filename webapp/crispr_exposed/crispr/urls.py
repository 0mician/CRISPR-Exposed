from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search_result/$', views.search_result, name='search_result'),
    url(r'^details/(?P<slug>.*?)/$', views.crispr_details, name='crispr_details'),
]
