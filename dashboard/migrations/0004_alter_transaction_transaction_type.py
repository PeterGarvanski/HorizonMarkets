# Generated by Django 4.2.10 on 2024-03-03 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_transaction_city_transaction_country_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(choices=[('Withdraw', 'Withdraw'), ('Deposit', 'Deposit')], default='Deposit', max_length=10),
        ),
    ]
