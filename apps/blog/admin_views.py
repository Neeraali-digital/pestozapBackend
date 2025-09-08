"""
Admin views for the blog app.
"""
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from django.contrib.auth import get_user_model
from .models import BlogPost, Category, Tag, Review, Enquiry, Offer
from .serializers import (
    BlogPostDetailSerializer,
    BlogPostCreateSerializer,
    CategorySerializer,
    TagSerializer
)

User = get_user_model()


class IsAdminUser(permissions.BasePermission):
    """Custom permission to only allow admin users."""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            request.user.is_staff or request.user.is_superuser
        )


# Dashboard Stats
@api_view(['GET'])
@permission_classes([IsAdminUser])
def dashboard_stats(request):
    """Get dashboard statistics."""
    stats = {
        'total_users': User.objects.count(),
        'total_posts': BlogPost.objects.filter(is_deleted=False).count(),
        'total_enquiries': Enquiry.objects.filter(is_deleted=False).count(),
        'total_reviews': Review.objects.filter(is_deleted=False).count(),
        'total_offers': Offer.objects.filter(is_deleted=False).count(),
        'recent_users': User.objects.filter(date_joined__gte='2024-01-01').count(),
        'recent_posts': BlogPost.objects.filter(
            created_at__gte='2024-01-01',
            is_deleted=False
        ).count(),
        'recent_enquiries': Enquiry.objects.filter(
            created_at__gte='2024-01-01',
            is_deleted=False
        ).count(),
    }
    return Response(stats)


# Blog Post Admin Views
class AdminBlogPostListView(generics.ListAPIView):
    """Admin view for listing all blog posts."""
    serializer_class = BlogPostDetailSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'category', 'is_featured']
    
    def get_queryset(self):
        return BlogPost.objects.filter(is_deleted=False).select_related(
            'author', 'category'
        ).prefetch_related('tags')


class AdminBlogPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin view for blog post detail operations."""
    serializer_class = BlogPostDetailSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        return BlogPost.objects.filter(is_deleted=False)


class AdminBlogPostCreateView(generics.CreateAPIView):
    """Admin view for creating blog posts."""
    serializer_class = BlogPostCreateSerializer
    permission_classes = [IsAdminUser]


# User Management Views
@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_users_list(request):
    """Get paginated list of users."""
    from django.core.paginator import Paginator
    
    users = User.objects.all().order_by('-date_joined')
    
    # Search
    search = request.GET.get('search')
    if search:
        users = users.filter(
            Q(email__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(users, 20)
    page_obj = paginator.get_page(page)
    
    user_data = []
    for user in page_obj:
        user_data.append({
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_active': user.is_active,
            'is_verified': user.is_verified,
            'date_joined': user.date_joined,
            'last_login': user.last_login,
        })
    
    return Response({
        'results': user_data,
        'count': paginator.count,
        'num_pages': paginator.num_pages,
        'current_page': page_obj.number,
    })


# Review Management
@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_reviews_list(request):
    """Get paginated list of reviews."""
    from django.core.paginator import Paginator
    
    reviews = Review.objects.filter(is_deleted=False).select_related('user').order_by('-created_at')
    
    # Filter by approval status
    is_approved = request.GET.get('is_approved')
    if is_approved is not None:
        reviews = reviews.filter(is_approved=is_approved.lower() == 'true')
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(reviews, 20)
    page_obj = paginator.get_page(page)
    
    review_data = []
    for review in page_obj:
        review_data.append({
            'id': review.id,
            'user': {
                'id': review.user.id,
                'full_name': review.user.full_name,
                'email': review.user.email,
            },
            'rating': review.rating,
            'title': review.title,
            'content': review.content,
            'service_type': review.service_type,
            'is_approved': review.is_approved,
            'is_featured': review.is_featured,
            'created_at': review.created_at,
        })
    
    return Response({
        'results': review_data,
        'count': paginator.count,
    })


# Enquiry Management
@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_enquiries_list(request):
    """Get paginated list of enquiries."""
    from django.core.paginator import Paginator
    
    enquiries = Enquiry.objects.filter(is_deleted=False).order_by('-created_at')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        enquiries = enquiries.filter(status=status_filter)
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(enquiries, 20)
    page_obj = paginator.get_page(page)
    
    enquiry_data = []
    for enquiry in page_obj:
        enquiry_data.append({
            'id': enquiry.id,
            'name': enquiry.name,
            'email': enquiry.email,
            'phone': enquiry.phone,
            'service_type': enquiry.service_type,
            'property_type': enquiry.property_type,
            'pest_types': enquiry.pest_types,
            'address': enquiry.address,
            'message': enquiry.message,
            'status': enquiry.status,
            'priority': enquiry.priority,
            'created_at': enquiry.created_at,
        })
    
    return Response({
        'results': enquiry_data,
        'count': paginator.count,
    })


# Offer Management
@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_offers_list(request):
    """Get paginated list of offers."""
    from django.core.paginator import Paginator
    
    offers = Offer.objects.filter(is_deleted=False).order_by('-created_at')
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(offers, 20)
    page_obj = paginator.get_page(page)
    
    offer_data = []
    for offer in page_obj:
        offer_data.append({
            'id': offer.id,
            'title': offer.title,
            'description': offer.description,
            'discount_percentage': offer.discount_percentage,
            'code': offer.code,
            'image': offer.image.url if offer.image else None,
            'valid_from': offer.valid_from,
            'valid_until': offer.valid_until,
            'is_active': offer.is_active,
            'usage_limit': offer.usage_limit,
            'used_count': offer.used_count,
            'created_at': offer.created_at,
        })
    
    return Response({
        'results': offer_data,
        'count': paginator.count,
    })


@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_offer(request):
    """Create a new offer."""
    data = request.data
    
    offer = Offer.objects.create(
        title=data.get('title'),
        description=data.get('description'),
        discount_percentage=data.get('discount_percentage'),
        discount_amount=data.get('discount_amount'),
        code=data.get('code'),
        valid_from=data.get('valid_from'),
        valid_until=data.get('valid_until'),
        is_active=data.get('is_active', True),
        usage_limit=data.get('usage_limit'),
        terms_conditions=data.get('terms_conditions', ''),
    )
    
    if 'image' in request.FILES:
        offer.image = request.FILES['image']
        offer.save()
    
    return Response({
        'id': offer.id,
        'title': offer.title,
        'message': 'Offer created successfully'
    }, status=status.HTTP_201_CREATED)