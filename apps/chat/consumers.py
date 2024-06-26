import django

django.setup()  # noqa

import logging  # noqa
from json import JSONDecodeError  # noqa

from asgiref.sync import async_to_sync, sync_to_async  # noqa
from channels.db import database_sync_to_async  # noqa
from channels.generic.websocket import AsyncJsonWebsocketConsumer  # noqa
from channels.layers import get_channel_layer  # noqa
from django.utils import timezone  # noqa

from apps.chat.models import Conversation, Message  # noqa
from apps.chat.serializers import ChatMessageSerializer  # noqa
from apps.users.models import User  # noqa


@database_sync_to_async
def refresh_user_from_db(user):
    user.refresh_from_db()
    return user


@sync_to_async
def send_user_status_notification(user):
    channel_layer = get_channel_layer()

    for online_user in User.objects.filter(is_online=True).exclude(id=user.id):
        async_to_sync(channel_layer.group_send)(
            f"user_{online_user.id}",
            {
                "type": "user_status",
                "user_id": user.id,
                "is_online": user.is_online,
                "last_seen": None if user.is_online else user.last_seen.strftime("%d.%m.%Y %H:%M:%S"),
            },
        )


@database_sync_to_async
def update_user_online_status(user_id):
    User.objects.filter(id=user_id).update(is_online=True)


@database_sync_to_async
def update_user_offline_status(user_id):
    User.objects.filter(id=user_id).update(is_online=False, last_seen=timezone.now())


@database_sync_to_async
def create_message(data, user):
    serializer = ChatMessageSerializer(data=data, context={"domain": data.get("domain"), "user": user})
    if serializer.is_valid():
        serializer.save()
        return True, serializer.data
    else:
        logging.error(serializer.errors)
        return False, serializer.errors


@database_sync_to_async
def send_message_to_user(conversation_id, sender_id, message_data):
    try:
        conversation = Conversation.objects.get(id=conversation_id)
        recipient = conversation.participants.exclude(id=sender_id).first()

        channel_layer = get_channel_layer()

        message_data.pop("socket_type", None)

        async_to_sync(channel_layer.group_send)(
            f"user_{recipient.id}",
            {
                "type": "new_message",
                "message": message_data,
            },
        )
    except Conversation.DoesNotExist as e:
        logging.error(e)
    except Exception as e:
        logging.error(e)


@database_sync_to_async
def update_message_read_status(data, user):
    message_id = data.get("message_id")
    message = Message.objects.filter(id=message_id).first()
    if not message:
        return
    conversation = message.conversation
    Message.objects.filter(conversation=conversation, created_at__lte=message.created_at,).exclude(
        sender=user
    ).update(is_read=True, read_at=timezone.now())


class BaseAsyncJsonWebSocketConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_authenticated:
            await update_user_online_status(self.scope["user"].id)
        await super().connect()

    async def disconnect(self, close_code):
        if self.scope["user"].is_authenticated:
            await update_user_offline_status(self.scope["user"].id)


class EchoConsumer(BaseAsyncJsonWebSocketConsumer):
    async def connect(self):
        await super().connect()
        await self.send_json({"data": "Hello world!"})

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        await self.send_json({"data": "Hello world!"})


class UserConsumer(BaseAsyncJsonWebSocketConsumer):
    async def connect(self):
        await super().connect()
        user = self.scope["user"]
        self.group_name = f"user_{user.id}"
        if user.is_authenticated:
            user = await refresh_user_from_db(user)
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await send_user_status_notification(user)

    async def disconnect(self, close_code):
        await super().disconnect(close_code)
        user = self.scope["user"]
        if user.is_authenticated:
            user = await refresh_user_from_db(user)
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
            await send_user_status_notification(user)

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        try:
            data = await self.decode_json(text_data)
            type = data.get("socket_type")
            if type == "chat_message":
                await self.chat_message(data)
            elif type == "read_message":
                await self.read_message(data)
        except JSONDecodeError:
            await self.send_json({"error": "Invalid json"})

    async def chat_message(self, event):
        print(event)
        headers = {key.decode("utf-8"): value.decode("utf-8") for key, value in self.scope["headers"]}
        domain = f"{headers.get('x-forwarded-proto', 'http')}://{headers.get('host')}"
        user = self.scope["user"]
        event["sender"] = user.id if user.is_authenticated else None
        event["domain"] = domain
        created, message_data = await create_message(event, self.scope["user"])
        response = message_data
        response["socket_type"] = "chat_message"
        await send_message_to_user(message_data.get("conversation"), getattr(user, "id"), message_data)
        if created:
            response["is_me"] = True
            response["type"] = "send_message"
            response["success"] = True

        await self.send_json(response)

    async def new_message(self, event):
        await self.send_json(event)

    async def read_message(self, event):
        user = self.scope["user"]
        await update_message_read_status(event, user)

    async def user_status(self, event):
        await self.send_json(event)
