# Generated by Django 4.0 on 2023-10-17 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_category_name_alter_product_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.ImageField(default='', upload_to='', verbose_name='ราคา'),
        ),
    ]