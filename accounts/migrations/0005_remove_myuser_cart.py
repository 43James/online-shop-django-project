# Generated by Django 4.0 on 2023-11-03 04:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_profile_cart_myuser_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='cart',
        ),
    ]
