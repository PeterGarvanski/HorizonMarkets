from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)

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
    
    TRANSACTION_TYPE_CHOICES = [
        ('Withdraw', 'Withdraw'),
        ('Deposit', 'Deposit'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    country = models.CharField(max_length=40, null=False, blank=False, default="N/A")
    city = models.CharField(max_length=50, null=False, blank=False, default="N/A")
    postal_code = models.CharField(max_length=10, null=False, blank=False, default="N/A")
    address_line_1 = models.CharField(max_length=100, null=False, blank=False, default="N/A")
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=10, validators=[MinValueValidator(10)])
    transfer_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES, null=False, blank=False, default="Deposit")


class AccountHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='account_history')
    new_account_balance = models.DecimalField(max_digits=15, decimal_places=2)
    net_difference = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)