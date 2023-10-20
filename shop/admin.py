from django.contrib import admin

from .models import Category, Product, Subcategory

class ProductAdmin(admin.ModelAdmin):
    list_display = ['code', 'title']
    prepopulated_fields = {'slug':['code']}


admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Product, ProductAdmin)

