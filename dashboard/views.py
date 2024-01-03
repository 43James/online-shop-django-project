from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import Http404, JsonResponse
from django.core.paginator import Paginator
from app_linebot.views import notify_user_approved
from django.db.models import Q
from shop.models import Product
from accounts.models import MyUser, Profile
from orders.models import Order, OrderItem
from .forms import AddProductForm, AddCategoryForm, AddSubcategoryForm, EditProductForm, ApproveForm


def count_pending_orders():
    # ดึงข้อมูลออเดอร์ทั้งหมดที่รอการยืนยัน
    pending_orders = Order.objects.filter(status=False, refuse=False)
    return pending_orders.count()


def is_manager(user):
    try:
        if not user.is_manager:
            raise Http404
        return True
    except:
        raise Http404


@user_passes_test(is_manager)
@login_required
def dashboard_home(request):
    context = {'title':'dashboard' ,
               'products':products ,
                'pending_orders_count': count_pending_orders(),
               }
    return render(request, 'dashboard_home.html', context)


@user_passes_test(is_manager)
@login_required
def products(request):
    products = Product.objects.all()

    query = request.GET.get('q')
    if query is not None:
        lookups = Q(title__icontains=query) | Q(code__icontains=query)
        products = Product.objects.filter(lookups)


    page = request.GET.get('page')

    p = Paginator(products, 8)
    try:
        products = p.page(page)
    except:
        products = p.page(1)

    context = {
        'title':'รายการวัสดุทั้งหมด' ,
        'products':products,
        'pending_orders_count': count_pending_orders(),
        }
    return render(request, 'products.html', context)


@user_passes_test(is_manager)
@login_required
def add_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'เพิ่มวัสดุเรียบร้อยแล้ว!')
            return redirect('dashboard:add_product')
    else:
        form = AddProductForm()
    context = {'title':'เพิ่มวัสดุ', 'form':form,
                'pending_orders_count': count_pending_orders(),}
    return render(request, 'add_product.html', context)


@user_passes_test(is_manager)
@login_required
def delete_product(request, id):
    product = Product.objects.filter(id=id).delete()
    messages.success(request, 'ลบวัสดุสำเร็จ')
    return redirect('dashboard:products')


@user_passes_test(is_manager)
@login_required
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = EditProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'อัพเดทวัสดุ สำเร็จ')
            return redirect('dashboard:products')
    else:
        form = EditProductForm(instance=product)
    context = {'title': 'Edit Product', 
               'form':form,
                'pending_orders_count': count_pending_orders(),}
    return render(request, 'edit_product.html', context)


@user_passes_test(is_manager)
@login_required
def add_category(request):
    if request.method == 'POST':
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'เพิ่มหมวดหมู่เรียบร้อยแล้ว!')
            return redirect('dashboard:add_category')
    else:
        form = AddCategoryForm()
    context = {'title':'เพิ่มหมวดหมู่หลัก', 
               'form':form,
                'pending_orders_count': count_pending_orders(),}
    return render(request, 'add_category.html', context)


@user_passes_test(is_manager)
@login_required
def add_subcategory(request):
    if request.method == 'POST':
        form = AddSubcategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'เพิ่มหมวดหมู่ย่อยเรียบร้อยแล้ว!')
            return redirect('dashboard:add_subcategory')
    else:
        form = AddSubcategoryForm()
    context = {'title':'เพิ่มหมวดหมู่ย่อย', 
               'form':form,
                'pending_orders_count': count_pending_orders(),}
    return render(request, 'add_subcategory.html', context)


@user_passes_test(is_manager)
@login_required
def orders_all(request):
    orders_all = Order.objects.all()

    query = request.GET.get('q')
    if query is not None:
        lookups = Q(id__icontains=query)
        orders_all = Order.objects.filter(lookups)

    page = request.GET.get('page')
    p = Paginator(orders_all, 7)
    try:
        orders_all = p.page(page)
    except:
        orders_all = p.page(1)

    context = {
        'title':'คำร้องเบิกวัสดุทั้งหมด', 
        'orders_all':orders_all,
        'pending_orders_count': count_pending_orders(),
        }
    return render(request, 'orders_all.html', context)


@login_required
def orders(request):
    orders = Order.objects.all()

    page = request.GET.get('page')
    p = Paginator(orders, 8)
    try:
        orders = p.page(page)
    except:
        orders = p.page(1)

    # ดึงข้อมูลออร์เดอร์ทั้งหมดที่รอการยืนยัน
    orders_waiting_approval = Order.objects.filter(status=False, refuse=False)

    # ส่งข้อมูล approval_count ไปยัง template
    context = {
        'title':'คำร้องใหม่',
        'orders':'orders',
        'orders':orders_waiting_approval,
        'approval_count': orders_waiting_approval.count(),
        'pending_orders_count': count_pending_orders(),
        }
    return render(request, 'orders.html', context)


@login_required
def approve_orders(request, order_id):
    ap = Order.objects.get(id = order_id)
    form = ApproveForm()
    
    if request.method == 'POST':
        form = ApproveForm(request.POST, instance = ap)

        if form.is_valid():
            form.save()
            id=form.instance.id
            messages.success(request, 'ดำเนินการสำเร็จ')

            # Notify the user about the approval
            notify_user_approved(id)
            
            return redirect(reverse('dashboard:order_detail', args=[order_id]))
        else :
            messages.error(request, 'ดำเนินการไม่สำเร็จ')
            
    return render(request, 'orders.html', {
        'ap':ap,
        'form': form,
        'title' : 'แก้ไขข้อมูลสมาชิก',
        'pending_orders_count': count_pending_orders(),
    })

@user_passes_test(is_manager)
@login_required
def order_detail(request, id):
    order = Order.objects.filter(id=id).first()
    items = OrderItem.objects.filter(order=order).all()
    context = {
        'title':'รายการเบิกจ่ายวัสดุ', 
        'items':items, 
        'order':order,
        'pending_orders_count': count_pending_orders(),
        }
    return render(request, 'order_detail.html', context)
