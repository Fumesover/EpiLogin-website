from django.urls import path, include
from rest_framework import routers
from . import views

app_name='api'

router = routers.DefaultRouter()

router.register(r'updates', views.UpdateViewSet)
router.register(r'members', views.MemberViewSet)
router.register(r'servers', views.ServerViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
