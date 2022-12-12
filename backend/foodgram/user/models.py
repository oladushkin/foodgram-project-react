from django.contrib.auth import get_user_model
from django.contrib.auth.models import UserManager
from django.db import models

User = get_user_model()


class Manager(UserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Пользователь должен иметь email')
        user = self.model(email=email,)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.model(email=email,)
        # user.username=""
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user


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

    class Meta:
        unique_together = ('user', 'following')
