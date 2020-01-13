from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ['email', 'currency', 'get_balance', 'is_staff', 'is_superuser']
    list_display = fields
    readonly_fields = ['get_balance']

    def get_balance(self, obj):
        return obj.get_balance()
    get_balance.short_description = _('Balance')
