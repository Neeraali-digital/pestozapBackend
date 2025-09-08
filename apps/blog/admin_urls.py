"""
Admin URL configuration for the blog app.
"""
from django.urls import path
from . import admin_views

app_name = 'blog_admin'

urlpatterns = [
    # Dashboard
    path('dashboard/stats/', admin_views.dashboard_stats, name='dashboard-stats'),
    
    # Blog Management
    path('blog/posts/', admin_views.AdminBlogPostListView.as_view(), name='admin-blog-list'),
    path('blog/posts/create/', admin_views.AdminBlogPostCreateView.as_view(), name='admin-blog-create'),
    path('blog/posts/<int:pk>/', admin_views.AdminBlogPostDetailView.as_view(), name='admin-blog-detail'),
    
    # User Management
    path('users/', admin_views.admin_users_list, name='admin-users-list'),
    
    # Review Management
    path('reviews/', admin_views.admin_reviews_list, name='admin-reviews-list'),
    
    # Enquiry Management
    path('enquiries/', admin_views.admin_enquiries_list, name='admin-enquiries-list'),
    
    # Offer Management
    path('offers/', admin_views.admin_offers_list, name='admin-offers-list'),
    path('offers/create/', admin_views.create_offer, name='admin-offers-create'),
]