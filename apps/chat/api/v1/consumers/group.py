import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.core.exceptions import ObjectDoesNotExist

from apps.chat.models import Group, Message


class GroupChatConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.group_id = None
        self.group_name = None

    async def connect(self):
        self.group_id = self.scope["url_route"]["kwargs"]["group_id"]
        self.group_name = f"group_{self.group_id}"

        # Проверяем, аутентифицирован ли пользователь
        if not self.scope["user"].is_authenticated:
            await self.close()
            return

        # Проверяем, имеет ли пользователь доступ к этой группе
        if not await self.user_in_group(self.scope["user"], self.group_id):
            await self.close()
            return

        # Присоединяемся к группе чата
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Покидаем группу чата
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

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
            self.group_name,
            {
                "type": "chat_message",
                "message": message_content,
                "file": file_content,
                "sender": f'{self.scope["user"].first_name} {self.scope["user"].last_name}',
                "sender_role": self.scope["user"].role,
                "sender_phone": self.scope["user"].phone_number,
                "date": message.date_posted.isoformat(),
            },
        )

    async def chat_message(self, event):
        # Отправляем сообщение клиенту
        await self.send_json(event)

    @database_sync_to_async
    def save_message(self, message_content, file_content):
        try:
            group = Group.objects.get(id=self.group_id)
            sender = self.scope["user"]
            message = Message.objects.create(group=group, sender=sender, content=message_content, file=file_content)
            return message
        except ObjectDoesNotExist:
            # Обработка случая, когда группа не существует
            return None

    @database_sync_to_async
    def user_in_group(self, user, group_id):
        return user.chat_groups.filter(id=group_id).exists()
