from django.apps import AppConfig

from django.utils.translation import gettext_lazy as _


class AccountantConfig(AppConfig):
    name = 'accountant'
    verbose_name = _('Бухгалтерия')

    def ready(self):
        from accountant import signals  # noqa
