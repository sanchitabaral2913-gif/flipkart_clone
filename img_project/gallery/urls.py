from django.urls import path
from . import views

urlpatterns = [
    path('', views.gallery_view, name='gallery'),
    path('<str:category>/', views.gallery_view, name='gallery_by_category'),
]
