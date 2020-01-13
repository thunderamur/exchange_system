from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    fields = '__all__'
    list_display = ['from_user', 'to_user', 'currency', 'amount', 'created']
    readonly_fields = fields
