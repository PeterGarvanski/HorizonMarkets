from django.contrib import admin
from .models import UserProfile, AccountHistory

class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'account_balance',
        'deposit_amount_multiplier'
    )

admin.site.register(UserProfile, UserProfileAdmin)

class AccountHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'new_account_balance',
        'net_difference',
        'date',
        'time'
    )

admin.site.register(AccountHistory, AccountHistoryAdmin)