from django.utils import timezone
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    last_request = models.DateTimeField("last request", default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    @property
    def posts(self):
        return self.user_posts.all()

    @property
    def likes(self):
        return self.user_likes.all()

    def __str__(self):
        return self.email
