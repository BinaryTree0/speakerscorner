from django.conf.urls import url


from .views import (
    AboutPageView,
    HomePageView,
)
urlpatterns = [
    url(r'about$', AboutPageView.as_view(), name='about'),
    url(r'$', HomePageView.as_view(), name='home'),
]
