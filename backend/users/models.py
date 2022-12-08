from django.contrib.auth.models import AbstractUser
from django.db import models
from foodgram.constant import (MAX_LENGTH_CHARFIELD, MAX_LENGTH_EMAILFIELD,
                               MAX_LENGTH_ROLE_USER)


class CustomUser(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    ROLES = [
        (USER, 'user'),
        (ADMIN, 'admin'),
    ]
    email = models.EmailField(
        max_length=MAX_LENGTH_EMAILFIELD,
        unique=True,
        verbose_name='Электронная почта'
    )
    role = models.CharField(
        max_length=MAX_LENGTH_ROLE_USER,
        choices=ROLES,
        default=USER,
        verbose_name='Роль пользователя',
    )
    first_name = models.CharField(
        max_length=MAX_LENGTH_CHARFIELD,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=MAX_LENGTH_CHARFIELD,
        verbose_name='Фамилия'
    )
    subscriber = models.ManyToManyField(
        'self', symmetrical=False,
        related_name='subscribers', verbose_name='Подписчики'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
