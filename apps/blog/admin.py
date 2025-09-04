"""
Admin configuration for the blog app.
"""
from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Category, Tag, BlogPost, Comment, BlogLike


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Category model.
    """
    list_display = ('name', 'slug', 'color_display', 'icon', 'is_active', 'posts_count')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')

    def color_display(self, obj):
        """Display color as a colored box."""
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border: 1px solid #ccc;"></div>',
            obj.color
        )
    color_display.short_description = 'Color'

    def posts_count(self, obj):
        """Display the number of posts in this category."""
        return obj.posts.filter(status='published', is_deleted=False).count()
    posts_count.short_description = 'Posts Count'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Tag model.
    """
    list_display = ('name', 'slug', 'posts_count', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')

    def posts_count(self, obj):
        """Display the number of posts with this tag."""
        return obj.posts.filter(status='published', is_deleted=False).count()
    posts_count.short_description = 'Posts Count'


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    """
    Admin configuration for the BlogPost model.
    """
    list_display = (
        'title', 'author', 'category', 'status', 'is_featured',
        'views_count', 'likes_count', 'published_at'
    )
    list_filter = (
        'status', 'is_featured', 'category', 'created_at',
        'published_at', 'author'
    )
    search_fields = ('title', 'excerpt', 'content')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    readonly_fields = ('views_count', 'likes_count', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'excerpt', 'content', 'featured_image')
        }),
        ('Classification', {
            'fields': ('author', 'category', 'tags')
        }),
        ('Publishing', {
            'fields': ('status', 'is_featured', 'published_at')
        }),
        ('Metadata', {
            'fields': ('read_time', 'meta_title', 'meta_description')
        }),
        ('Statistics', {
            'fields': ('views_count', 'likes_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """Set published_at when status changes to published."""
        if obj.status == 'published' and not obj.published_at:
            obj.published_at = timezone.now()
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('author', 'category')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Comment model.
    """
    list_display = (
        'author', 'post', 'content_preview', 'is_approved',
        'parent', 'created_at'
    )
    list_filter = ('is_approved', 'created_at', 'post__category')
    search_fields = ('content', 'author__username', 'post__title')
    readonly_fields = ('created_at', 'updated_at')
    
    def content_preview(self, obj):
        """Display a preview of the comment content."""
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('author', 'post', 'parent')


@admin.register(BlogLike)
class BlogLikeAdmin(admin.ModelAdmin):
    """
    Admin configuration for the BlogLike model.
    """
    list_display = ('user', 'post', 'created_at')
    list_filter = ('created_at', 'post__category')
    search_fields = ('user__username', 'post__title')
    readonly_fields = ('created_at',)

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('user', 'post')