from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from cart.utils.cart import Cart
from .forms import QuantityForm
from shop.models import Product
from .cart import Cart


@login_required
def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = QuantityForm(request.POST)
    
    if form.is_valid():
        data = form.cleaned_data
        quantity = data['quantity']
        
        if product.number <= 0:
            messages.error(request, 'This product is out of stock.')
            return redirect('shop:product_detail', slug=product.slug)
        elif quantity > product.number:
            messages.error(request, 'Not enough stock available.')
            return redirect('shop:product_detail', slug=product.slug)
        else:
            cart.add(product=product, quantity=quantity)
            product.number -= quantity
            product.save()
            messages.success(request, 'Added to your cart!')
            return redirect('shop:product_detail', slug=product.slug)



@login_required
def show_cart(request):
    cart = Cart(request)
    cart_data = cart.get_cart()  # ใช้ get_cart เพื่อดึงข้อมูลตะกร้า

    context = {'title': 'Cart', 'cart_data': cart_data}
    return render(request, 'cart.html', context)



@login_required
def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    if product:
        # หาจำนวนสินค้าในตะกร้าที่ถูกลบ
        removed_quantity = cart.get_item_quantity(product)
        
        # ลบสินค้าออกจากตะกร้า
        cart.remove(product)
        
        # เพิ่มจำนวนสินค้าที่ถูกลบกลับไปยังสินค้าตามเดิม
        product.number += removed_quantity
        product.save()
        messages.success(request, 'Removed from your cart!')
    
    return redirect('cart:show_cart')






# def add_to_cart(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Product, id=product_id)
#     form = QuantityForm(request.POST)
#     if form.is_valid():
#         data = form.cleaned_data
#         cart.add(product=product, quantity=data['quantity'])
#         messages.success(request, 'Added to your cart!', 'info')
#     return redirect('shop:product_detail', slug=product.slug)

# @login_required
# def show_cart(request):
#     cart = Cart(request)
#     context = {'title': 'Cart', 'cart': cart}
#     return render(request, 'cart.html', context)




# @login_required
# def remove_from_cart(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Product, id=product_id)
#     cart.remove(product)
#     return redirect('cart:show_cart')


# def remove_from_cart(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Product, id=product_id)

#     # หาสินค้าที่ต้องการลบในตระกร้า
#     for item in cart:
#         if item['product'].id == product_id:
#             cart.remove(product)  # ลบสินค้าออกจากตระกร้า
#             product.number += item['quantity']  # เพิ่มจำนวนสินค้ากลับไปยังสต็อก
#             product.save()

#     messages.success(request, 'ลบสินค้าออกจากตระกร้าแล้ว')
#     return redirect('cart:show_cart')


# @login_required
# def remove_from_cart(request, product_id):
#     cart = Cart(request)

#     # หาสินค้าที่ต้องการลบในตระกร้า
#     products_to_remove = []
#     for item in cart:
#         if item['product'].id == product_id:
#             products_to_remove.append(item)  # เก็บสินค้าไว้ในรายการที่ต้องการลบ

#     for item in products_to_remove:
#         cart.remove(product_id)  # ลบสินค้าออกจากตระกร้า

#         product = Product.objects.get(id=product_id)  # ดึงข้อมูลสินค้าจาก ID
#         product.number += item['quantity']  # เพิ่มจำนวนสินค้ากลับไปยังสต็อก
#         product.save()

#     messages.success(request, 'ลบสินค้าออกจากตระกร้าแล้ว')
#     return redirect('cart:show_cart')


# @login_required
# def remove_from_cart(request, product_id):
#     cart = Cart(request)

#     # หาสินค้าที่ต้องการลบในตระกร้า
#     products_to_remove = []
#     for item in cart:
#         if item['product'].id == int(product_id):
#             products_to_remove.append(item)  # เก็บสินค้าไว้ในรายการที่ต้องการลบ

#     for item in products_to_remove:
#         cart.remove(int(product_id))  # ลบสินค้าออกจากตระกร้า

#         product = Product.objects.get(id=product_id)  # ดึงข้อมูลสินค้าจาก ID
#         product.number += item['quantity']  # เพิ่มจำนวนสินค้ากลับไปยังสต็อก
#         product.save()

#     messages.success(request, 'ลบสินค้าออกจากตระกร้าแล้ว')
#     return redirect('cart:show_cart')



# @login_required
# def remove_from_cart(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Product, id=product_id)
    
#     if product:
#         # เพิ่มจำนวนสินค้ากลับไปยังสินค้าตามเดิม
#         cart.remove(product)
#         product.number += cart['quantity']  # เพิ่มจำนวนสินค้าที่ถูกลบออกจากตะกร้า
#         product.save()
#         messages.success(request, 'Removed from your cart!')
    
#     return redirect('cart:show_cart')


