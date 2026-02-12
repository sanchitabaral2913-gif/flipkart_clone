from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.home_view, name='home'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('settings/', views.settings_view, name='settings'),
    # Auth
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Profile
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),

    # Posts + Reels
    path('post/create/', views.create_post, name='create_post'),
    path('reels/', views.reels_view, name='reels'),
    path('reels/<int:reel_id>/comment/', views.add_comment, name='add_comment'),
    path('reels/<int:reel_id>/like/', views.toggle_like, name='toggle_like'),

    # Messaging + Search
    path('messages/<str:username>/', views.messages_view, name='messages'),
    path('search/', views.search_view, name='search'),
]
