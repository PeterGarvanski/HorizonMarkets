# Generated by Django 4.2.10 on 2024-03-04 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_alter_transaction_transaction_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='street_name',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='street_number',
        ),
        migrations.AddField(
            model_name='transaction',
            name='address_line_1',
            field=models.CharField(default='N/A', max_length=100),
        ),
    ]
