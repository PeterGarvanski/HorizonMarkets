from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    account_history = models.CharField(max_length=256, null=False, blank=False, default="0")

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


class Transaction(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    transaction_type = models.CharField(max_length=256, null=False, blank=False, default="0")

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    @property
    def email(self):
        return self.user.email