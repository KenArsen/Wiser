from rest_framework.routers import DefaultRouter
from django.urls import path

from api.views.user import UserViewSet, InvitationView, PasswordSetupView, ResetPasswordRequestView, ResetPasswordConfirmView


router = DefaultRouter()

urlpatterns = [
    path('send-invitation/', InvitationView.as_view(), name='send-invitation'),
    path('setup-password/<str:invitation_token>/', PasswordSetupView.as_view(), name='setup-password'),
    path('reset-password/', ResetPasswordRequestView.as_view(), name='reset-password-request'),
    path('reset-password/confirm/', ResetPasswordConfirmView.as_view(), name='reset-password-confirm'),
]

router.register('', UserViewSet, basename='users')

urlpatterns += router.urls


































