from django.urls import path
from apps.chat.api.v1.consumers.group_consumer import GroupChatConsumer

websocket_urlpatterns = [
    path(r'ws/chats/group/<int:group_id>/', GroupChatConsumer.as_asgi()),
]
