import uuid

from django.contrib.auth import authenticate
from django.core import signing
from django.core.mail import send_mail
from django.db import transaction
from django.urls import reverse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.common.permissions import IsSuperAdmin
from apps.user.api.v1.serializers.user_serializer import (
    InvitationSerializer,
    ResetPasswordConfirmSerializer,
    ResetPasswordRequestSerializer,
    RolesSerializer,
    UserActivationSerializer,
    UserCreateSerializer,
    UserListSerializer,
    UserRetrieveSerializer,
    UserSerializer,
)
from apps.user.models import Invitation, Roles, User
from wiser_load_board.settings import EMAIL_HOST_USER


class RolesViewSet(ModelViewSet):
    queryset = Roles.objects.all()
    serializer_class = RolesSerializer
    permission_classes = (IsSuperAdmin,)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsSuperAdmin,)

    def get_serializer_class(self):
        if self.action == "retrieve" or self.action == "me":
            return UserRetrieveSerializer
        elif self.action == "list":
            return UserListSerializer
        elif self.action == "activate_by_email":
            return UserActivationSerializer
        elif self.action == "create":
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ["create"]:
            return [AllowAny()]
        return [IsSuperAdmin()]

    @action(["get"], detail=False)
    def me(self, request, *args, **kwargs):
        queryset = User.objects.filter(id=request.user.id)
        user = get_object_or_404(queryset)
        serializer = self.get_serializer(user, context={"request": request})
        return Response(serializer.data)

    @action(detail=False, methods=["POST"])
    def activate_by_email(self, request):
        """Активация пользователя СуперАдмином"""
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"message": "User with this email was not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.user.is_superuser:
            user.is_active = True
            user.save()
            return Response({"message": "User activated."}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "You do not have rights to activate the user."}, status=status.HTTP_403_FORBIDDEN
            )


class InvitationView(APIView):
    permission_classes = (IsSuperAdmin,)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING, description="Email address for the invitation"),
            },
            required=["email"],
        ),
        responses={
            201: "Created - Invitation sent successfully",
            400: "Bad Request - Invitation already sent to this email",
        },
        operation_summary="Send Invitation",
        operation_description="Send an invitation to the specified email address.",
    )
    @transaction.atomic()
    def post(self, request):
        serializer = InvitationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get("email")
            if Invitation.objects.filter(email=email, is_used=False).exists():
                return Response(
                    {"detail": "Invitation already sent to this email."}, status=status.HTTP_400_BAD_REQUEST
                )
            user = User.objects.create(email=email)
            invitation_token = str(uuid.uuid4())
            invitation = Invitation.objects.create(user=user, email=email, invitation_token=invitation_token)
            # Отправьте приглашение на электронную почту пользователя здесь.
            subject = "Invitation to register"
            invitation_url = request.build_absolute_uri(
                reverse("api:users:setup-password", kwargs={"invitation_token": invitation_token})
            )
            message = f"To continue registration follow the link: {invitation_url}"
            from_email = EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            return Response(InvitationSerializer(invitation).data, status=status.HTTP_201_CREATED)


class PasswordSetupView(APIView):
    def post(self, request, invitation_token):
        invitation = Invitation.objects.filter(invitation_token=invitation_token, is_used=False)
        if not invitation:
            return Response({"error": "This invitation url is used"})
        else:
            invitation = invitation.first()
        email = invitation.email
        password = request.data.get("password")
        if not password:
            return Response({"password": "is required field"})
        user_password = User.objects.get(email=email)
        user_password.set_password(password)
        user_password.save()
        user = authenticate(request, email=email, password=password)
        if user:
            invitation.is_used = True
            invitation.save()
            subject = "Password Change Confirmation"
            message = "Your password has been successfully changed."
            from_email = EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)
            return Response({"success": "Your password succussfully changed!"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid password."}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordRequestView(generics.CreateAPIView):
    serializer_class = ResetPasswordRequestSerializer

    def generate_reset_token(self, user):
        token = signing.dumps({"user_id": user.id})
        return token

    def send_password_reset_email(self, email, reset_token, request):
        subject = "Password reset"
        reset_url = request.build_absolute_uri(reverse("api:users:reset-password-confirm")) + f"?token={reset_token}"

        message = f"To reset your password, follow the link: {reset_url}"
        from_email = EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                user1 = User.objects.get(email=email)
                reset_token = self.generate_reset_token(user1)
                self.send_password_reset_email(email, reset_token, request)
                return Response({"message": "Email sent with reset instructions"}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordConfirmView(generics.CreateAPIView):
    serializer_class = ResetPasswordConfirmSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            new_password = serializer.validated_data["password"]
            user.set_password(new_password)
            user.save()
            subject = "Password Reset Confirmation"
            message = "Your password has been successfully reset."
            from_email = EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)
            return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
