from django.core import signing
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from apps.user.models import User, Invitation
from api.serializers.user import UserSerializer, InvitationSerializer, ResetPasswordRequestSerializer, \
    ResetPasswordConfirmSerializer, UserRetrieveSerializer

from api.utils.permissions import IsSuperAdminUser

from django.core.mail import send_mail
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

import uuid
from rest_framework.decorators import action

from django.contrib.auth import authenticate
from wiser_load_board.settings import EMAIL_HOST_USER


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserRetrieveSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [AllowAny()]
        return [IsAuthenticated()]

    """Активация пользователя СуперАдмином"""
    @action(detail=False, methods=['POST'])
    def activate_by_email(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'Пользователь с таким email не найден.'}, status=status.HTTP_404_NOT_FOUND)

        if request.user.is_superuser:
            user.is_active = True
            user.save()
            return Response({'message': 'Пользователь активирован.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'У вас нет прав для активации пользователя.'}, status=status.HTTP_403_FORBIDDEN)


class InvitationView(APIView):
    permission_classes = (IsSuperAdminUser,)

    def post(self, request):
        serializer = InvitationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get('email')

            if Invitation.objects.filter(email=email, is_used=False).exists():
                return Response({"detail": "Invitation already sent to this email."},
                                status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create(email=email)
            invitation_token = str(uuid.uuid4())
            invitation = Invitation.objects.create(user=user, email=email, invitation_token=invitation_token)

            # Отправьте приглашение на электронную почту пользователя здесь.
            subject = 'Приглашение для регистрации'

            invitation_url = f'http://127.0.0.1:8000/api/users/setup-password/?token={invitation_token}'
            message = f'Для продолжении регистрации по ссылке: {invitation_url}'

            from_email = EMAIL_HOST_USER
            recipient_list = [email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return Response(InvitationSerializer(invitation).data, status=status.HTTP_201_CREATED)


class PasswordSetupView(APIView):
    def post(self, request, invitation_token):
        invitation = Invitation.objects.filter(invitation_token=invitation_token, is_used=False)
        if not invitation:
            return Response({
                "error": "This invitation url is used"
            })
        else:
            invitation = invitation.first()
        email = invitation.email
        password = request.data.get('password')
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
        token = signing.dumps({'user_id': user.id})
        return token

    def send_password_reset_email(self, email, reset_token):
        subject = 'Сброс пароля'

        reset_url = f'http://127.0.0.1:8000/api/users/reset-password/confirm/?token={reset_token}'
        message = f'Для сброса пароля перейдите по ссылке: {reset_url}'

        from_email = EMAIL_HOST_USER
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user1 = User.objects.get(email=email)
                reset_token = self.generate_reset_token(user1)
                self.send_password_reset_email(email, reset_token)
                return Response({'message': 'Email sent with reset instructions'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordConfirmView(generics.CreateAPIView):
    serializer_class = ResetPasswordConfirmSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            new_password = serializer.validated_data['password']
            user.set_password(new_password)
            user.save()

            subject = "Password Reset Confirmation"
            message = "Your password has been successfully reset."
            from_email = EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)

            return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
