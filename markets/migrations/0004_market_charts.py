# Generated by Django 4.2.10 on 2024-03-08 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0003_alter_market_fav_tickers'),
    ]

    operations = [
        migrations.AddField(
            model_name='market',
            name='charts',
            field=models.JSONField(blank=True, default=['BTC'], max_length=2, null=True),
        ),
    ]
