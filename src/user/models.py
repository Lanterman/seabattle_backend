import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


AbstractUser._meta.get_field('username').max_length = 30
AbstractUser._meta.get_field('username').help_text = _(
            "Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."
        )


class User(AbstractUser):
    """User model"""

    mobile_number: str = models.CharField(max_length=20, verbose_name="mobile number", blank=True)
    cash: int = models.IntegerField(default=100)
    rating: int = models.IntegerField(default=0)
    created_in: datetime.datetime = models.DateTimeField(auto_now_add=True)
    updated_in: datetime.datetime = models.DateTimeField(blank=True, null=True)
    photo: bytes = models.ImageField(blank=True, upload_to="users/")
    email = models.EmailField(_('email address'), blank=False, help_text="Required.", unique=True, 
                              error_messages={"unique": _("A user with that email already exists.")})
    hashed_password: str = models.CharField("password", max_length=128, help_text="Required.")

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('user-detail', kwargs={'username': self.username})


class SecretKey(models.Model):
    """User secret key to create JWT token"""

    key: str = models.CharField(_("secret key"), max_length=30, unique=True)
    user: int = models.ForeignKey(verbose_name="user_id", to=User, on_delete=models.CASCADE, related_name="secret_key")

    class Meta:
        verbose_name = _("Secret Key")
        verbose_name_plural = _("Secret Keys")


class JWTToken(models.Model):
    """JWT token for authentication"""

    access_token: str = models.CharField(_("access token"), max_length=250, unique=True,)
    refresh_token: str = models.CharField(_("refresh token"), max_length=250, unique=True)
    created: datetime.datetime = models.DateTimeField(_("created"), auto_now_add=True)
    user: int = models.ForeignKey(verbose_name=_("user_id"), to=User, on_delete=models.CASCADE, related_name="auth_token1")

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