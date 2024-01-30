from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views.driver import DriverViewSet

router = DefaultRouter()

router.register('', DriverViewSet, basename='roles')

urlpatterns = [
    path('', include(router.urls)),
]
