# Generated by Django 4.0 on 2023-11-10 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_alter_cartitem_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='price',
            field=models.PositiveIntegerField(),
        ),
    ]
