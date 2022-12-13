from django.contrib.auth.models import AbstractUser
from django.db import models
from foodgram.constants import (MAX_LENGTH_CHARFIELD, MAX_LENGTH_EMAILFIELD,
                                MAX_LENGTH_ROLE_USER)


class CustomUser(AbstractUser):
    """Кастомная модель юзеров, которая основана на модели «AbstractUser».

    Поля модели(являются обязательными, кроме последнего):
      - email: электронная почта пользователя.
      - role: роль пользователя на сайте(по умолчанию «user»),
              изменить роль может только админ сайта.
      - first_name: имя пользователя.
      - last_name: фамилия пользователя.
      - subscriber(M2M на одной модели): подписки пользователя на других юзеров
    """
    USER = 'user'
    ADMIN = 'admin'
    ROLES = [
        (USER, 'user'),
        (ADMIN, 'admin'),
    ]
    email = models.EmailField(
        max_length=MAX_LENGTH_EMAILFIELD,
        unique=True,
        verbose_name='Электронная почта юзера'
    )
    role = models.CharField(
        max_length=MAX_LENGTH_ROLE_USER,
        choices=ROLES,
        default=USER,
        verbose_name='Роль юзера',
    )
    first_name = models.CharField(
        max_length=MAX_LENGTH_CHARFIELD,
        verbose_name='Имя юзера'
    )
    last_name = models.CharField(
        max_length=MAX_LENGTH_CHARFIELD,
        verbose_name='Фамилия юзера'
    )
    subscriber = models.ManyToManyField(
        'self', symmetrical=False,
        related_name='subscribers', verbose_name='Подписки юзера'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
