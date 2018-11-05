from django.conf.urls import url


from .views import (
    ConferenceCreateView,
    ConferenceListView,
)
urlpatterns = [
    url(r'create$', ConferenceCreateView.as_view(), name='create'),
    url(r'$', ConferenceListView.as_view(), name='detail'),
]
