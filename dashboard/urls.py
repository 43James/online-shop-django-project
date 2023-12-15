from django.urls import path

from dashboard import views

app_name = 'dashboard'

urlpatterns = [
    path('dashboard_home/', views.dashboard_home, name='dashboard_home'),
    path('products/', views.products, name='products'),
    path('products/delete/<int:id>/', views.delete_product, name='delete_product'),
    path('products/edit/<int:id>/', views.edit_product, name='edit_product'),
    path('orders/', views.orders, name='orders'),
    path('orders_all/', views.orders_all, name='orders_all'),
    # path('approve/orders/<int:id>', views.approve_orders, name='approve_orders'),
    path('approve/orders/<int:order_id>/', views.approve_orders, name='approve_orders'),
    path('orders_all/detail/<int:id>', views.order_detail, name='order_detail'),
    path('add-product/', views.add_product, name='add_product'),
    path('add-category/', views.add_category, name='add_category'),
    path('add-subcategory/', views.add_subcategory, name='add_subcategory'),
]
