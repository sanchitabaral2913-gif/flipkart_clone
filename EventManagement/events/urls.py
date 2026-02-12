from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('book/', views.book_event, name='book_event'),
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('booked_events/', views.booked_events, name='booked_events'),
    path('edit-event/<int:event_id>/', views.edit_event, name='edit_event'),

]
