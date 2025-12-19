#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pestozap_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.blog.models import BlogPost, Category
from apps.blog.serializers import BlogPostCreateSerializer

User = get_user_model()

# Get or create admin user
admin_user = User.objects.filter(is_staff=True).first()
if not admin_user:
    admin_user = User.objects.create_superuser(
        email='admin@test.com',
        password='admin123',
        first_name='Admin',
        last_name='User'
    )

# Test data
test_data = {
    'title': 'Test Blog Post',
    'excerpt': 'This is a test excerpt',
    'content': 'This is test content',
    'category': 1,
    'status': 'published',
    'is_featured': False,
    'read_time': 5
}

# Test serializer
serializer = BlogPostCreateSerializer(data=test_data, context={'request': type('obj', (object,), {'user': admin_user})()})
if serializer.is_valid():
    blog_post = serializer.save(author=admin_user)
    print(f"Blog post created successfully: {blog_post.title}")
else:
    print(f"Serializer errors: {serializer.errors}")