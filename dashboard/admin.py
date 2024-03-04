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
        'address_line_1',
        'amount',
        'type_of_transaction'
    )

admin.site.register(Transaction, TransactionAdmin)
