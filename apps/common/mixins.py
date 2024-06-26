from django.db.models import ImageField
from image_uploader_widget.widgets import ImageUploaderWidget


class ImageFieldMixin:
    formfield_overrides = {ImageField: {"widget": ImageUploaderWidget}}
