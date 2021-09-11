from django.utils.translation import gettext as _


class Role:
    LEAD = 'lead'
    USER = 'user'
    ACCOUNTANT = 'accountant'

    CHOICES = [
        (LEAD, _('Руководитель')),
        (USER, _('Пользователь')),
        (ACCOUNTANT, _('Бухгалтер')),
    ]
