from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.user.api.v1.views.user import (
    InvitationView,
    PasswordSetupView,
    ResetPasswordConfirmView,
    ResetPasswordRequestView,
    UserViewSet,
)

app_name = "users"

router = DefaultRouter()

urlpatterns = [
    path("send-invitation/", InvitationView.as_view(), name="send-invitation"),
    path(
        "setup-password/<str:invitation_token>/",
        PasswordSetupView.as_view(),
        name="setup-password",
    ),
    path(
        "reset-password/",
        ResetPasswordRequestView.as_view(),
        name="reset-password-request",
    ),
    path(
        "reset-password/confirm/",
        ResetPasswordConfirmView.as_view(),
        name="reset-password-confirm",
    ),
    path(
        "activate_by_email/",
        UserViewSet.as_view({"post": "activate_by_email"}),
        name="user-activate-by-email",
    ),
]
router.register("", UserViewSet, basename="users")

urlpatterns += router.urls
