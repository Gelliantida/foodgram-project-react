"""Создание модели пользователя."""

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""

    username = models.CharField(
        verbose_name='Имя пользователя',
        db_index=True,
        unique=True,
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message='Недопустимые символы!'
            )
        ]
    )
    first_name = models.CharField(
        verbose_name='Имя пользователя',
        max_length=50,
    )
    last_name = models.CharField(
        verbose_name='Фамилия пользователя',
        max_length=50,
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True,
        max_length=254
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    class Meta:
        """Единственное и множественные имена модели."""

        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username}'


class Follow(models.Model):
    """Модель подписчика."""

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        """Единственное и множественные имена модели."""

        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'

        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='follow_user_author_constraint'
            ),
        )

    def __str__(self):
        return f'{self.user} подписан на {self.author}'