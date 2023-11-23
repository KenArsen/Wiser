from rest_framework.routers import DefaultRouter
from django.urls import path

from api.views.user import UserViewSet, InvitationView, PasswordSetupView, ResetPasswordRequestView, \
    ResetPasswordConfirmView, RolesViewSet, DriverFilterViewSet

router = DefaultRouter()

urlpatterns = [
    path('send-invitation/', InvitationView.as_view(), name='send-invitation'),
    path('setup-password/<str:invitation_token>/', PasswordSetupView.as_view(), name='setup-password'),
    path('reset-password/', ResetPasswordRequestView.as_view(), name='reset-password-request'),
    path('reset-password/confirm/', ResetPasswordConfirmView.as_view(), name='reset-password-confirm'),
    path('activate_by_email/', UserViewSet.as_view({'post': 'activate_by_email'}), name='user-activate-by-email'),
]
router.register('drivers', DriverFilterViewSet, basename='drivers')
router.register('role', RolesViewSet, basename='roles')
router.register('', UserViewSet, basename='users')


urlpatterns += router.urls


































