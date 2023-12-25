from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cart.utils.cart import Cart
from .forms import QuantityForm
# from cart.models import CartItem
from shop.models import Product
# from .cart import Cart


@login_required
def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = QuantityForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        cart.add(product=product, quantity=data['quantity'])
        product.number -= data['quantity']  # ลดจำนวนสินค้าในสต๊อก
        product.save()
        messages.success(request, 'เพิ่มลงในตะกร้าแล้ว!')
    return redirect('shop:product_detail', slug=product.slug)


@login_required
def show_cart(request):
    cart = Cart(request)
    context = {'title': 'Cart', 'cart': cart}
    return render(request, 'cart.html', context)


@login_required
def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    # ตรวจสอบว่า product_id มีอยู่ใน cart หรือไม่
    if str(product_id) in cart.cart:
        # เก็บข้อมูลสินค้าก่อนลบ
        removed_item = cart.cart[str(product_id)].copy()
        cart.remove(product)

        # เพิ่มจำนวนสินค้าในสต็อกเมื่อลบออกจากตะกร้า
        product.number += removed_item['quantity']
        product.save()

        return redirect('cart:show_cart')
    else:
        messages.error(request, 'ไม่พบสินค้าในตะกร้า')
        return redirect('cart:show_cart')

