from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimeStampedModel
from apps.users.managers import UserManager


class User(AbstractUser, TimeStampedModel):
    is_online = models.BooleanField(_("Is online"), default=False)
    last_seen = models.DateTimeField(_("Last seen"), null=True, blank=True)
    objects = UserManager()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
