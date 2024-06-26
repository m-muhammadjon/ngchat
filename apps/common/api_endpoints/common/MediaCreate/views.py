from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated

from apps.common.models import Media

from .serializers import MediaCreateSerializer


class MediaCreateAPIView(CreateAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaCreateSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)


__all__ = ["MediaCreateAPIView"]
