from django.core import signing
from rest_framework import serializers

from apps.user.models import Invitation, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ('email',)


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value


class ResetPasswordConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate_token(self, value):
        try:
            # Проверяем, действителен ли токен
            data = signing.loads(value, max_age=3600)  # Указывайте здесь желаемое время действия токена в секундах
            user_id = data.get('user_id')
            user = User.objects.get(id=user_id)
            self.user = user
        except (signing.SignatureExpired, signing.BadSignature, User.DoesNotExist):
            raise serializers.ValidationError("Invalid or expired token")
        return value
