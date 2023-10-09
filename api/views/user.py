from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.user.models import User, Invitation
from api.serializers.user import UserSerializer, InvitationSerializer

from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import uuid

from django.contrib.auth import authenticate
from wiser_load_board.settings import EMAIL_HOST_USER


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser, IsAuthenticated)


class InvitationView(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request):
        serializer = InvitationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get('email')

            if Invitation.objects.filter(email=email, is_used=False).exists():
                return Response({"detail": "Invitation already sent to this email."}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create(email=email)
            invitation_token = str(uuid.uuid4())
            invitation = Invitation.objects.create(user=user, email=email, invitation_token=invitation_token)

            # Отправьте приглашение на электронную почту пользователя здесь.
            subject = 'Приглашение для регистрации'
            message = f'Пожалуйста, перейдите по ссылке для завершения регистрации: {invitation_token}'
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
            return Response({"success": "Your password succussfully changed!"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid password."}, status=status.HTTP_400_BAD_REQUEST)