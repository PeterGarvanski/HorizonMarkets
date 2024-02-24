from django.contrib import admin
from .models import UserProfile, Transaction

# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'account_balance',
        'account_history'
    )


class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'email',
        'amount',
        'transaction_type'
    )


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Transaction, TransactionAdmin)