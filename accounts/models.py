from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from core.standard_values import ROLE_CHOICES


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default="user",
        verbose_name=_("Role")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
