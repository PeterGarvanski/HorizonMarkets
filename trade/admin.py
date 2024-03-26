from django.contrib import admin
from .models import OpenTrade, TradeHistory


class OpenTradeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'time',
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

admin.site.register(OpenTrade, OpenTradeAdmin)


class TradeHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'date',
        'time',
        'order_id',
        'client_order_id',
        'symbol',
        'order_type',
        'quantity',
        'cumulative_quote_qty',
        'entry_price',
        'close_price',
        'take_profit',
        'stop_loss',
        'net_pl',
    )

admin.site.register(TradeHistory, TradeHistoryAdmin)