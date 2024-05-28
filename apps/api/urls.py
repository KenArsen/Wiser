from django.conf import settings
from django.urls import include, path, re_path
from django.views.static import serve
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = "api"


class HealthCheckView(APIView):
    @swagger_auto_schema(
        tags=["HealthCheck"],
        operation_summary="Health Check",
        operation_description="Check the health status of the application",
        security=[],
        responses={200: openapi.Response(description="OK")},
    )
    def get(self, request, *args, **kwargs):
        return Response({"status": "ok"}, status=status.HTTP_200_OK)


# apps
urlpatterns = [
    path("users/", include("apps.user.api.v1.urls", namespace="users")),
    path("drivers/", include("apps.driver.api.v1.urls", namespace="drivers")),
    path("vehicles/", include("apps.vehicle.api.v1.urls", namespace="vehicles")),
    path("orders/", include("apps.order.api.v1.urls", namespace="orders")),
    path("healthcheck/", HealthCheckView.as_view(), name="healthcheck"),
]

# libraries
urlpatterns += [
    re_path(
        r"^static/(?P<path>.*)$",
        serve,
        {"document_root": settings.STATIC_ROOT, "show_indexes": settings.DEBUG},
    ),
    re_path(
        r"^api/v1/media/(?P<path>.*)$",
        serve,
        {"document_root": settings.MEDIA_ROOT, "show_indexes": settings.DEBUG},
    ),
]

# token
urlpatterns += [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
