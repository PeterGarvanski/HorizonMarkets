# Generated by Django 4.2.10 on 2024-03-26 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0004_alter_tradehistory_close_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opentrade',
            name='quantity',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
        migrations.AlterField(
            model_name='opentrade',
            name='stop_loss',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='opentrade',
            name='take_profit',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=20, null=True),
        ),
    ]
