from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.TextField(null=False, blank=False, default='common')

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
