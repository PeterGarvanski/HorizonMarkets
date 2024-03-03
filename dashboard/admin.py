from django.contrib import admin
from .models import UserProfile, Transaction

class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'account_balance',
        'account_history'
    )

admin.site.register(UserProfile, UserProfileAdmin)

class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'country',
        'city',
        'postal_code',
        'street_name',
        'street_number',
        'amount',
        'transaction_type'
    )

admin.site.register(Transaction, TransactionAdmin)
