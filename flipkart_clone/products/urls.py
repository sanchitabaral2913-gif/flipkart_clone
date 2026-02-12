from django.urls import path
from . import views

urlpatterns = [
    # HOME & PRODUCTS
    path('', views.product_list, name='home'),
    path('products/', views.all_products, name='all_products'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('category/<str:category_name>/', views.category_products, name='category_products'),
    path('product_list/', views.product_list, name='product_list'),

    # SELLER
    path('seller/dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('add_product/', views.add_product, name='add_product'),
    path('my_products/', views.my_products, name='my_products'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    

    # ADMIN
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('product/<int:product_id>/approve/', views.approve_product, name='approve_product'),
    path('product/<int:product_id>/reject/', views.reject_product, name='reject_product'),
    

    # REVIEW (CUSTOMER)
    path('product/<int:pk>/add_review/', views.product_detail, name='add_review'),  # POST handled in product_detail
    path('review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    

    # CUSTOMER DASHBOARD
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
]
