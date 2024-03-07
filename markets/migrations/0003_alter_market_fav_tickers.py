# Generated by Django 4.2.10 on 2024-03-07 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0002_market_fav_tickers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='market',
            name='fav_tickers',
            field=models.JSONField(blank=True, default=['BTC', 'ETH', 'BNB', 'SOL'], max_length=8, null=True),
        ),
    ]