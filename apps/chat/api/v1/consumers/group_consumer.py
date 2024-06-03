import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from apps.chat.models import Group, Message
from channels.db import database_sync_to_async


class GroupChatConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, kwargs)
        self.user = None
        self.group_id = None
        self.group_name = None

    async def connect(self):
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.group_name = f"group_{self.group_id}"

        # Проверяем, имеет ли пользователь доступ к этой группе
        if not self.scope['user'].joined_groups.filter(id=self.group_id).exists():
            await self.close()
            return

        # Присоединяемся к группе чата
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Покидаем группу чата
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        data = json.loads(text_data)
        message_content = data['message']

        # Сохраняем сообщение в базе данных
        message = await self.save_message(message_content)

        # Отправляем сообщение обратно клиенту
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message': message_content,
                'sender': f'{self.scope["user"].first_name} {self.scope["user"].last_name}',
                'sender_role': self.scope['user'].role,
                'sender_phone': self.scope['user'].phone_number,
                'date': message.date_posted
            }
        )

    async def chat_message(self, event):
        # Отправляем сообщение клиенту
        await self.send_json(event)

    async def save_message(self, message):
        # Сохраняем сообщение в базе данных
        group = await self.get_group()
        sender = self.scope['user']
        return await database_sync_to_async(Message.objects.create)(group=group, sender=sender, content=message)

    async def get_group(self):
        # Получаем группу чата
        return await database_sync_to_async(Group.objects.get)(id=self.group_id)