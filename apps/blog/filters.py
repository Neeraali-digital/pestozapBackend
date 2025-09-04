"""
Filters for the blog app.
"""
import django_filters
from .models import BlogPost, Category, Tag


class BlogPostFilter(django_filters.FilterSet):
    """
    Filter for blog posts.
    """
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.filter(is_active=True, is_deleted=False)
    )
    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.filter(is_deleted=False),
        conjoined=False  # OR logic for multiple tags
    )
    is_featured = django_filters.BooleanFilter()
    date_from = django_filters.DateFilter(field_name='published_at', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='published_at', lookup_expr='lte')
    author = django_filters.CharFilter(field_name='author__username', lookup_expr='icontains')

    class Meta:
        model = BlogPost
        fields = ['category', 'tags', 'is_featured', 'author']