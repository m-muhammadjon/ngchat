from rest_framework import serializers

from apps.common.models import Media


class MediaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = (
            "id",
            "file",
        )
