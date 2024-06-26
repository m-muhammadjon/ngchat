from django.urls import path

from apps.chat import api_endpoints

app_name = "chat"

urlpatterns = [
    path(
        "message-history/<int:conversation_id>/",
        api_endpoints.MessageHistoryListAPIView.as_view(),
        name="message-history",
    ),
    path("conversations/", api_endpoints.ConversationListAPIView.as_view(), name="conversations"),
    path("conversation-create/", api_endpoints.ConversationCreateAPIView.as_view(), name="conversation-create"),
]
