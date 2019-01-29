from django.conf.urls import url, include
from . import views

app_name='servers'

urlpatterns = [
    url(r'^$', views.list.as_view(), name='list'),
    url(r'^(?P<server_id>[0-9]+)/$', views.info.as_view(), name='info'),
    url(r'^(?P<server_id>[0-9]+)/ban$', views.ban.as_view(), name='ban'),

    url(r'^update$', views.update.as_view(), name='update'),
    url(r'^push$', views.push.as_view(), name='push'),
]
