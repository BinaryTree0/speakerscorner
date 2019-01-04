from django.conf.urls import url

from .views import (
    ConferenceCreateView,
    ConferenceListView,
    ConferenceDetailView,
    SekcijeView,
    FileCreateView,
    RadoviListView,
    RecenzentListView,
)
urlpatterns = [
    url(r'radovi/(?P<pk>\d+)/$', RadoviListView.as_view(), name='radovi_list'),
    url(r'recenzent_list/(?P<pk>\d+)/$', RecenzentListView.as_view(), name='recenzent_list'),
    url(r'create$', ConferenceCreateView.as_view(), name='create'),
    url(r'create/(?P<pk>\d+)/file/$', FileCreateView.as_view(), name='create_file'),
    url(r'sekcije/(?P<pk>\d+)/$', SekcijeView.as_view(), name = 'sekcija'),
    url(r'(?P<pk>\d+)/$', ConferenceDetailView.as_view(), name = 'detail'),
    url(r'$', ConferenceListView.as_view(), name='custom-list'),
]
