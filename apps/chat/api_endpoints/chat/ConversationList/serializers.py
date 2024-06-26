from rest_framework import serializers

from apps.chat.models import Conversation
from apps.users.models import User


class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "full_name",
            "img",
        )


class ConversationSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    unread_messages_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = (
            "id",
            "user",
            "last_message",
            "unread_messages_count",
        )

    def get_user(self, obj):
        user = obj.participants.all().exclude(id=self.context.get("request").user.id).first()
        return {
            "user_id": user.id,
            "username": user.username,
            "full_name": f"{user.first_name} {user.last_name}",
            "is_online": user.is_online,
        }

    def get_last_message(self, obj: Conversation):
        if not obj.messages.first():
            return None
        data = {
            "message": obj.messages.first().text,
            "created_at": obj.messages.first().created_at.astimezone(),
        }
        if obj.messages.first().sender == self.context.get("request").user:
            data["mine"] = True
        else:
            data["mine"] = False
        return data

    def get_unread_messages_count(self, obj: Conversation):
        return obj.messages.filter(is_read=False).exclude(sender__id=self.context.get("request").user.id).count()
