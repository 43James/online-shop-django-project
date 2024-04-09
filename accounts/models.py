from django.db import models
# from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
# from .managers import UserManager
from shop.models import Product
from django.utils.html import format_html

class WorkGroup(models.Model):
    work_group = models.CharField(max_length=150, verbose_name='กลุ่มงาน')

    class Meta:
        ordering = ['-id']
        verbose_name_plural='กลุ่มงาน'

    def __str__(self):
        return self.work_group
    


class MyUser(AbstractUser):
    
    PREFIX_CHOICES = [
        ('นาย', 'นาย'),
        ('นาง', 'นาง'),
        ('นางสาว', 'นางสาว'),
    ]

    perfix = models.CharField(max_length=10, blank=True, null=True, verbose_name="คำนำหน้า", choices=PREFIX_CHOICES)
    email = models.EmailField(max_length=100, verbose_name="อีเมล", unique=True)
    is_general = models.BooleanField(default=False, verbose_name='ผู้ใช้งานทั่วไป' , blank=True, null=True)
    is_manager = models.BooleanField(default=False, verbose_name='ผู้จัดการคลัง', blank=True, null=True)
    is_admin = models.BooleanField(default=False, verbose_name='ผู้ดูแลระบบ' , blank=True, null=True)
    likes = models.ManyToManyField(Product, blank=True, related_name='likes')

    class Meta:
        ordering = ['-id']
        verbose_name='สมาชิกผู้ใช้งาน (Users)'

    def __str__(self):
        return self.username

    def get_likes_count(self):
        return self.likes.count()
    
    def get_full_name(self):
        return f"{self.perfix}{self.first_name}   {self.last_name}"

class Profile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, default='', verbose_name='เพศ')
    # work_group = models.CharField(max_length=150, verbose_name='กลุ่มงาน')
    workgroup = models.ForeignKey(WorkGroup,max_length=150, on_delete=models.CASCADE, verbose_name='กลุ่มงาน', blank=True, null=True)
    position = models.CharField(max_length=150, verbose_name='ตำแหน่ง')
    phone = models.CharField(max_length=10, verbose_name='เบอร์โทรศัพท์มือถือ')
    img = models.ImageField(upload_to='Image_users', verbose_name='รูปโปรไฟล์',blank=True, null=True )
    updatedAt = models.DateTimeField(auto_now=True, blank=False)

    def __str__(self):
        return str(self.user) + str(self.gender) + str(self.position) + self.phone

    def image(self):
        if self.img:
            return format_html('<img src="' + self.img.url + '" height="40px">')
        return ''
    image.allow_tags = True
    # image.short_description = "รูปภาพ"
    

    
