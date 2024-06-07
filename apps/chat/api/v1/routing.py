from django.urls import path

from apps.chat.api.v1.consumers.group import GroupChatConsumer
from apps.chat.api.v1.consumers.private import PrivateChatConsumer

websocket_urlpatterns = [
    path("ws/chats/group/<int:group_id>/", GroupChatConsumer.as_asgi()),
    path("ws/chats/private/<int:receiver_id>/", PrivateChatConsumer.as_asgi()),
]
