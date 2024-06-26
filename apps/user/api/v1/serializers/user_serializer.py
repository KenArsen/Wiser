from django.core import signing
from rest_framework import serializers

from apps.user.models import Invitation, Roles, User


class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ("id", "name")
        read_only_fields = ("id",)
        ref_name = "Roles"


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email")
        ref_name = "UserList"


class UserRetrieveSerializer(serializers.ModelSerializer):
    role = RolesSerializer(read_only=True)

    class Meta:
        model = User
        exclude = (
            "password",
            "user_permissions",
            "groups",
            "lat",
            "lon",
            "last_login",
            "created_at",
            "updated_at",
            "is_superuser",
        )
        ref_name = "UserRetrieve"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password", "user_permissions", "groups")
        ref_name = "User"


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "password", "phone_number", "first_name", "last_name", "role")
        read_only_fields = ("id",)
        extra_kwargs = {"password": {"write_only": True}}
        ref_name = "UserCreate"

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_active = False
        user.save()
        return user


class UserActivationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email",)
        ref_name = "UserActivation"


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ("email",)
        ref_name = "Invitation"


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
            data = signing.loads(value, max_age=3600)
            user_id = data.get("user_id")
            user = User.objects.get(id=user_id)
            self.user = user
        except (signing.SignatureExpired, signing.BadSignature, User.DoesNotExist):
            raise serializers.ValidationError("Invalid or expired token")
        return value
