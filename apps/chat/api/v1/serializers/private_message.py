from rest_framework import serializers

from apps.chat.models import PrivateMessage


class PrivateMessageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateMessage
        fields = ("id", "private", "content", "file", "posted_at")
        ref_name = "PrivateMessageList"


class PrivateMessageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateMessage
        fields = ("id", "private", "content", "file", "posted_at")
        ref_name = "PrivateMessageDetail"


class PrivateMessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateMessage
        exclude = ("id",)
        ref_name = "PrivateMessageCreate"


class PrivateMessageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateMessage
        exclude = ("id",)
        ref_name = "PrivateMessageUpdate"
