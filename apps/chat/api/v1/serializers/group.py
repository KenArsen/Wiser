from rest_framework import serializers

from apps.chat.models import Group, GroupMessage
from apps.user.models import User


class InnerMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMessage
        fields = ("id", "sender", "content", "file", "posted_at")
        ref_name = "InnerMessage"


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "phone_number")
        ref_name = "Member"


class GroupListSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ("id", "name", "last_message")
        ref_name = "GroupList"

    def get_last_message(self, obj):
        last_message = obj.messages.order_by("-posted_at").first()
        if last_message:
            return last_message.content
        return None


class GroupDetailSerializer(serializers.ModelSerializer):
    messages = InnerMessageSerializer(many=True, read_only=True)
    members = MemberSerializer(many=True)

    class Meta:
        model = Group
        fields = ("id", "name", "creator", "description", "members", "image", "messages")
        ref_name = "GroupDetail"


class GroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        exclude = ("id",)
        ref_name = "GroupCreate"


class GroupUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"
        ref_name = "GroupUpdate"


class AddUserToGroupSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Group
        fields = ("user_id",)
        ref_name = "AddUserToGroup"


class RemoveUserFromGroupSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Group
        fields = ("user_id",)
        ref_name = "RemoveUserFromGroup"
