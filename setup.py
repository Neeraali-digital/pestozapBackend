#!/usr/bin/env python
"""
Setup script for Pestozap Backend.
Run this script to set up the development environment.
"""

import os
import sys
import subprocess
import django
from django.core.management import execute_from_command_line

def run_command(command):
    """Run a shell command."""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print(f"Success: {result.stdout}")
    return True

def setup_environment():
    """Set up the Django environment."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pestozap_backend.settings')
    django.setup()

def create_sample_data():
    """Create sample blog data."""
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
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults=cat_data
        )
        if created:
            print(f"Created category: {category.name}")
    
    # Create tags
    tags_data = [
        'pest-control', 'prevention', 'eco-friendly', 'home', 'commercial',
        'termites', 'cockroaches', 'rodents', 'ants', 'mosquitoes',
        'bed-bugs', 'seasonal', 'diy', 'professional', 'safety'
    ]
    
    for tag_name in tags_data:
        tag, created = Tag.objects.get_or_create(name=tag_name)
        if created:
            print(f"Created tag: {tag.name}")
    
    print("Sample data created successfully!")

def main():
    """Main setup function."""
    print("🚀 Setting up Pestozap Backend...")
    
    # Check if virtual environment is activated
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: Virtual environment not detected. Consider activating a virtual environment.")
    
    # Install requirements
    print("\n📦 Installing requirements...")
    if not run_command("pip install -r requirements.txt"):
        print("❌ Failed to install requirements")
        return
    
    # Set up Django environment
    setup_environment()
    
    # Run migrations
    print("\n🗄️  Running migrations...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Create sample data
    print("\n📝 Creating sample data...")
    create_sample_data()
    
    # Collect static files
    print("\n📁 Collecting static files...")
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
    
    print("\n✅ Setup completed successfully!")
    print("\n🎯 Next steps:")
    print("1. Create a superuser: python manage.py createsuperuser")
    print("2. Start the development server: python manage.py runserver")
    print("3. Access the admin interface: http://localhost:8000/admin/")
    print("4. API documentation: http://localhost:8000/api/v1/")

if __name__ == '__main__':
    main()