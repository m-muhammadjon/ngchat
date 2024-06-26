from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import ConversationSerializer


class ConversationListAPIView(ListAPIView):
    serializer_class = ConversationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        conversations = self.request.user.conversations.filter(messages__isnull=False).distinct()

        return conversations
