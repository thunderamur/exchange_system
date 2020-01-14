from django.contrib import admin

from .models import Currency


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    fields = ['currency', 'rate', 'created']
    list_display = fields
    readonly_fields = fields
