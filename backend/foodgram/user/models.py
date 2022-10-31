from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractUser):
    """Модель пользователя"""
    email = models.EmailField(
        max_lenght=250,
    )
    username = models.CharField(
        max_length=100,
        validator=[UnicodeUsernameValidator])
    first_name = models.CharField(
        max_lenght=100,
        )
    last_name = models.CharField(
        max_lenght=100,
    )
    password = models.CharField(
        max_lenght=100,
    )


class Follow(models.Model):
    """Модель подписчиков"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        null=True
    )
