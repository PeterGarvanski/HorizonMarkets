from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    deposit_amount_multiplier = models.IntegerField(default=1, null=False, blank=False)

    @property
    def username(self):
        return self.user.username

    @property
    def email(self):
        return self.user.email

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name


class AccountHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='account_history')
    new_account_balance = models.DecimalField(max_digits=15, decimal_places=2)
    net_difference = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)