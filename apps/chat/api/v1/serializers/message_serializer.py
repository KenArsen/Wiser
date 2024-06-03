from rest_framework import serializers

from apps.chat.models import Message


class MessageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
        ref_name = "MessageList"


class MessageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
        ref_name = "MessageDetail"


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
        ref_name = "MessageCreate"


class MessageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
        ref_name = "MessageUpdate"
