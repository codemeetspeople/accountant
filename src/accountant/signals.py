from django.db.models.signals import post_save
from django.dispatch import receiver

from accountant import models


@receiver(post_save, sender=models.CashInRequest)
def cash_in_request_updated(sender, instance, created, **kwargs):
    if created:
        return

    if not instance.closed:
        return

    for transaction in instance.transactions.all():
        if transaction.card.card_type.replenishment_percent != 0:
            amount = transaction.received_amount
            commission = amount / 100 * transaction.card.card_type.replenishment_percent
            amount_with_commission = amount - commission

            transaction.received_amount = amount_with_commission
            transaction.received_amount_raw = amount

            transaction.card.balance += amount_with_commission

            transaction.card.save()
            transaction.save()
