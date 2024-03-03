# Generated by Django 4.2.10 on 2024-03-03 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='city',
            field=models.CharField(default='N/A', max_length=50),
        ),
        migrations.AddField(
            model_name='transaction',
            name='country',
            field=models.CharField(default='N/A', max_length=40),
        ),
        migrations.AddField(
            model_name='transaction',
            name='postal_code',
            field=models.CharField(default='N/A', max_length=10),
        ),
        migrations.AddField(
            model_name='transaction',
            name='street_name',
            field=models.CharField(default='N/A', max_length=50),
        ),
        migrations.AddField(
            model_name='transaction',
            name='street_number',
            field=models.IntegerField(default=0),
        ),
    ]
