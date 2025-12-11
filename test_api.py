#!/usr/bin/env python
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pestozap_backend.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

# Get admin user
admin_user = User.objects.filter(is_staff=True).first()
if not admin_user:
    print("No admin user found")
    exit()

# Create test client
client = Client()
client.force_login(admin_user)

# Test data
test_data = {
    'title': 'API Test Blog Post',
    'excerpt': 'This is a test excerpt from API',
    'content': 'This is test content from API',
    'category': 1,
    'status': 'published',
    'is_featured': False,
    'read_time': 5
}

# Test POST request
response = client.post(
    '/api/v1/admin/blog/posts/',
    data=json.dumps(test_data),
    content_type='application/json'
)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.content.decode()}")

if response.status_code == 400:
    print("Validation errors found")
elif response.status_code == 201:
    print("Blog post created successfully via API")