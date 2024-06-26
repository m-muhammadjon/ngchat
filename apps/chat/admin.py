from django.contrib import admin

from apps.chat.models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("id",)
    list_filter = ("participants",)
    search_fields = ("id",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "conversation",
        "sender",
        "type",
        "text",
        "file",
        "is_read",
        "read_at",
    )
    readonly_fields = ("created_at", "updated_at")
    list_filter = ("conversation", "sender", "type", "is_read", "read_at")
    search_fields = ("id", "conversation", "sender", "type", "text", "file")
