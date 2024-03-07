from django.db import models
from django.contrib.auth.models import User


class Market(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='market')
    user_market = models.CharField(max_length=15, null=False, blank=False, default='BTC/USDT')
    fav_tickers = models.JSONField(null=True, blank=True, default=['BTC', 'ETH', "BNB", "SOL"], max_length=8)