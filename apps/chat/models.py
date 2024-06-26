from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimeStampedModel
from apps.users.models import User


class Conversation(TimeStampedModel):
    participants = models.ManyToManyField(User, verbose_name="Participants", related_name="conversations")

    def __str__(self):
        return f"Conversation {self.id}"


class MessageTypeChoices(models.TextChoices):
    TEXT = "text", "Text"
    IMAGE = "image", "Image"


class Message(TimeStampedModel):
    conversation = models.ForeignKey(
        Conversation, verbose_name="Conversation", on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(User, verbose_name="Sender", on_delete=models.CASCADE, related_name="messages")
    type = models.CharField(verbose_name="Type", max_length=16, choices=MessageTypeChoices.choices, default="text")
    text = models.TextField(verbose_name="Text", null=True, blank=True)
    file = models.ForeignKey("common.Media", verbose_name="File", on_delete=models.SET_NULL, null=True, blank=True)
    is_read = models.BooleanField(verbose_name="Is read", default=False)
    read_at = models.DateTimeField(verbose_name="Read at", null=True, blank=True)

    def __str__(self):
        return f"Message {self.id} from {self.sender.first_name}"

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
