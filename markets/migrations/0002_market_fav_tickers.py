# Generated by Django 4.2.10 on 2024-03-07 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='market',
            name='fav_tickers',
            field=models.JSONField(blank=True, default=list, max_length=8, null=True),
        ),
    ]