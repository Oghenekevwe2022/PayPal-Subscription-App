# Generated by Django 5.0.4 on 2024-05-10 23:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscription',
            old_name='paypal_id',
            new_name='paypal_subscription_id',
        ),
    ]
