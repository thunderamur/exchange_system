from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    fields = ['from_user', 'to_user', 'currency', 'amount', 'created']
    list_display = fields
    readonly_fields = fields
