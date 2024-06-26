from django.db.models import BooleanField, Case, Value, When
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.chat.models import Conversation, Message

from .permissions import IsConversationParticipant
from .serializers import MessageHistoryListSerializer


class MessageHistoryListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, IsConversationParticipant)
    serializer_class = MessageHistoryListSerializer

    def get_object(self):
        return Conversation.objects.filter(id=self.kwargs.get("conversation_id")).first()

    def get_queryset(self):
        conversation = self.get_object()
        if not conversation:
            return Message.objects.none()
        qs = conversation.messages.annotate(
            is_me=Case(
                When(sender=self.request.user, then=Value(True)), default=Value(False), output_field=BooleanField()
            )
        )

        return qs
