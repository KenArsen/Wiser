from django.urls import path

from .views.file import (
    FileCreateAPI,
    FileDeleteAPI,
    FileDetailAPI,
    FileUpdateAPI,
    ListAPIView,
)

app_name = "files"

urlpatterns = [
    path("", ListAPIView.as_view(), name="file-list"),
    path("create/", FileCreateAPI.as_view(), name="file-create"),
    path("<int:pk>/", FileDetailAPI.as_view(), name="file-detail"),
    path("<int:pk>/update/", FileUpdateAPI.as_view(), name="file-update"),
    path("<int:pk>/delete/", FileDeleteAPI.as_view(), name="file-destroy"),
]
