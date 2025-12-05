"""
URL configuration for the users app.
"""
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('profile/update/', views.UserUpdateView.as_view(), name='user-update'),
    path('profile/extended/', views.UserProfileDetailView.as_view(), name='user-profile-extended'),
    path('profile/picture/upload/', views.upload_profile_picture, name='upload-profile-picture'),
    path('profile/picture/delete/', views.delete_profile_picture, name='delete-profile-picture'),
    path('stats/', views.user_stats, name='user-stats'),
    path('create-admin/', views.create_admin, name='create-admin'),
]