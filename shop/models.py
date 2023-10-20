from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify

class Category(models.Model):
    name = models.CharField(max_length=100,)

    def __str__(self):
        return self.name
    
class Subcategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='หมวดหมู่ย่อย')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='หมวดหมู่หลัก')

    def __str__(self):
        return self.name
    
# class Category(models.Model):
#     title = models.CharField(max_length=200)
#     sub_category = models.ForeignKey(
#         'self', on_delete=models.CASCADE,
#         related_name='sub_categories', null=True, blank=True
#     )
#     is_sub = models.BooleanField(default=False)
#     slug = models.SlugField(max_length=200, unique=True)

#     def __str__(self):
#         return self.title

#     def get_absolute_url(self):
#         return reverse('shop:product_detail', kwargs={'slug':self.slug})

#     def save(self, *args, **kwargs): # new
#         self.slug = slugify(self.title)
#         return super().save(*args, **kwargs)
        
class Product(models.Model):
    category = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='Subcategory', null=True, blank=True, verbose_name='หมวดหมู่')
    image = models.ImageField(upload_to='products', verbose_name='รูปภาพ')
    code = models.CharField(max_length=50, unique=True, verbose_name='เลขพัสดุ/ครุภัณฑ์')
    slug = models.SlugField(max_length=300, unique=True)
    title = models.CharField(max_length=250, verbose_name='ชื่อรายการ')
    description = models.TextField(verbose_name='อื่นๆ')
    number = models.IntegerField(default=0, null=True, verbose_name='จำนวน')
    price = models.IntegerField(verbose_name='ราคา')
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.slug
        
    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.code)
        return super().save(*args, **kwargs)