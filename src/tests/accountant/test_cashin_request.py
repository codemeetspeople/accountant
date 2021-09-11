import datetime

import pytest
from django.utils.timezone import make_aware

from accountant import models


@pytest.mark.django_db
def test_cashin_request(create_user):
    bank = models.Bank.objects.create(title='Private')
    card_type = models.CardType.objects.create(
        bank=bank, title='GOLD', replenishment_percent=0.5
    )
    user = create_user(is_staff=True, is_superuser=True)
    card = models.Card.objects.create(
        owner=user, card_type=card_type, number='1111'*4
    )
    cash_in_request = models.CashInRequest.objects.create(
        date=make_aware(datetime.datetime.now()), executor=user
    )
    cash_in_transaction = models.CashInTransaction.objects.create(
        request=cash_in_request, card=card, requested_amount=50000
    )

    cash_in_transaction.received_amount = 40000
    cash_in_transaction.save()

    cash_in_request.closed = True
    cash_in_request.save()

    cash_in_transaction = models.CashInTransaction.objects.get(id=cash_in_transaction.id)

    assert cash_in_transaction.requested_amount == 50000
    assert cash_in_transaction.received_amount_raw == 40000
    assert cash_in_transaction.received_amount == 39800

    card = models.Card.objects.get(id=card.id)
    assert card.balance == 39800
