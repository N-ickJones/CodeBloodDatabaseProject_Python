"""core_settings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.conf.urls import url
# from django.urls import path   # ,include
# from django.contrib import admin
# from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
# from . import views

from django.urls import path, re_path
# from django.contrib import admin
from core_app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('search/', views.search_view, name='search'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.activate, name='activate'),
    path('email_confirm_complete/', views.email_confirm_complete, name='email_confirm_complete'),
    path('password_reset/', views.password_reset_form, name='password_reset'),
    re_path(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.password_reset_confirm, name='password_reset_confirm'),
    path('password_reset_complete', views.password_reset_complete, name='password_reset_complete'),
    path('password_change/', views.password_change_form, name='password_change'),
    path('password_change_complete/', views.password_change_complete, name='password_change_complete'),
    path('profile/', views.profile_view, name='profile'),
    path('settings/', views.setting_view, name='settings'),
    path('username_recovery/', views.username_recovery, name='username_recovery'),
    path('invalid_activation_code/', views.username_recovery, name='invalid_activation_code'),
    re_path(r'^activate_medical_staff/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.activate_medical_staff, name='activate_medical_staff'),
    path('patient_forms', views.patient_forms, name='patient_forms'),
    path('patient_forms_viewing', views.patient_forms_viewing, name='patient_forms_viewing'),
    path('reviews', views.reviews, name='reviews'),
    path('vials', views.vials_view, name='vials')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


"""
url(r'^$', auth_views.login, {'template_name': 'Base-Content/base.html'}, name='signin'),
url(r'^logout/$', auth_views.logout, {'next_page': 'home'}, name='logout'),

# Password Reset
url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
       auth_views.password_reset_confirm, name='password_reset_confirm'),
url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

url(r'^logout/$', auth_views.logout, {'template_name': 'logged_out.html'}, name='logout'),
url(r'^login/$', auth_views.login, {'template_name': 'core/login.html'}, name='login'), different temp
url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'), next page
url('^', include('django.contrib.auth.urls')), # for all auth

"""
