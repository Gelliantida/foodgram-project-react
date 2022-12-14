"""Создание модели пользователя."""

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models


USERNAME_VALIDATION = 'Недопустимое значение поля "username"'
EMAIL_LENGTH = 254
FIRST_NAME_LENGTH = 50
LAST_NAME_LENGTH = 50
USERNAME_LENGTH = 100
FOLLOW_TO_YOURSELF = 'Невозможно подписаться на себя'


class User(AbstractUser):
    """Модель пользователя."""

    username = models.CharField(
        verbose_name='Имя пользователя',
        unique=True,
        max_length=USERNAME_LENGTH,
        validators=(RegexValidator(
            regex=r'^[\w.@+-]+\Z',
            message=USERNAME_VALIDATION),
        )
    )
    first_name = models.CharField(
        verbose_name='Имя пользователя',
        max_length=FIRST_NAME_LENGTH,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name='Фамилия пользователя',
        max_length=LAST_NAME_LENGTH,
        blank=True,
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True,
        max_length=EMAIL_LENGTH
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    class Meta:
        """Единственное и множественные имена модели."""

        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


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

    def clean(self):
        if self.user == self.author:
            raise ValidationError(FOLLOW_TO_YOURSELF)

    class Meta:
        """Дополнительные значения модели."""

        ordering = ['author', ]
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
