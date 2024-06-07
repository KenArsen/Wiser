from rest_framework import serializers
from apps.chat.models import Private, PrivateMessage


class InnerMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateMessage
        fields = ("id", "private", "content", "file", "posted_at")
        ref_name = "InnerMessage"


class PrivateListSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Private
        fields = ("id", "sender", "receiver")
        ref_name = 'PrivateList'

    def get_last_message(self, obj):
        last_message = obj.chat_messages.order_by("-posted_at").first()
        if last_message:
            return last_message.content
        return None


class PrivateDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Private
        fields = ("id", "sender", "receiver")
        ref_name = 'PrivateDetail'


class PrivateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Private
        exclude = ("id",)
        ref_name = 'PrivateCreate'


class PrivateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Private
        exclude = ("id",)
        ref_name = 'PrivateUpdate'
