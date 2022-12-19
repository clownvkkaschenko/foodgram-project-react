from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from foodgram.constants import (MAX_LENGTH_CHARFIELD, MAX_LENGTH_EMAILFIELD,
                                MAX_LENGTH_ROLE_USER)
from rest_framework.serializers import ValidationError


class CustomUser(AbstractUser):
    """Кастомная модель юзеров, которая основана на модели «AbstractUser».

    Поля модели(являются обязательными, кроме «subscriber»):
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

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_user(self):
        return self.role == 'user'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


@receiver(m2m_changed, sender=CustomUser.subscriber.through)
def prevent_duplicate_tags_from_group(sender, instance, action, reverse,
                                      model, pk_set, **kwargs):
    """Обработчик сигнала для поля «subscriber».

    Обработчик не разрешает пользователям подписываться на себя.
    """
    if action == 'pre_add':
        if instance.pk in pk_set:
            raise ValidationError(
                {'subscriber': 'Вы не можете подписаться на себя'}
            )
