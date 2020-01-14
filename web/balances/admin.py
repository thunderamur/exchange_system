from django.contrib import admin

from .models import Balance


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    fields = ['user', 'currency', 'amount', 'flow', 'created']
    list_display = fields
    readonly_fields = fields
