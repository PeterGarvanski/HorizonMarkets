from django.contrib import admin
from .models import UserProfile, Transaction, AccountHistory

class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'account_balance'
    )

admin.site.register(UserProfile, UserProfileAdmin)

class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'country',
        'city',
        'postal_code',
        'address_line_1',
        'amount',
        'transfer_type'
    )

admin.site.register(Transaction, TransactionAdmin)

class AccountHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'new_account_balance',
        'net_difference',
        'date',
        'time'
    )

admin.site.register(AccountHistory, AccountHistoryAdmin)