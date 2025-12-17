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
    path('blog/posts/<int:pk>/', admin_views.AdminBlogPostDetailView.as_view(), name='admin-blog-detail'),
    path('blog/posts/<int:pk>/update/', admin_views.AdminBlogPostUpdateView.as_view(), name='admin-blog-update'),
    path('blog/posts/<int:pk>/delete/', admin_views.AdminBlogPostDeleteView.as_view(), name='admin-blog-delete'),

    # Categories and Tags
    path('blog/categories/', admin_views.AdminCategoryListView.as_view(), name='admin-categories-list'),
    path('blog/categories/create/', admin_views.AdminCategoryCreateView.as_view(), name='admin-categories-create'),
    path('blog/tags/', admin_views.AdminTagListView.as_view(), name='admin-tags-list'),
    path('blog/tags/create/', admin_views.AdminTagCreateView.as_view(), name='admin-tags-create'),

    # User Management
    path('users/', admin_views.admin_users_list, name='admin-users-list'),
    path('users/<int:user_id>/', admin_views.admin_user_detail, name='admin-user-detail'),
    path('users/<int:user_id>/update/', admin_views.admin_user_update, name='admin-user-update'),
    path('users/<int:user_id>/delete/', admin_views.admin_user_delete, name='admin-user-delete'),

    # Review Management
    path('reviews/', admin_views.admin_reviews_list, name='admin-reviews-list'),
    path('reviews/<int:review_id>/update/', admin_views.admin_review_update, name='admin-review-update'),
    path('reviews/<int:review_id>/delete/', admin_views.admin_review_delete, name='admin-review-delete'),
    path('reviews/<int:review_id>/approve/', admin_views.admin_review_approve, name='admin-review-approve'),

    # Enquiry Management
    path('enquiries/', admin_views.admin_enquiries_list, name='admin-enquiries-list'),
    path('enquiries/<int:enquiry_id>/', admin_views.admin_enquiry_detail, name='admin-enquiry-detail'),

    # Offer Management
    path('offers/', admin_views.admin_offers_list, name='admin-offers-list'),
    path('offers/create/', admin_views.create_offer, name='admin-offers-create'),
    path('offers/<int:offer_id>/', admin_views.admin_offer_detail, name='admin-offer-detail'),
    path('offers/<int:offer_id>/update/', admin_views.admin_offer_update, name='admin-offer-update'),
    path('offers/<int:offer_id>/delete/', admin_views.admin_offer_delete, name='admin-offer-delete'),

    # File Upload
    path('upload/', admin_views.upload_file, name='admin-upload'),
]
