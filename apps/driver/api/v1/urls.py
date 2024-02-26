from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.driver.api.v1.apis.driver_apis import DriverViewSet

app_name = "drivers"

router = DefaultRouter()
router.register("", DriverViewSet, basename="roles")

urlpatterns = [
    path("", include(router.urls)),
]
