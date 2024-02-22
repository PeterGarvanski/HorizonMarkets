from django.db import models

# Create your models here.
class UserProfile(models.Model):
    primary_key = models.AutoField(primary_key=True)
    username = models.CharField(max_length=40, null=False, blank=False)
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(max_length=60, null=False, blank=False)