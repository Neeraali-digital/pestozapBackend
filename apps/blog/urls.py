"""
URL configuration for the blog app.
"""
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Categories and Tags
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('tags/', views.TagListView.as_view(), name='tag-list'),
    
    # Blog Posts
    path('posts/', views.BlogPostListView.as_view(), name='post-list'),
    path('posts/create/', views.BlogPostCreateView.as_view(), name='post-create'),
    path('posts/featured/', views.FeaturedBlogPostsView.as_view(), name='featured-posts'),
    path('posts/<slug:slug>/', views.BlogPostDetailView.as_view(), name='post-detail'),
    path('posts/<slug:slug>/related/', views.RelatedBlogPostsView.as_view(), name='related-posts'),
    
    # Comments
    path('posts/<slug:slug>/comments/', views.BlogPostCommentsView.as_view(), name='post-comments'),
    
    # Likes
    path('posts/<slug:slug>/like/', views.toggle_blog_like, name='toggle-like'),
    
    # Statistics
    path('stats/', views.blog_stats, name='blog-stats'),
]