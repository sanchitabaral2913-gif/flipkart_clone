from django.urls import path
from . import views

urlpatterns = [
    path('my-orders/', views.my_orders, name='my_orders'),
    path('order/<int:order_id>/', views.order_detail_view, name='order_detail'),

    # Cart
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/increment/<int:cart_id>/', views.cart_increment, name='cart_increment'),
    path('cart/decrement/<int:cart_id>/', views.cart_decrement, name='cart_decrement'),
    path('cart/remove/<int:cart_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),

    # Seller orders
    path('seller/orders/', views.seller_orders, name='seller_orders'),
    path('seller/complete-order/<int:order_id>/', views.complete_order, name='complete_order'),
    path('seller/pending-orders/', views.seller_pending_orders, name='seller_pending_orders'),
    path('update-order/<int:order_id>/<str:status>/',
         views.update_order_status,
         name='update_order_status'),

]
