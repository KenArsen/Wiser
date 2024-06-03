from rest_framework import generics
from apps.chat.models import Message
from apps.chat.api.v1.serializers import (
    MessageListSerializer,
    MessageDetailSerializer,
    MessageCreateSerializer,
    MessageUpdateSerializer,
)


class MessageBaseAPI(generics.GenericAPIView):
    queryset = Message.objects.all()
    permission_classes = None


class MessageListAPI(MessageBaseAPI, generics.ListCreateAPIView):
    serializer_class = MessageListSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class MessageDetailAPI(MessageBaseAPI, generics.RetrieveAPIView):
    serializer_class = MessageDetailSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class MessageCreateAPI(MessageBaseAPI, generics.CreateAPIView):
    serializer_class = MessageCreateSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class MessageUpdateAPI(MessageBaseAPI, generics.UpdateAPIView):
    serializer_class = MessageUpdateSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class MessageDeleteAPI(MessageBaseAPI, generics.DestroyAPIView):
    serializer_class = MessageDetailSerializer

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
