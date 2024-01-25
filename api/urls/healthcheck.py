from django.urls import path

from api.views.healthcheck import HealCheckView

urlpatterns = [
    path("", HealCheckView.as_view(), name="health_check"),
]
