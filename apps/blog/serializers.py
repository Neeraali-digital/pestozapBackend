"""
Serializers for the blog app.
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Category, Tag, BlogPost, Comment, BlogLike

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for blog categories.
    """
    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            'id', 'name', 'slug', 'description', 'color',
            'icon', 'is_active', 'posts_count'
        )

    def get_posts_count(self, obj):
        """Get the number of published posts in this category."""
        return obj.posts.filter(status='published', is_deleted=False).count()


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for blog tags.
    """
    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for blog post authors.
    """
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'full_name', 'profile_picture')


class BlogPostListSerializer(serializers.ModelSerializer):
    """
    Serializer for blog post list view.
    """
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = (
            'id', 'title', 'slug', 'excerpt', 'featured_image',
            'author', 'category', 'tags', 'status', 'is_featured',
            'read_time', 'views_count', 'likes_count', 'comments_count',
            'published_at', 'created_at'
        )

    def get_comments_count(self, obj):
        """Get the number of approved comments."""
        return obj.comments.filter(is_approved=True, is_deleted=False).count()


class BlogPostDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for blog post detail view.
    """
    author = AuthorSerializer(read_only=True)
    category_detail = CategorySerializer(source='category', read_only=True)
    category = serializers.IntegerField(required=False, write_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = (
            'id', 'title', 'slug', 'excerpt', 'content', 'featured_image',
            'author', 'category', 'category_detail', 'tags', 'status', 'is_featured',
            'read_time', 'views_count', 'likes_count', 'comments_count',
            'meta_title', 'meta_description', 'published_at', 'created_at',
            'updated_at', 'is_liked'
        )

    def get_comments_count(self, obj):
        """Get the number of approved comments."""
        return obj.comments.filter(is_approved=True, is_deleted=False).count()

    def get_is_liked(self, obj):
        """Check if the current user has liked this post."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return BlogLike.objects.filter(post=obj, user=request.user).exists()
        return False
    
    def update(self, instance, validated_data):
        """Update blog post and set published_at if status changes to published."""
        from django.utils import timezone
        old_status = instance.status
        
        # Handle category update
        if 'category' in validated_data:
            category_id = validated_data.pop('category')
            category_map = {
                1: 'Tips & Tricks',
                2: 'Prevention',
                3: 'Eco-Friendly',
                4: 'Home Care',
                5: 'Commercial',
                6: 'Seasonal'
            }
            category_name = category_map.get(category_id, 'Tips & Tricks')
            category, _ = Category.objects.get_or_create(
                name=category_name,
                defaults={'is_active': True}
            )
            instance.category = category
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Set published_at when status changes to published
        if instance.status == 'published' and old_status != 'published' and not instance.published_at:
            instance.published_at = timezone.now()
        
        instance.save()
        return instance


class BlogPostCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating blog posts.
    """
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        required=False
    )
    category = serializers.IntegerField(required=True, write_only=True)
    featured_image_url = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = BlogPost
        fields = (
            'title', 'excerpt', 'content', 'featured_image',
            'category', 'tags', 'status', 'is_featured',
            'read_time', 'meta_title', 'meta_description', 'featured_image_url'
        )

    def create(self, validated_data):
        """Create a new blog post."""
        from django.utils import timezone
        from django.core.files.base import ContentFile
        import requests
        import os
        
        tags = validated_data.pop('tags', [])
        category_id = validated_data.pop('category')
        featured_image_url = validated_data.pop('featured_image_url', None)
        
        # Map category IDs to names and create if not exists
        category_map = {
            1: 'Tips & Tricks',
            2: 'Prevention',
            3: 'Eco-Friendly',
            4: 'Home Care',
            5: 'Commercial',
            6: 'Seasonal'
        }
        
        category_name = category_map.get(category_id, 'Tips & Tricks')
        category, _ = Category.objects.get_or_create(
            name=category_name,
            defaults={'is_active': True}
        )
        validated_data['category'] = category
        
        # Handle featured image URL
        if featured_image_url and featured_image_url.startswith('/media/'):
            # Convert URL to file path and set the image
            from django.conf import settings
            file_path = featured_image_url.replace('/media/', '')
            validated_data['featured_image'] = file_path
        
        # Set published_at if status is published
        if validated_data.get('status') == 'published' and 'published_at' not in validated_data:
            validated_data['published_at'] = timezone.now()
        
        blog_post = BlogPost.objects.create(**validated_data)
        blog_post.tags.set(tags)
        
        return blog_post


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for blog comments.
    """
    author = AuthorSerializer(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            'id', 'content', 'author', 'parent', 'is_approved',
            'created_at', 'replies'
        )

    def get_replies(self, obj):
        """Get replies to this comment."""
        if obj.replies.exists():
            return CommentSerializer(
                obj.replies.filter(is_approved=True, is_deleted=False),
                many=True,
                context=self.context
            ).data
        return []


class CommentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating comments.
    """
    class Meta:
        model = Comment
        fields = ('content', 'parent')

    def create(self, validated_data):
        """Create a new comment."""
        validated_data['author'] = self.context['request'].user
        validated_data['post'] = self.context['post']
        return Comment.objects.create(**validated_data)


class BlogLikeSerializer(serializers.ModelSerializer):
    """
    Serializer for blog likes.
    """
    class Meta:
        model = BlogLike
        fields = ('id', 'created_at')