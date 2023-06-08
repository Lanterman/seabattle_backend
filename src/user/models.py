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
    email = models.EmailField('email address', blank=False, help_text="Required.", unique=True, 
                              error_messages={"unique": "A user with that email already exists."})
    hashed_password: hex = models.CharField("password", max_length=128, help_text="Required.")

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'user_detail': self.slug})
