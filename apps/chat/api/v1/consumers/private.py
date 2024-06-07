import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from apps.chat.models import Private, PrivateMessage
from apps.user.models import User


class PrivateChatConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.receiver = None
        self.private_name = None

    async def connect(self):
        self.receiver = self.scope["url_route"]["kwargs"]["receiver_id"]
        self.private_name = f"private_{self.scope['user'].id}_{self.receiver}"

        # Проверяем, аутентифицирован ли пользователь
        if not self.scope["user"].is_authenticated:
            await self.close()
            return

        # Присоединяемся к приватному чату
        await self.channel_layer.group_add(self.private_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Покидаем приватный чат
        await self.channel_layer.group_discard(self.private_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        if bytes_data:
            file_content = bytes_data
            message_content = None
        else:
            data = json.loads(text_data)
            message_content = data.get("message")
            file_content = None

        # Сохраняем сообщение в базе данных
        message = await self.save_message(message_content, file_content)

        # Отправляем сообщение обратно клиенту
        await self.channel_layer.group_send(
            self.private_name,
            {
                "type": "chat_message",
                "message": message_content,
                "file": file_content,
                "sender": f'{self.scope["user"].first_name} {self.scope["user"].last_name}',
                "date": message.posted_at.isoformat(),
            },
        )

    async def chat_message(self, event):
        # Отправляем сообщение клиенту
        await self.send_json(event)

    @database_sync_to_async
    def save_message(self, message_content, file_content):
        try:
            sender = self.scope["user"]
            receiver = get_object_or_404(User, pk=self.receiver)
            private, created = Private.objects.get_or_create(
                sender=sender, receiver=receiver
            )
            message = PrivateMessage.objects.create(
                private=private, content=message_content, file=file_content
            )
            return message
        except ObjectDoesNotExist:
            # Обработка случая, когда пользователь не существует
            return None
