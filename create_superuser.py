#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pestozap_backend.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(email='admin@pestozap.com').exists():
    User.objects.create_superuser(
        email='admin@pestozap.com',
        password='admin123',
        first_name='Admin',
        last_name='User'
    )
    print("Superuser created successfully!")
else:
    print("Superuser already exists!")