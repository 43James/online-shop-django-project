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
    other = models.CharField(max_length=50 ,blank=True, null=True, verbose_name='หมายเหตุ')

    class Meta:
        ordering = ('-id',)
    
    def __str__(self):
        return str(self.id)
  
    
    # def get_approval_count(self):
    #     return Order.objects.filter(status=False, refuse=False).count()
    # def get_approval_count(self):
    #     # นับจำนวนออเดอร์ที่รอการยืนยัน
    #     approval_count = Order.objects.filter(status=False, refuse=False).count()
    #     return approval_count

    @property
    def get_approval_count(self):
        return Order.objects.filter(status=False).count()

    @property
    def get_total_price(self):
        total = sum(item.get_cost() for item in self.items.all())
        return total
    
    @property
    def get_total_sum(self):
        total = sum(item.get_total() for item in self.items.all())
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
    
    def get_total(self):
        return self.quantity