# Generated by Django 4.2.10 on 2024-03-26 11:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tradehistory',
            old_name='price',
            new_name='entry_price',
        ),
    ]
