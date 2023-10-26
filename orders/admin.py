from django.contrib import admin

from .models import Order, OrderItem

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','user','created','status','refuse','date_receive']

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id','order','product','price','quantity']

admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)