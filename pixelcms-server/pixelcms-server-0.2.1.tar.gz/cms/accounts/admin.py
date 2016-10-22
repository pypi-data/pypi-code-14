from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    list_display = ('user',)
    readonly_fields = ('user',)
