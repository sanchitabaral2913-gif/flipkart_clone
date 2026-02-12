from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu_view, name='menu'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('about/', views.about, name='about'),
    path('booktable/', views.booktable, name='booktable'),
    path('feedback/', views.feedback, name='feedback'),
    path('order/', views.order_view, name='order'),
    path('update-cart/', views.update_cart, name='update_cart'),
]
