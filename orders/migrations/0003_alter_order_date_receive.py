# Generated by Django 4.0 on 2023-10-17 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_order_return_status_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_receive',
            field=models.DateTimeField(null=True, verbose_name='วันที่รับของ'),
        ),
    ]
