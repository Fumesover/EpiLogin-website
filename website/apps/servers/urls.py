from django.conf.urls import url, include
from . import views

app_name='servers'

urlpatterns = [
    url(r'^$', views.list.as_view(), name='list'),
    url(r'^(?P<server_id>[0-9]+)/$', views.info.as_view(), name='info'),
]
