from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    ROLES = [
        (USER, 'user'),
        (ADMIN, 'admin'),
    ]
    username_validator = AbstractUser.username_validator
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator],
        verbose_name='Логин',
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Электронная почта'
    )
    role = models.CharField(
        max_length=6,
        choices=ROLES,
        default=USER,
        verbose_name='Роль пользователя',
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия'
    )
    subscriber = models.ManyToManyField(
        'self', symmetrical=False,
        related_name='subscribers', verbose_name='Подписчики'
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == CustomUser.ADMIN or self.is_superuser

    @property
    def is_user(self):
        return self.role == CustomUser.USER
