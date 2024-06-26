import os

from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        abstract = True


class FileTypeChoices(models.IntegerChoices):
    UNKNOWN = -1, _("Unknown")
    IMAGE = 0, _("Image")
    VIDEO = 1, _("Video")
    DOCUMENT = 2, _("Document")


class Media(TimeStampedModel):
    file_type = models.IntegerField(choices=FileTypeChoices.choices, null=True, blank=True)
    file_name = models.CharField(verbose_name=_("File name"), max_length=255)
    file_extension = models.CharField(verbose_name=_("File extension"), max_length=255)
    file_size = models.BigIntegerField(verbose_name=_("File size"))
    file = models.FileField(verbose_name=_("File"), upload_to="uploaded/%Y/%m/%d/")

    def save(self, *args, **kwargs):
        if not self.file_extension:
            self.file_extension = self.get_file_extension()
        if not self.file_name:
            self.file_name = self.get_file_name()
        if not self.file_size:
            self.file_size = self.file.size
        if not self.file_type:
            self.file_type = self.get_file_type()
        super().save(*args, **kwargs)

    def get_file_extension(self):
        return os.path.splitext(self.file.name)[1][1:].lower()

    def get_file_name(self):
        return os.path.splitext(self.file.name)[0]

    def get_file_type(self):
        file_extension = self.get_file_extension()
        if file_extension in ["jpg", "jpeg", "png", "gif", "webp"]:
            return FileTypeChoices.IMAGE
        if file_extension in ["mp4", "webm", "mov"]:
            return FileTypeChoices.VIDEO
        if file_extension in ["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx"]:
            return FileTypeChoices.DOCUMENT
        return FileTypeChoices.UNKNOWN
