from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _

from core.models import User


@admin.register(User)
class CoreUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (_('Дополнительные настройки'), {'fields': ('lead', 'role')}),
    )
