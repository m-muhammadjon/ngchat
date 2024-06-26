from rest_framework import serializers

from apps.chat.models import Message
from apps.common.models import Media
from apps.users.models import User


class MessageSendSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "is_online",
            "last_seen",
            "first_name",
            "last_name",
        )


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = (
            "id",
            "file_name",
            "file_type",
            "file_extension",
            "file_size",
            "file",
        )


class MessageHistoryListSerializer(serializers.ModelSerializer):
    sender = MessageSendSerializer()
    is_me = serializers.BooleanField(default=False)
    file = MediaSerializer()

    class Meta:
        model = Message
        fields = (
            "id",
            "sender",
            "is_me",
            "type",
            "text",
            "file",
            "created_at",
            "updated_at",
            "is_read",
            "read_at",
        )
