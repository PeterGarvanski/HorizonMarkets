# Generated by Django 4.2.10 on 2024-03-08 11:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0004_market_charts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='market',
            name='charts',
        ),
    ]
