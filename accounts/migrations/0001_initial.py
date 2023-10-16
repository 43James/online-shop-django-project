# Generated by Django 4.0 on 2023-10-10 06:58

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=100, unique=True, verbose_name='อีเมล')),
                ('is_general', models.BooleanField(blank=True, default=False, null=True, verbose_name='ผู้ใช้งานทั่วไป')),
                ('is_manager', models.BooleanField(blank=True, default=False, null=True, verbose_name='ผู้จัดการคลัง')),
                ('is_admin', models.BooleanField(blank=True, default=False, null=True, verbose_name='ผู้ดูแลระบบ')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('likes', models.ManyToManyField(blank=True, related_name='likes', to='shop.Product')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'สมาชิกผู้ใช้งาน (Users)',
                'ordering': ['-id'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(default='', max_length=10, verbose_name='เพศ')),
                ('work_group', models.CharField(max_length=150, verbose_name='กลุ่มงาน')),
                ('position', models.CharField(max_length=150, verbose_name='ตำแหน่ง')),
                ('phone', models.CharField(max_length=10, verbose_name='เบอร์โทรศัพท์มือถือ')),
                ('img', models.ImageField(default='', upload_to='Image_users', verbose_name='รูปภาพ')),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.myuser')),
            ],
        ),
    ]
