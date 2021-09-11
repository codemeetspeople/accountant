from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _

from core.models import BaseModel


USER_MODEL = get_user_model()


class Bank(BaseModel):
    class Meta:
        verbose_name = _('Банк')
        verbose_name_plural = _('Банки')

    title = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name=_('Название')
    )

    def __str__(self):
        return self.title


class CardType(BaseModel):
    class Meta:
        verbose_name = _('Тип карты')
        verbose_name_plural = _('Типы карт')

    title = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name=_('Название')
    )

    bank = models.ForeignKey(
        to='Bank',
        verbose_name=_('Банк'),
        on_delete=models.CASCADE,
        related_name='card_types',
        null=False,
        blank=False
    )

    replenishment_percent = models.FloatField(
        default=0.0,
        null=False,
        blank=False,
        verbose_name=_('Процент за пополнение')
    )

    withdrawal_percent = models.FloatField(
        default=0.0,
        null=False,
        blank=False,
        verbose_name=_('Процент за снятие')
    )

    def __str__(self):
        return f'{self.bank.title} {self.title}'


class Card(BaseModel):
    class Meta:
        verbose_name = _('Карта')
        verbose_name_plural = _('Карты')

    card_type = models.ForeignKey(
        to='CardType',
        verbose_name=_('Тип карты'),
        on_delete=models.CASCADE,
        related_name='cards',
        null=False,
        blank=False
    )

    owner = models.ForeignKey(
        to=USER_MODEL,
        verbose_name=_('Владелец'),
        on_delete=models.CASCADE,
        related_name='cards',
        null=False,
        blank=False
    )

    balance = models.FloatField(
        default=0.0,
        null=False,
        blank=False,
        verbose_name=_('Баланс')
    )

    number = models.CharField(
        max_length=16,
        null=False,
        blank=False,
        verbose_name=_('Номер')
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Активна')
    )

    def __str__(self):
        return f'{self.card_type.bank.title} {self.card_type.title} {self.number} {self.owner.username}'


class CashInRequest(BaseModel):
    class Meta:
        verbose_name = _('Запрос на пополнение')
        verbose_name_plural = _('Запросы на пополнение')

    executor = models.ForeignKey(
        to=USER_MODEL,
        verbose_name=_('Исполнитель'),
        on_delete=models.CASCADE,
        related_name='cashin_requests',
        null=False,
        blank=False
    )

    date = models.DateTimeField(
        null=False,
        blank=False,
        verbose_name=_('Дата')
    )

    closed = models.BooleanField(
        verbose_name=_('Запрос выполнен'),
        default=False
    )

    def __str__(self):
        return f'{self._meta.verbose_name} {self.date}'


class CashInTransaction(BaseModel):
    verbose_name = _('Транзакция (пополнение)')
    verbose_name_plural = _('Транзакции (пополнение)')

    request = models.ForeignKey(
        to='CashInRequest',
        verbose_name=_('Запрос на пополнение'),
        on_delete=models.CASCADE,
        related_name='transactions',
        null=False,
        blank=False
    )

    card = models.ForeignKey(
        to='card',
        verbose_name=_('Карта'),
        on_delete=models.CASCADE,
        related_name='cashin_transactions',
        null=False,
        blank=False
    )

    requested_amount = models.FloatField(
        null=False,
        blank=False,
        verbose_name=_('Сумма пополнения')
    )

    received_amount = models.FloatField(
        default=0.0,
        null=False,
        blank=False,
        verbose_name=_('Фактически пополнено')
    )

    received_amount_raw = models.FloatField(
        default=0.0,
        null=True,
        blank=True,
        verbose_name=_('Фактически пополнено (без комиссии)')
    )
