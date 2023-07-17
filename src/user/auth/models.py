from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from config import settings


User = settings.AUTH_USER_MODEL


class SecretKey(models.Model):
    """User secret key to create JWT token"""

    key: str = models.CharField(_("secret key"), max_length=250, unique=True)
    created: timezone = models.DateTimeField(_("created"), auto_now_add=True)
    user: int = models.ForeignKey(verbose_name="user_id", to=User, on_delete=models.CASCADE, related_name="secret_key")

    class Meta:
        verbose_name = _("Secret Key")
        verbose_name_plural = _("Secret Keys")


class JWTToken(models.Model):
    """JWT token for authentication"""

    access_token: str = models.CharField(_("access token"), max_length=250, unique=True,)
    refresh_token: str = models.CharField(_("refresh token"), max_length=250, unique=True)
    created: timezone = models.DateTimeField(_("created"), auto_now_add=True)
    user: int = models.ForeignKey(verbose_name=_("user_id"), to=User, on_delete=models.CASCADE, related_name="auth_token")

    class Meta:
        verbose_name = _("JWTToken")
        verbose_name_plural = _("JWTTokens")

    def __str__(self):
        return f"JWT token to {self.user.username}"


class JWTTokenProxy(JWTToken):
    """
    Proxy mapping pk to user pk for use in admin.
    """
    @property
    def pk(self):
        return self.user

    class Meta:
        proxy = True
        abstract = True
        verbose_name = "JWTToken"