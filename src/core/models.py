from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from core.constants import Role


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        verbose_name=_('Время создания'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_('Время обновления'),
        auto_now=True
    )


class User(AbstractUser):
    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    lead = models.ForeignKey(
        to='self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('Руководитель')
    )

    role = models.CharField(
        max_length=15,
        default=Role.USER,
        choices=Role.CHOICES,
        verbose_name=_('Роль')
    )
