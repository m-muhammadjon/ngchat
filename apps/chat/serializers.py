from rest_framework import serializers

from apps.chat.models import Message
from apps.common.models import Media
from apps.users.models import User


class UserChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "is_online",
            "last_seen",
        )


class MediaChatSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = Media
        fields = ("id", "file_type", "file_name", "file_extension", "file_size", "file")

    def get_file(self, obj: Media):
        domain = self.context.get("domain")
        return f"{domain}{obj.file.url}"


class ChatMessageSerializer(serializers.ModelSerializer):
    is_me = serializers.BooleanField(default=False, read_only=True)

    class Meta:
        model = Message
        fields = (
            "id",
            "is_me",
            "conversation",
            "sender",
            "type",
            "text",
            "file",
            "created_at",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["sender"] = UserChatSerializer(instance.sender, context=self.context).data
        if data["type"] == "file":
            data["file"] = MediaChatSerializer(instance.file, context=self.context).data
        return data

    def validate_conversation(self, conversation):
        user_id = self.initial_data.get("sender")
        user = User.objects.filter(id=user_id).first()
        if not user:
            raise serializers.ValidationError("User not found")
        if not conversation.participants.filter(id=user.id).exists():
            raise serializers.ValidationError("You are not a participant of this conversation")
        return conversation

    def validate(self, attrs):
        if attrs.get("text") is None and attrs.get("file") is None:
            raise serializers.ValidationError("Either text or file should be provided")
        if attrs.get("text") and attrs.get("file"):
            raise serializers.ValidationError("Either text or file should be provided")
        _type = attrs.get("type")
        if _type == "text" and not attrs.get("text"):
            raise serializers.ValidationError("Text should be provided")
        if _type == "file" and not attrs.get("file"):
            raise serializers.ValidationError("File should be provided")
        return attrs

    def create(self, validated_data):
        obj = Message.objects.create(**validated_data)
        if obj.file:
            obj.type = "image"
            obj.save()
        return obj
