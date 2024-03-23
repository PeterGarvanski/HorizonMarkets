from django.db import models
from django.contrib.auth.models import User


class CryptoAssets(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='crypto_assets')
    assets = models.JSONField(default=dict, null=True, blank=True)


class OpenTrades(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trades')
    order_id = models.IntegerField(null=False, blank=False)
    client_order_id = models.CharField(max_length=100, null=False, blank=False)
    symbol = models.CharField(max_length=20, null=False, blank=False)
    order_type = models.CharField(max_length=10, null=False, blank=False)
    side = models.CharField(max_length=4, null=False, blank=False)
    quantity = models.DecimalField(max_digits=20, decimal_places=8, null=False, blank=False)
    cumulative_quote_qty = models.DecimalField(max_digits=20, decimal_places=8, null=False, blank=False)
    price = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    take_profit = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
    stop_loss = models.DecimalField(max_digits=20, decimal_places=8, null=True, blank=True)
