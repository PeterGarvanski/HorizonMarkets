# Generated by Django 4.2.10 on 2024-03-04 16:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_rename_type_of_transaction_transaction_transaction_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='transaction_type',
            new_name='transfer_type',
        ),
    ]