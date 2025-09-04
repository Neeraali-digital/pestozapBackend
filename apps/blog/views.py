"""
Views for the blog app.
"""
from rest_framework import generics, status, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Q, F
from .models import Category, Tag, BlogPost, Comment, BlogLike
from .serializers import (
    CategorySerializer,
    TagSerializer,
    BlogPostListSerializer,
    BlogPostDetailSerializer,
    BlogPostCreateSerializer,
    CommentSerializer,
    CommentCreateSerializer,
    BlogLikeSerializer
)
from .filters import BlogPostFilter


class CategoryListView(generics.ListAPIView):
    """
    List all active blog categories.
    """
    queryset = Category.objects.filter(is_active=True, is_deleted=False)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class TagListView(generics.ListAPIView):
    """
    List all blog tags.
    """
    queryset = Tag.objects.filter(is_deleted=False)
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]


class BlogPostListView(generics.ListAPIView):
    """
    List all published blog posts with filtering and search.
    """
    serializer_class = BlogPostListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BlogPostFilter
    search_fields = ['title', 'excerpt', 'content']
    ordering_fields = ['created_at', 'published_at', 'views_count', 'likes_count']
    ordering = ['-published_at']

    def get_queryset(self):
        """Get published blog posts."""
        return BlogPost.objects.filter(
            status='published',
            is_deleted=False
        ).select_related('author', 'category').prefetch_related('tags')


class BlogPostDetailView(generics.RetrieveAPIView):
    """
    Retrieve a single blog post by slug.
    """
    serializer_class = BlogPostDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

    def get_queryset(self):
        """Get published blog posts."""
        return BlogPost.objects.filter(
            status='published',
            is_deleted=False
        ).select_related('author', 'category').prefetch_related('tags')

    def retrieve(self, request, *args, **kwargs):
        """Retrieve blog post and increment view count."""
        instance = self.get_object()
        
        # Increment view count
        BlogPost.objects.filter(id=instance.id).update(
            views_count=F('views_count') + 1
        )
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class BlogPostCreateView(generics.CreateAPIView):
    """
    Create a new blog post (authenticated users only).
    """
    serializer_class = BlogPostCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class FeaturedBlogPostsView(generics.ListAPIView):
    """
    List featured blog posts.
    """
    serializer_class = BlogPostListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """Get featured published blog posts."""
        return BlogPost.objects.filter(
            status='published',
            is_featured=True,
            is_deleted=False
        ).select_related('author', 'category').prefetch_related('tags')[:6]


class RelatedBlogPostsView(generics.ListAPIView):
    """
    Get related blog posts based on category and tags.
    """
    serializer_class = BlogPostListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """Get related blog posts."""
        slug = self.kwargs.get('slug')
        try:
            current_post = BlogPost.objects.get(slug=slug, status='published', is_deleted=False)
        except BlogPost.DoesNotExist:
            return BlogPost.objects.none()

        # Get posts from same category or with similar tags
        related_posts = BlogPost.objects.filter(
            Q(category=current_post.category) | Q(tags__in=current_post.tags.all()),
            status='published',
            is_deleted=False
        ).exclude(id=current_post.id).distinct()

        return related_posts.select_related('author', 'category').prefetch_related('tags')[:4]


class BlogPostCommentsView(generics.ListCreateAPIView):
    """
    List and create comments for a blog post.
    """
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        """Return appropriate serializer based on request method."""
        if self.request.method == 'POST':
            return CommentCreateSerializer
        return CommentSerializer

    def get_queryset(self):
        """Get approved comments for the blog post."""
        slug = self.kwargs.get('slug')
        return Comment.objects.filter(
            post__slug=slug,
            post__status='published',
            is_approved=True,
            is_deleted=False,
            parent=None  # Only top-level comments
        ).select_related('author', 'post').prefetch_related('replies')

    def get_serializer_context(self):
        """Add post to serializer context."""
        context = super().get_serializer_context()
        slug = self.kwargs.get('slug')
        context['post'] = get_object_or_404(
            BlogPost,
            slug=slug,
            status='published',
            is_deleted=False
        )
        return context

    def create(self, request, *args, **kwargs):
        """Create a comment (authenticated users only)."""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required to post comments'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return super().create(request, *args, **kwargs)


@api_view(['POST', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def toggle_blog_like(request, slug):
    """
    Toggle like status for a blog post.
    """
    try:
        blog_post = BlogPost.objects.get(
            slug=slug,
            status='published',
            is_deleted=False
        )
    except BlogPost.DoesNotExist:
        return Response(
            {'error': 'Blog post not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    like, created = BlogLike.objects.get_or_create(
        post=blog_post,
        user=request.user
    )

    if not created:
        # Unlike the post
        like.delete()
        BlogPost.objects.filter(id=blog_post.id).update(
            likes_count=F('likes_count') - 1
        )
        return Response(
            {'message': 'Post unliked', 'is_liked': False},
            status=status.HTTP_200_OK
        )
    else:
        # Like the post
        BlogPost.objects.filter(id=blog_post.id).update(
            likes_count=F('likes_count') + 1
        )
        return Response(
            {'message': 'Post liked', 'is_liked': True},
            status=status.HTTP_201_CREATED
        )


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def blog_stats(request):
    """
    Get blog statistics.
    """
    stats = {
        'total_posts': BlogPost.objects.filter(status='published', is_deleted=False).count(),
        'total_categories': Category.objects.filter(is_active=True, is_deleted=False).count(),
        'total_tags': Tag.objects.filter(is_deleted=False).count(),
        'total_comments': Comment.objects.filter(is_approved=True, is_deleted=False).count(),
        'featured_posts': BlogPost.objects.filter(
            status='published',
            is_featured=True,
            is_deleted=False
        ).count(),
    }
    return Response(stats, status=status.HTTP_200_OK)