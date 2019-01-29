from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from django.contrib.auth import views as auth_views
from website.apps.users import views as users_views

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),

    url(r'^home/', include('website.apps.users.urls', namespace='home')),
    url(r'^servers/', include('website.apps.servers.urls', namespace='servers')),
    url(r'^members/', include('website.apps.members.urls', namespace='members')),
    url(r'^groups/', include('website.apps.groups.urls', namespace='groups')),

    url(r'^$', users_views.index.as_view(), name='index'),
]
