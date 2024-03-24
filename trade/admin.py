from django.contrib import admin
from .models import OpenTrades


class OpenTradesAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'order_id',
        'client_order_id',
        'symbol',
        'order_type',
        'side',
        'quantity',
        'cumulative_quote_qty',
        'price',
        'take_profit',
        'stop_loss'
    )

admin.site.register(OpenTrades, OpenTradesAdmin)