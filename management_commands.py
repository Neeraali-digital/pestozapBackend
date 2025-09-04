"""
Custom Django management commands for Pestozap backend.
Run these commands to set up initial data and perform maintenance tasks.
"""

# Create sample blog data
"""
python manage.py shell

from django.contrib.auth import get_user_model
from apps.blog.models import Category, Tag, BlogPost
from django.utils import timezone

User = get_user_model()

# Create categories
categories_data = [
    {'name': 'Prevention', 'description': 'Pest prevention tips and techniques', 'color': '#10B981', 'icon': 'shield'},
    {'name': 'Eco-Friendly', 'description': 'Environmentally safe pest control methods', 'color': '#059669', 'icon': 'eco'},
    {'name': 'Seasonal', 'description': 'Seasonal pest control advice', 'color': '#F59E0B', 'icon': 'calendar_today'},
    {'name': 'Commercial', 'description': 'Business pest control solutions', 'color': '#3B82F6', 'icon': 'business'},
    {'name': 'Tips', 'description': 'General pest control tips', 'color': '#8B5CF6', 'icon': 'lightbulb'},
    {'name': 'Termites', 'description': 'Termite control and prevention', 'color': '#EF4444', 'icon': 'bug_report'},
]

for cat_data in categories_data:
    Category.objects.get_or_create(
        name=cat_data['name'],
        defaults=cat_data
    )

# Create tags
tags_data = [
    'pest-control', 'prevention', 'eco-friendly', 'home', 'commercial',
    'termites', 'cockroaches', 'rodents', 'ants', 'mosquitoes',
    'bed-bugs', 'seasonal', 'diy', 'professional', 'safety'
]

for tag_name in tags_data:
    Tag.objects.get_or_create(name=tag_name)

print("Sample data created successfully!")
"""

# Create superuser command
"""
python manage.py createsuperuser --email admin@pestozap.com --username admin
"""

# Run migrations
"""
python manage.py makemigrations
python manage.py migrate
"""

# Collect static files
"""
python manage.py collectstatic --noinput
"""