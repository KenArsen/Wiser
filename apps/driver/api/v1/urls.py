from django.urls import path

from apps.driver.api.v1.views.driver import (
    DriverActivateAPI,
    DriverCreateAPI,
    DriverDeactivateAPI,
    DriverDeleteAPI,
    DriverDetailAPI,
    DriverFilterAPI,
    DriverListAPI,
    DriverUpdateAPI,
)

app_name = "drivers"

urlpatterns = [
    path("", DriverListAPI.as_view(), name="driver-list"),
    path("filter/", DriverFilterAPI.as_view(), name="driver-filter"),
    path("create/", DriverCreateAPI.as_view(), name="driver-create"),
    path("<int:pk>/", DriverDetailAPI.as_view(), name="driver-details"),
    path("<int:pk>/update/", DriverUpdateAPI.as_view(), name="driver-update"),
    path("<int:pk>/delete/", DriverDeleteAPI.as_view(), name="driver-delete"),
    path("<int:pk>/activate/", DriverActivateAPI.as_view(), name="driver-activate"),
    path("<int:pk>/deactivate/", DriverDeactivateAPI.as_view(), name="driver-deactivate"),
]
