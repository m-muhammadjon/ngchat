from rest_framework.serializers import ModelSerializer

from apps.users.models import User


class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "is_online", "last_seen"]
        read_only_fields = ["id"]
