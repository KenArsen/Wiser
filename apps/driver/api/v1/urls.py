from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.driver.api.v1.apis.driver import DriverViewSet

app_name = 'driver'

router = DefaultRouter()

router.register('', DriverViewSet, basename='roles')

urlpatterns = [
    path('', include(router.urls)),
]
