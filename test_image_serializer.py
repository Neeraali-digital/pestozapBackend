#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pestozap_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.blog.models import BlogPost, Category
from apps.blog.serializers import BlogPostListSerializer
from django.test import RequestFactory

User = get_user_model()

# Create test data
admin_user = User.objects.filter(is_staff=True).first()
if not admin_user:
    admin_user = User.objects.create_superuser(
        email='admin@test.com',
        password='admin123',
        first_name='Admin',
        last_name='User'
    )

# Create category
category, _ = Category.objects.get_or_create(
    name='Tips & Tricks',
    defaults={'is_active': True}
)

# Create blog post
blog_post, created = BlogPost.objects.get_or_create(
    title='Test Blog Post',
    defaults={
        'excerpt': 'Test excerpt',
        'content': 'Test content',
        'category': category,
        'author': admin_user,
        'status': 'published'
    }
)

# Test serializer
factory = RequestFactory()
request = factory.get('/')
request.user = admin_user

serializer = BlogPostListSerializer(blog_post, context={'request': request})
data = serializer.data

print("Serialized blog post data:")
print(f"Title: {data['title']}")
print(f"Category: {data['category']['name']}")
print(f"Featured Image: {data['featured_image']}")
print(f"Author: {data['author']['full_name']}")