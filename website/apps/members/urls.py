from django.conf.urls import url, include
from . import views

app_name='members'

urlpatterns = [
    url(r'^(?P<id>[0-9]+)/$', views.profile.as_view(), name='profile'),
    url(r'^(?P<id>[0-9]+)/addgroup$', views.addgroup.as_view(), name='addgroup'),
]
