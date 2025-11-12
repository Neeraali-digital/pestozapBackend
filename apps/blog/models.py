"""
Blog models for the Pestozap application.
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from apps.common.models import BaseModel

User = get_user_model()


class Category(BaseModel):
    """
    Blog category model.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#cc1f4a')  # Hex color
    icon = models.CharField(max_length=50, blank=True)  # Material icon name
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'blog_categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Auto-generate slug from name."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(BaseModel):
    """
    Blog tag model.
    """
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    
    class Meta:
        db_table = 'blog_tags'
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Auto-generate slug from name."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogPost(BaseModel):
    """
    Blog post model.
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    excerpt = models.TextField(max_length=300, help_text="Brief description of the post")
    content = models.TextField()
    featured_image = models.ImageField(
        upload_to='blog/images/',
        blank=True,
        null=True,
        help_text="Main image for the blog post"
    )
    
    # Relationships
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts'
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    
    # Status and metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    read_time = models.PositiveIntegerField(
        default=5,
        help_text="Estimated read time in minutes"
    )
    views_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    
    # SEO fields
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    
    # Publishing
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'blog_posts'
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'published_at']),
            models.Index(fields=['category', 'status']),
            models.Index(fields=['is_featured', 'status']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Auto-generate slug from title."""
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Auto-generate meta fields if not provided
        if not self.meta_title:
            self.meta_title = self.title[:60]
        if not self.meta_description:
            self.meta_description = self.excerpt[:160]
            
        super().save(*args, **kwargs)

    @property
    def is_published(self):
        """Check if the post is published."""
        return self.status == 'published' and not self.is_deleted


class Comment(BaseModel):
    """
    Blog comment model.
    """
    post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_comments'
    )
    content = models.TextField(max_length=1000)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    is_approved = models.BooleanField(default=True)

    class Meta:
        db_table = 'blog_comments'
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.author.full_name} on {self.post.title}"


class BlogLike(models.Model):
    """
    Blog post like model.
    """
    post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'blog_likes'
        unique_together = ['post', 'user']
        verbose_name = 'Blog Like'
        verbose_name_plural = 'Blog Likes'

    def __str__(self):
        return f"{self.user.full_name} likes {self.post.title}"


