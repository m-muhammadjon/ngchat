from rest_framework import serializers


class ConversationCreateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
