# Generated by Django 3.2 on 2024-01-04 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_myuser_perfix'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_group', models.CharField(max_length=150, verbose_name='กลุ่มงาน')),
            ],
            options={
                'verbose_name': 'กลุ่มงาน',
                'ordering': ['-id'],
            },
        ),
    ]
