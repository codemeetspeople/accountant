from django.contrib import admin

from accountant import models


class CashInTransactionTabularInline(admin.TabularInline):
    model = models.CashInTransaction
    extra = 1


@admin.register(models.Bank)
class BankAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CardType)
class CardTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('owner', 'card_type', 'number', 'balance')


@admin.register(models.CashInRequest)
class CashInRequestAdmin(admin.ModelAdmin):
    inlines = (CashInTransactionTabularInline,)
