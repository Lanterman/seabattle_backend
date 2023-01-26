import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    """User model"""

    slug: str = models.SlugField(max_length=250, verbose_name="URL", help_text="Required. Populated by username!")
    mobile_number: str = models.CharField(max_length=50, verbose_name="mobile number", blank=True)
    cash: int = models.IntegerField(default=100)
    created_in: datetime.datetime = models.DateTimeField(auto_now_add=True)
    updated_in: datetime.datetime = models.DateTimeField(blank=True, null=True)
    photo: bytes = models.ImageField(blank=True, upload_to="users/")
    email = models.EmailField('email address', blank=False, help_text="Required.", error_messages={
            "unique": "A user with that email already exists.",
        })
    hashed_password: hex = models.CharField("password", max_length=128, help_text="Required.")

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-created_in"]
        unique_together = ["slug", "email"]

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'user_detail': self.slug})
