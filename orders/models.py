from django.db import models

from accounts.models import MyUser
from shop.models import Product


class Order(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='orders')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False, verbose_name="อนุมัติ")
    refuse = models.BooleanField(default=False, verbose_name="ปฏิเสธ")
    date_receive = models.DateTimeField(blank=True, null=True, verbose_name='วันที่รับของ')

    class Meta:
        ordering = ('-id',)
    
    def __str__(self):
        return str(self.id)

    @property
    def get_total_price(self):
        total = sum(item.get_cost() for item in self.items.all())
        return total
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price = models.PositiveIntegerField()
    quantity = models.SmallIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity