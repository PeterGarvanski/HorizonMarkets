from django.db import models
from django.contrib.auth.models import User


class Chart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='charts')
    crypto_charts = models.JSONField(null=True, blank=True, default=['BTCUSDT', 'ETHUSDT'], max_length=3)