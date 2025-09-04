"""
Blog app configuration.
"""
from django.apps import AppConfig


class BlogConfig(AppConfig):
    """Configuration for the blog app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.blog'