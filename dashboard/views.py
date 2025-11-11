from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Sum, Avg
from django.utils import timezone
from datetime import timedelta
from apps.blog.models import Enquiry, Offer, Review, BlogPost
from apps.users.models import User

class IsAdminUser:
    """Custom permission to only allow admin users."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            request.user.is_staff or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def dashboard_stats(request):
    from django.db.models import Count, Sum, Avg
    from django.utils import timezone
    from datetime import timedelta
    import calendar

    # Basic stats
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    total_enquiries = Enquiry.objects.filter(is_deleted=False).count()
    new_enquiries = Enquiry.objects.filter(status='new', is_deleted=False).count()
    total_reviews = Review.objects.filter(is_deleted=False).count()
    approved_reviews = Review.objects.filter(is_approved=True, is_deleted=False).count()
    total_offers = Offer.objects.filter(is_deleted=False).count()
    active_offers = Offer.objects.filter(is_active=True, is_deleted=False).count()
    total_posts = BlogPost.objects.filter(is_deleted=False).count()
    published_posts = BlogPost.objects.filter(status='published', is_deleted=False).count()

    # Revenue calculation (using offer usage as proxy for revenue)
    # In a real app, this would come from actual transaction data
    total_revenue = active_offers * 1000  # Mock calculation
    revenue_change = 12.5  # This would be calculated from historical data

    # Customer satisfaction from approved reviews
    avg_rating = Review.objects.filter(is_approved=True, is_deleted=False).aggregate(
        avg_rating=Avg('rating')
    )['avg_rating'] or 0
    customer_satisfaction = round(avg_rating * 20, 1)  # Convert 5-star to percentage

    # Recent activities (last 10 activities)
    activities = []

    # Recent enquiries
    recent_enquiries = Enquiry.objects.filter(is_deleted=False).order_by('-created_at')[:3]
    for enquiry in recent_enquiries:
        activities.append({
            'action': f'New service request from {enquiry.name}',
            'time': enquiry.created_at.strftime('%Y-%m-%d %H:%M'),
            'type': 'request'
        })

    # Recent reviews
    recent_reviews = Review.objects.filter(is_deleted=False).order_by('-created_at')[:3]
    for review in recent_reviews:
        activities.append({
            'action': f'New review from {review.user.get_full_name() if review.user.get_full_name() else review.user.username}',
            'time': review.created_at.strftime('%Y-%m-%d %H:%M'),
            'type': 'review'
        })

    # Recent users
    recent_users = User.objects.order_by('-date_joined')[:2]
    for user in recent_users:
        activities.append({
            'action': f'New user registration: {user.get_full_name() if user.get_full_name() else user.username}',
            'time': user.date_joined.strftime('%Y-%m-%d %H:%M'),
            'type': 'user'
        })

    # Sort activities by time
    activities.sort(key=lambda x: x['time'], reverse=True)
    activities = activities[:5]

    # Chart data - Revenue over last 6 months
    now = timezone.now()
    revenue_labels = []
    revenue_data = []

    for i in range(5, -1, -1):
        month_date = now - timedelta(days=30*i)
        month_name = calendar.month_abbr[month_date.month]
        year = month_date.year
        label = f"{month_name} {year}"

        # Count enquiries in this month as proxy for revenue
        month_start = month_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if i == 0:
            month_end = now
        else:
            next_month = month_date.replace(day=28, hour=23, minute=59, second=59, microsecond=999999) + timedelta(days=4)
            month_end = next_month.replace(day=1) - timedelta(days=1)

        month_enquiries = Enquiry.objects.filter(
            created_at__gte=month_start,
            created_at__lte=month_end,
            is_deleted=False
        ).count()

        revenue_labels.append(label)
        revenue_data.append(month_enquiries * 500)  # Mock revenue calculation

    # Services distribution
    service_counts = Enquiry.objects.filter(is_deleted=False).values('service_type').annotate(
        count=Count('service_type')
    ).order_by('-count')[:4]

    services_labels = []
    services_data = []

    for service in service_counts:
        services_labels.append(service['service_type'].title())
        services_data.append(service['count'])

    # Fill with defaults if not enough data
    default_services = ['Pest Control', 'Termite', 'Rodent', 'Inspection']
    default_data = [45, 25, 20, 10]

    if len(services_labels) < 4:
        for i, service in enumerate(default_services):
            if service not in services_labels:
                services_labels.append(service)
                services_data.append(default_data[i])
                if len(services_labels) >= 4:
                    break

    # Website traffic (mock data for now - would come from analytics)
    traffic_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    traffic_data = [120, 190, 300, 500, 200, 300, 450]

    return Response({
        'stats': {
            'total_revenue': total_revenue,
            'revenue_change': revenue_change,
            'active_users': active_users,
            'total_enquiries': total_enquiries,
            'customer_satisfaction': customer_satisfaction,
            'total_reviews': total_reviews,
            'total_offers': total_offers,
            'total_posts': total_posts
        },
        'recent_activities': activities,
        'charts': {
            'revenue': {
                'labels': revenue_labels,
                'data': revenue_data
            },
            'services': {
                'labels': services_labels,
                'data': services_data
            },
            'traffic': {
                'labels': traffic_labels,
                'data': traffic_data
            }
        }
    })
