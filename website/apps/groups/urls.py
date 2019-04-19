from django.conf.urls import url, include
from . import views

app_name='groups'

urlpatterns = [
    url(r'^deleteban/(?P<pk>[0-9]+)/$', views.deleteban.as_view(), name='deleteban'),
    url(r'^deletegroup/(?P<pk>[0-9]+)/$', views.deletegroup.as_view(), name='deletegroup'),

    url(r'^updates/$', views.updates.as_view(), name='updates'),
]
