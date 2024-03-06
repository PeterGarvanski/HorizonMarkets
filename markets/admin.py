from django.contrib import admin
from .models import Market


class MarketAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'user_market'
    )

admin.site.register(Market, MarketAdmin)