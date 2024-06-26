from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.chat.models import Conversation
from apps.users.models import User

from .serializers import ConversationCreateSerializer


class ConversationCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(request_body=ConversationCreateSerializer())
    def post(self, request):
        user_id = request.data.get("user_id")
        user2 = User.objects.filter(id=user_id).first()
        user = self.request.user
        if user_id == user.id:
            return Response(
                {"message": "You cannot create a conversation with yourself"}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            if user2:
                conversation = Conversation.objects.filter(participants=user.id).filter(participants=user2.id).first()
                if conversation:
                    return Response(
                        {"conversation_id": conversation.id, "message": "Conversation already exists"},
                        status=status.HTTP_200_OK,
                    )
                else:
                    conversation = Conversation.objects.create()
                    conversation.participants.add(user_id, user.id)
                    return Response(
                        {"conversation_id": conversation.id, "message": "Conversation created successfully"},
                        status=status.HTTP_201_CREATED,
                    )
            else:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
