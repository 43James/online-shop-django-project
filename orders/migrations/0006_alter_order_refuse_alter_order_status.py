# Generated by Django 4.0 on 2023-10-25 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_alter_orderitem_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='refuse',
            field=models.BooleanField(default=False, verbose_name='ปฏิเสธ'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.BooleanField(default=False, verbose_name='อนุมัติ'),
        ),
    ]