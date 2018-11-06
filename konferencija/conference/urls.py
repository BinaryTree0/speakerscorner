from django.conf.urls import url


from .views import (
    ConferenceCreateView,
    ConferenceListView,
    ConferenceDetailView,
)
urlpatterns = [
    url(r'create$', ConferenceCreateView.as_view(), name='create'),
    url(r'(?P<pk>\d+)/$', ConferenceDetailView.as_view(), name = 'detail'),
    url(r'$', ConferenceListView.as_view(), name='list'),
]
