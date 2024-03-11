from django.urls import path

from .apis import (
    VehicleCreateAPI,
    VehicleDeleteAPI,
    VehicleDetailAPI,
    VehicleListAPI,
    VehicleUpdateAPI,
)

app_name = "vehicles"

urlpatterns = [
    path("", VehicleListAPI.as_view(), name="vehicle-list"),
    path("create/", VehicleCreateAPI.as_view(), name="vehicle-create"),
    path("<int:pk>/", VehicleDetailAPI.as_view(), name="vehicle-detail"),
    path("<int:pk>/update/", VehicleUpdateAPI.as_view(), name="vehicle-update"),
    path("<int:pk>/delete/", VehicleDeleteAPI.as_view(), name="vehicle-delete"),
]
