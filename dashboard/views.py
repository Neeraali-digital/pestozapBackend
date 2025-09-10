from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
from enquiries.models import Enquiry
from offers.models import Offer
from reviews.models import Review
from apps.users.models import User

@api_view(['GET'])
def dashboard_stats(request):
    # Basic stats
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    total_enquiries = Enquiry.objects.count()
    new_enquiries = Enquiry.objects.filter(status='new').count()
    
    # Revenue calculation (mock data for now)
    total_revenue = 45230
    revenue_change = 12.5
    
    # Recent activities
    recent_enquiries = Enquiry.objects.order_by('-created_at')[:5]
    activities = []
    for enquiry in recent_enquiries:
        activities.append({
            'action': f'New service request from {enquiry.customer_name}',
            'time': enquiry.created_at.strftime('%Y-%m-%d %H:%M'),
            'type': 'request'
        })
    
    # Chart data
    last_6_months = []
    revenue_data = [12000, 19000, 15000, 25000, 22000, 30000]
    
    return Response({
        'stats': {
            'total_revenue': total_revenue,
            'revenue_change': revenue_change,
            'active_users': active_users,
            'total_enquiries': total_enquiries,
            'customer_satisfaction': 98.5
        },
        'recent_activities': activities,
        'charts': {
            'revenue': {
                'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                'data': revenue_data
            },
            'services': {
                'labels': ['Pest Control', 'Termite', 'Rodent', 'Inspection'],
                'data': [45, 25, 20, 10]
            },
            'traffic': {
                'labels': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                'data': [120, 190, 300, 500, 200, 300, 450]
            }
        }
    })