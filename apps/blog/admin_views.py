"""
Admin views for the blog app.
"""
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils import timezone
from .models import BlogPost, Category, Tag
from reviews.models import Review
from enquiries.models import Enquiry
from offers.models import Offer
from .serializers import (
    BlogPostDetailSerializer,
    BlogPostCreateSerializer,
    CategorySerializer,
    TagSerializer
)
import os

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
class AdminBlogPostListView(generics.ListCreateAPIView):
    """Admin view for listing and creating blog posts."""
    serializer_class = BlogPostDetailSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'category', 'is_featured']
    
    def get_queryset(self):
        return BlogPost.objects.filter(is_deleted=False).select_related(
            'author', 'category'
        ).prefetch_related('tags')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BlogPostCreateSerializer
        return BlogPostDetailSerializer
    
    def perform_create(self, serializer):
        """Set author and published_at when creating."""
        from django.utils import timezone
        blog_post = serializer.save(author=self.request.user)
        if blog_post.status == 'published' and not blog_post.published_at:
            blog_post.published_at = timezone.now()
            blog_post.save()


class AdminBlogPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin view for blog post detail operations."""
    serializer_class = BlogPostDetailSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        return BlogPost.objects.filter(is_deleted=False)





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

    enquiries = Enquiry.objects.all().order_by('-created_at')

    # Filter by type
    type_filter = request.GET.get('type')
    if type_filter:
        enquiries = enquiries.filter(type=type_filter)

    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        enquiries = enquiries.filter(status=status_filter)

    # Filter by service_type
    service_filter = request.GET.get('service_type')
    if service_filter:
        enquiries = enquiries.filter(service_type=service_filter)

    # Search
    search = request.GET.get('search')
    if search:
        enquiries = enquiries.filter(
            Q(customer_name__icontains=search) |
            Q(email__icontains=search) |
            Q(subject__icontains=search)
        )

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(enquiries, 20)
    page_obj = paginator.get_page(page)

    enquiry_data = []
    for enquiry in page_obj:
        enquiry_data.append({
            'id': enquiry.id,
            'type': enquiry.type,
            'name': enquiry.customer_name,
            'email': enquiry.email,
            'phone': enquiry.phone,
            'subject': enquiry.subject,
            'service_type': enquiry.service_type,
            'property_type': enquiry.property_type,
            'pest_types': enquiry.pests,
            'address': enquiry.address,
            'message': enquiry.message,
            'status': enquiry.status,
            'priority': enquiry.priority,
            'created_at': enquiry.created_at,
            'updated_at': enquiry.updated_at,
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


# Additional Blog Post Views
class AdminBlogPostUpdateView(generics.UpdateAPIView):
    """Admin view for updating blog posts."""
    serializer_class = BlogPostDetailSerializer
    permission_classes = [IsAdminUser]
    queryset = BlogPost.objects.filter(is_deleted=False)
    
    def perform_update(self, serializer):
        """Set published_at when status changes to published."""
        from django.utils import timezone
        instance = serializer.instance
        old_status = instance.status
        blog_post = serializer.save()
        
        if blog_post.status == 'published' and old_status != 'published' and not blog_post.published_at:
            blog_post.published_at = timezone.now()
            blog_post.save()


class AdminBlogPostDeleteView(generics.DestroyAPIView):
    """Admin view for deleting blog posts."""
    permission_classes = [IsAdminUser]
    queryset = BlogPost.objects.filter(is_deleted=False)


# Category and Tag Admin Views
class AdminCategoryListView(generics.ListCreateAPIView):
    """Admin view for managing categories."""
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]
    queryset = Category.objects.filter(is_active=True)


class AdminCategoryCreateView(generics.CreateAPIView):
    """Admin view for creating categories."""
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]


class AdminTagListView(generics.ListCreateAPIView):
    """Admin view for managing tags."""
    serializer_class = TagSerializer
    permission_classes = [IsAdminUser]
    queryset = Tag.objects.all()


class AdminTagCreateView(generics.CreateAPIView):
    """Admin view for creating tags."""
    serializer_class = TagSerializer
    permission_classes = [IsAdminUser]


# Enhanced User Management Views
@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_user_detail(request, user_id):
    """Get detailed user information."""
    try:
        user = User.objects.get(id=user_id)
        user_data = {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone_number': user.phone_number,
            'address': user.address,
            'date_of_birth': user.date_of_birth,
            'profile_picture': user.profile_picture.url if user.profile_picture else None,
            'is_verified': user.is_verified,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'date_joined': user.date_joined,
            'last_login': user.last_login,
        }
        return Response(user_data)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def admin_user_update(request, user_id):
    """Update user information."""
    try:
        user = User.objects.get(id=user_id)
        data = request.data

        # Update user fields
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        user.phone_number = data.get('phone_number', user.phone_number)
        user.address = data.get('address', user.address)
        user.is_active = data.get('is_active', user.is_active)
        user.is_verified = data.get('is_verified', user.is_verified)

        user.save()

        return Response({'message': 'User updated successfully'})
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def admin_user_delete(request, user_id):
    """Delete user (soft delete by deactivating)."""
    try:
        user = User.objects.get(id=user_id)
        user.is_active = False
        user.save()
        return Response({'message': 'User deactivated successfully'})
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


# Enhanced Review Management Views
@api_view(['PUT'])
@permission_classes([IsAdminUser])
def admin_review_update(request, review_id):
    """Update review."""
    try:
        review = Review.objects.get(id=review_id, is_deleted=False)
        data = request.data

        review.title = data.get('title', review.title)
        review.content = data.get('content', review.content)
        review.rating = data.get('rating', review.rating)
        review.is_approved = data.get('is_approved', review.is_approved)
        review.is_featured = data.get('is_featured', review.is_featured)

        review.save()

        return Response({'message': 'Review updated successfully'})
    except Review.DoesNotExist:
        return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def admin_review_delete(request, review_id):
    """Delete review (soft delete)."""
    try:
        review = Review.objects.get(id=review_id, is_deleted=False)
        review.is_deleted = True
        review.save()
        return Response({'message': 'Review deleted successfully'})
    except Review.DoesNotExist:
        return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_review_approve(request, review_id):
    """Approve or reject review."""
    try:
        review = Review.objects.get(id=review_id, is_deleted=False)
        is_approved = request.data.get('is_approved', True)
        review.is_approved = is_approved
        review.save()
        return Response({'message': f'Review {"approved" if is_approved else "rejected"} successfully'})
    except Review.DoesNotExist:
        return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)


# Enhanced Enquiry Management Views
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def admin_enquiry_detail(request, enquiry_id):
    """Update or delete enquiry."""
    try:
        enquiry = Enquiry.objects.get(id=enquiry_id)

        if request.method == 'PUT':
            data = request.data
            enquiry.customer_name = data.get('name', enquiry.customer_name)
            enquiry.email = data.get('email', enquiry.email)
            enquiry.phone = data.get('phone', enquiry.phone)
            enquiry.service_type = data.get('service_type', enquiry.service_type)
            enquiry.property_type = data.get('property_type', enquiry.property_type)
            enquiry.pests = data.get('pest_types', enquiry.pests)
            enquiry.address = data.get('address', enquiry.address)
            enquiry.message = data.get('message', enquiry.message)
            enquiry.status = data.get('status', enquiry.status)
            enquiry.priority = data.get('priority', enquiry.priority)
            enquiry.save()
            # Return the updated enquiry object
            updated_data = {
                'id': enquiry.id,
                'type': enquiry.type,
                'name': enquiry.customer_name,
                'email': enquiry.email,
                'phone': enquiry.phone,
                'subject': enquiry.subject,
                'service_type': enquiry.service_type,
                'property_type': enquiry.property_type,
                'pest_types': enquiry.pests,
                'address': enquiry.address,
                'message': enquiry.message,
                'status': enquiry.status,
                'priority': enquiry.priority,
                'created_at': enquiry.created_at,
                'updated_at': enquiry.updated_at,
            }
            return Response(updated_data)

        elif request.method == 'DELETE':
            enquiry.delete()
            return Response({'message': 'Enquiry deleted successfully'})

    except Enquiry.DoesNotExist:
        return Response({'error': 'Enquiry not found'}, status=status.HTTP_404_NOT_FOUND)


# Enhanced Offer Management Views
@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_offer_detail(request, offer_id):
    """Get offer details."""
    try:
        offer = Offer.objects.get(id=offer_id, is_deleted=False)
        offer_data = {
            'id': offer.id,
            'title': offer.title,
            'description': offer.description,
            'discount_percentage': offer.discount_percentage,
            'discount_amount': offer.discount_amount,
            'code': offer.code,
            'image': offer.image.url if offer.image else None,
            'valid_from': offer.valid_from,
            'valid_until': offer.valid_until,
            'is_active': offer.is_active,
            'usage_limit': offer.usage_limit,
            'used_count': offer.used_count,
            'terms_conditions': offer.terms_conditions,
            'created_at': offer.created_at,
        }
        return Response(offer_data)
    except Offer.DoesNotExist:
        return Response({'error': 'Offer not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def admin_offer_update(request, offer_id):
    """Update offer."""
    try:
        offer = Offer.objects.get(id=offer_id, is_deleted=False)
        data = request.data

        offer.title = data.get('title', offer.title)
        offer.description = data.get('description', offer.description)
        offer.discount_percentage = data.get('discount_percentage', offer.discount_percentage)
        offer.discount_amount = data.get('discount_amount', offer.discount_amount)
        offer.code = data.get('code', offer.code)
        offer.valid_from = data.get('valid_from', offer.valid_from)
        offer.valid_until = data.get('valid_until', offer.valid_until)
        offer.is_active = data.get('is_active', offer.is_active)
        offer.usage_limit = data.get('usage_limit', offer.usage_limit)
        offer.terms_conditions = data.get('terms_conditions', offer.terms_conditions)

        if 'image' in request.FILES:
            offer.image = request.FILES['image']

        offer.save()

        return Response({'message': 'Offer updated successfully'})
    except Offer.DoesNotExist:
        return Response({'error': 'Offer not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def admin_offer_delete(request, offer_id):
    """Delete offer (soft delete)."""
    try:
        offer = Offer.objects.get(id=offer_id, is_deleted=False)
        offer.is_deleted = True
        offer.save()
        return Response({'message': 'Offer deleted successfully'})
    except Offer.DoesNotExist:
        return Response({'error': 'Offer not found'}, status=status.HTTP_404_NOT_FOUND)


# File Upload View
@api_view(['POST'])
@permission_classes([IsAdminUser])
def upload_file(request):
    """Upload file for admin use."""
    parser_classes = [MultiPartParser, FormParser]

    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

    file_obj = request.FILES['file']
    file_type = request.data.get('type', 'general')

    # Generate unique filename
    file_extension = os.path.splitext(file_obj.name)[1]
    timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
    filename = f'{file_type}_{timestamp}{file_extension}'

    # Save file to media directory
    file_path = f'uploads/admin/{file_type}/{filename}'
    file_name = default_storage.save(file_path, ContentFile(file_obj.read()))

    # Return file URL
    file_url = default_storage.url(file_name)

    return Response({
        'url': file_url,
        'filename': filename,
        'message': 'File uploaded successfully'
    }, status=status.HTTP_201_CREATED)
