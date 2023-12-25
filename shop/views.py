from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
# from dashboard.views import products

from shop.models import Product, Category, Subcategory
from django.db.models import Q
from cart.forms import QuantityForm
from .filters import FilterProduct, FilterSubcategory



def paginat(request, list_objects):
	p = Paginator(list_objects, 20)
	page_number = request.GET.get('page')
	try:
		page_obj = p.get_page(page_number)
	except PageNotAnInteger:
		page_obj = p.page(1)
	except EmptyPage:
		page_obj = p.page(p.num_pages)
	return page_obj

@login_required
def home_page(request):
	products = Product.objects.all()
	context = {'products': paginat(request ,products),}
	return render(request, 'home_page.html', context)

@login_required
def search_category(request):
    # print(request.POST.get('filters'))
    prod = Product.objects.all()
    filters = FilterProduct(request.GET, queryset=prod) 
    filter = filters.qs

    page = request.GET.get('page')
    p = Paginator(filter, 5)
    try:
        filter = p.page(page)
    except:
        filter = p.page(1)

    return render(request, 'bookreceives/Breceive_list.html', {
        "prod" : prod,
        "page" : page,
        "filters" : filters,
        "filter" : filter,
        "Subcategory" : Subcategory.objects.all(),
    })


@login_required
def product_detail(request, slug):
	form = QuantityForm()
	product = get_object_or_404(Product, slug=slug)
	related_products = Product.objects.filter(category=product.category).all()[:5]
	context = {
		'title':product.title,
		'product':product,
		'form':form,
		'favorites':'favorites',
		'related_products':related_products
	}
	if request.user.likes.filter(id=product.id).first():
		context['favorites'] = 'remove'
	return render(request, 'product_detail.html', context)


@login_required
def add_to_favorites(request, product_id):
	product = get_object_or_404(Product, id=product_id)
	request.user.likes.add(product)
	return redirect('shop:product_detail', slug=product.slug)


@login_required
def remove_from_favorites(request, product_id):
	product = get_object_or_404(Product, id=product_id)
	request.user.likes.remove(product)
	return redirect('shop:favorites')


@login_required
def favorites(request):
	products = request.user.likes.all()
	context = {'title':'Favorites', 'products':products}
	return render(request, 'favorites.html', context)

@login_required
def search(request):
	query = request.GET.get('q')
	products = Product.objects.filter(title__icontains=query).all()
	context = {'products': paginat(request ,products)}
	return render(request, 'home_page.html', context)


@login_required
def filter_by_category(request, category_id=None, subcategory_id=None):
    categories = Category.objects.all()

    if category_id:
        category = get_object_or_404(Category, pk=category_id)
        subcategories = Subcategory.objects.filter(category=category)
    else:
        category = None
        subcategories = None

    if subcategory_id:
        subcategory = get_object_or_404(Subcategory, pk=subcategory_id)
        products = Product.objects.filter(category=subcategory)
    else:
        subcategory = None
        products = Product.objects.all()

    context = {
        'categories': categories,
        'selected_category': category,
        'subcategories': subcategories,
        'selected_subcategory': subcategory,
        'products': products,
    }

    return render(request, 'home_page.html', context)