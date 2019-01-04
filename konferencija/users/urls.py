from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    #Authentication views
    url(r'validate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.ActivationView.as_view(),name='activate'),
    url(r'login/$',views.UserLoginView.as_view(),name='login'),
    #Password reset views
    url(r'reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',auth_views.PasswordResetConfirmView.as_view(template_name='user_reset_confirm.html'),name='password_reset_confirm'),
    url(r'reset/done/$',auth_views.PasswordResetView.as_view(template_name='user_reset_done.html'),name='reset-done'),
    url(r'reset/$',auth_views.PasswordResetView.as_view(template_name='user_reset_password.html',success_url = 'reset/done/'),name='reset-password'),

    #Password change views
    url(r'password-change/$',views.CustomPasswordChangeView.as_view(template_name='user_change_password.html'),name='user-change-password'),
    url(r'password_change/done/$',auth_views.PasswordChangeDoneView.as_view(template_name='user_change_done.html'),name='user-change-done'),

    #User views
    url(r'signup/$', views.UserCreateView.as_view(), name='signup'),
    url(r'update/(?P<pk>\d+)/$', views.UserUpdateView.as_view(), name='update'),
    url(r'detail/(?P<pk>\d+)/$', views.UserDetailView.as_view(), name='detail'),
    url(r'list/(?P<pk>\d+)/$', views.UserListView.as_view(), name='user_list'),

    #Home
    url(r'custom-list/$', views.CustomUserListView.as_view(), name='custom_user_list'),
    url(r'$', views.HomePageView.as_view(), name='home'),
]
