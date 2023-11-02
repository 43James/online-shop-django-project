from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    # เพิ่มเมธอดเพื่อดึงข้อมูลตะกร้าและแปลงให้อยู่ในรูป List
    def get_cart(self):
        cart_data = []
        for item_id, item_data in self.cart.items():
            product = Product.objects.get(id=item_id)
            cart_data.append({
                'product': product,
                'quantity': item_data['quantity'],
                'price': item_data['price'],
            })
        return cart_data

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def get_item_count(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_item_quantity(self, product):
        product_id = str(product.id)
        return self.cart[product_id]['quantity'] if product_id in self.cart else 0

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
