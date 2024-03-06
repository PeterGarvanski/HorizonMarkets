# Generated by Django 4.2.10 on 2024-03-05 10:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0009_rename_transaction_type_transaction_transfer_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='account_history',
        ),
        migrations.CreateModel(
            name='AccountHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new_account_balance', models.DecimalField(decimal_places=2, max_digits=15)),
                ('net_difference', models.DecimalField(decimal_places=2, max_digits=15)),
                ('date', models.DateField(auto_now_add=True)),
                ('time', models.TimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_history', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]