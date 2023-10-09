from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import User, Invitation
from .serializers import UserSerializer, InvitationSerializer

from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import uuid

from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser, IsAuthenticated)


class InvitationView(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request):
        email = request.data.get('email')

        if Invitation.objects.filter(email=email, is_used=False).exists():
            return Response({"detail": "Invitation already sent to this email."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(username=email)
        invitation_token = str(uuid.uuid4())
        invitation = Invitation.objects.create(user=user, email=email, invitation_token=invitation_token)

        # Отправьте приглашение на электронную почту пользователя здесь.
        subject = 'Приглашение для регистрации'
        message = f'Пожалуйста, перейдите по ссылке для завершения регистрации: {invitation_token}'
        from_email = 'stajer0206@gmail.com'
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        return Response(InvitationSerializer(invitation).data, status=status.HTTP_201_CREATED)


class PasswordSetupView(APIView):
    def post(self, request, invitation_token):
        invitation = get_object_or_404(Invitation, invitation_token=invitation_token, is_used=False)
        email = invitation.email
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)

        if user:
            invitation.is_used = True
            invitation.save()
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid password."}, status=status.HTTP_400_BAD_REQUEST)
