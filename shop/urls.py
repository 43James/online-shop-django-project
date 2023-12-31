from django.urls import path

from shop import views
# from .views import filter_by_category

app_name = "shop"

urlpatterns = [
	path('home_page', views.home_page, name='home_page'),
	path('<slug:slug>', views.product_detail, name='product_detail'),
	path('add/favorites/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
	path('remove/favorites/<int:product_id>/', views.remove_from_favorites, name='remove_from_favorites'),
	path('favorites/', views.favorites, name='favorites'),
	path('search/', views.search, name='search'),
	path('search-category/', views.search_category, name='search_category'),
	# path('filter/<slug:slug>/', views.filter_by_category, name='filter_by_category'),
    # path('filter_by_category/<int:category_id>/', filter_by_category, name='filter_by_category'),
	path('filter_by_category/<int:category_id>/', views.filter_by_category, name='filter_by_category'),
    path('filter_by_category/<int:category_id>/<int:subcategory_id>/', views.filter_by_category, name='filter_by_category'),
    
]
    
