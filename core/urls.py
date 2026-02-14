# from django.urls import path
# from . import views

# urlpatterns = [
#     # Home
#     path('', views.home, name='home'),
#     path('products/', views.product_list, name='product_list'),
#     path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    
#     # Auth
#     path('register/', views.register, name='register'),
#     path('login/', views.user_login, name='login'),
#     path('logout/', views.user_logout, name='logout'),
#     path('profile/', views.profile, name='profile'),
    
#     # Cart
#     path('cart/', views.cart_view, name='cart'),
#     path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
#     path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
#     path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),
    
#     # Order
#     path('checkout/', views.checkout, name='checkout'),
#     path('order/<int:order_id>/', views.order_detail, name='order_detail'),
#     path('orders/', views.order_history, name='order_history'),
    
#     # Payment
#     path('payment/submit/<int:order_id>/', views.submit_payment, name='submit_payment'),
#     path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
# ]


# core/urls.py
from django.urls import path
from . import views 

urlpatterns = [
    # Home & Products
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    
    # Auth
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # Cart
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),
    
    # Order
    path('checkout/', views.checkout, name='checkout'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/', views.order_history, name='order_history'),
    path('payment/submit/<int:order_id>/', views.submit_payment, name='submit_payment'),
    
    # ===== ADMIN DASHBOARD URLS =====
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    
    # Order Management API
    path('admin/orders/<int:order_id>/confirm/', views.admin_confirm_order, name='admin_confirm_order'),
    path('admin/orders/<int:order_id>/cancel/', views.admin_cancel_order, name='admin_cancel_order'),
    path('admin/orders/<int:order_id>/update-status/', views.admin_update_order_status, name='admin_update_order_status'),
    path('admin/orders/<int:order_id>/details/', views.admin_get_order_details, name='admin_get_order_details'),
    path('admin/orders/status/<str:status>/', views.admin_get_orders_by_status, name='admin_get_orders_by_status'),
    path('admin/orders/<int:order_id>/cancel/', views.admin_cancel_order, name='admin_cancel_order'),
    path('orders/<int:order_id>/cancel/', views.user_cancel_order, name='user_cancel_order'),

    # Payment Management API
    path('admin/payments/<int:payment_id>/verify/', views.admin_verify_payment, name='admin_verify_payment'),
    
    # Product Management API
    path('admin/products/', views.admin_get_products, name='admin_get_products'),
    path('admin/products/add/', views.admin_add_product, name='admin_add_product'),
    path('admin/products/<int:product_id>/update/', views.admin_update_product, name='admin_update_product'),
    path('admin/products/<int:product_id>/delete/', views.admin_delete_product, name='admin_delete_product'),
    
    
    # Category Management API
    path('admin/categories/', views.admin_get_categories, name='admin_get_categories'),
    path('admin/categories/add/', views.admin_add_category, name='admin_add_category'),
    path('admin/categories/<int:category_id>/delete/', views.admin_delete_category, name='admin_delete_category'),
]